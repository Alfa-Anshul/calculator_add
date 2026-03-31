from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os

app = FastAPI(title="Tic-Tac-Toe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

game_state = {
    "board": [""] * 9,
    "current_player": "X",
    "winner": None,
    "game_over": False,
    "winning_combo": [],
    "scores": {"X": 0, "O": 0, "draws": 0}
}

WINNING_COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

def check_winner(board):
    for combo in WINNING_COMBOS:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], combo
    if "" not in board:
        return "draw", []
    return None, []

class MoveRequest(BaseModel):
    index: int

@app.get("/api")
def health_check():
    return {"status": "ok", "message": "Tic-Tac-Toe API running"}

@app.get("/api/state")
def get_state():
    return game_state

@app.post("/api/move")
def make_move(req: MoveRequest):
    idx = req.index
    if game_state["game_over"] or game_state["board"][idx] != "":
        return JSONResponse(status_code=400, content={"error": "Invalid move", **game_state})
    game_state["board"][idx] = game_state["current_player"]
    result, combo = check_winner(game_state["board"])
    if result:
        game_state["game_over"] = True
        game_state["winning_combo"] = combo
        if result == "draw":
            game_state["winner"] = "draw"
            game_state["scores"]["draws"] += 1
        else:
            game_state["winner"] = result
            game_state["scores"][result] += 1
    else:
        game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"
    return game_state

@app.post("/api/start")
def start_game():
    game_state["board"] = [""] * 9
    game_state["current_player"] = "X"
    game_state["winner"] = None
    game_state["game_over"] = False
    game_state["winning_combo"] = []
    return game_state

# Serve static frontend files — MUST be after API routes
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/App.jsx")
def serve_jsx():
    return FileResponse(os.path.join(frontend_dir, "App.jsx"), media_type="application/javascript")

@app.get("/style.css")
def serve_css():
    return FileResponse(os.path.join(frontend_dir, "style.css"), media_type="text/css")
