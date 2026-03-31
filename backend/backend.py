from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(title="Tic-Tac-Toe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Game State ---
game_state = {
    "board": [""] * 9,
    "current_player": "X",
    "winner": None,
    "game_over": False,
    "scores": {"X": 0, "O": 0, "draws": 0},
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
            return board[a]
    return None

class MoveRequest(BaseModel):
    index: int

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Tic-Tac-Toe API running"}

@app.get("/state")
def get_state():
    return game_state

@app.post("/move")
def make_move(req: MoveRequest):
    if game_state["game_over"]:
        return {"error": "Game is over. Reset to play again.", **game_state}
    if game_state["board"][req.index] != "":
        return {"error": "Cell already occupied.", **game_state}
    
    game_state["board"][req.index] = game_state["current_player"]
    winner = check_winner(game_state["board"])
    
    if winner:
        game_state["winner"] = winner
        game_state["game_over"] = True
        game_state["scores"][winner] += 1
    elif "" not in game_state["board"]:
        game_state["game_over"] = True
        game_state["winner"] = "Draw"
        game_state["scores"]["draws"] += 1
    else:
        game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"
    
    return game_state

@app.post("/reset")
def reset_game():
    game_state["board"] = [""] * 9
    game_state["current_player"] = "X"
    game_state["winner"] = None
    game_state["game_over"] = False
    return game_state

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/app", include_in_schema=False)
    def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))
