from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(title="Tic-Tac-Toe")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Game State ──────────────────────────────────────────────
game = {
    "board": [""] * 9,
    "current_player": "X",
    "winner": None,
    "draw": False,
    "scores": {"X": 0, "O": 0}
}

WINNING = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

def check_winner(board):
    for line in WINNING:
        a,b,c = line
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

# ── Models ──────────────────────────────────────────────────
class MoveRequest(BaseModel):
    index: int

# ── Routes ──────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "game": "tic-tac-toe"}

@app.get("/state")
def get_state():
    return game

@app.post("/start")
def start_game():
    game["board"] = [""] * 9
    game["current_player"] = "X"
    game["winner"] = None
    game["draw"] = False
    return game

@app.post("/move")
def make_move(req: MoveRequest):
    if game["winner"] or game["draw"]:
        return {"error": "Game over. Start a new game.", **game}
    if req.index < 0 or req.index > 8:
        return {"error": "Invalid index"}
    if game["board"][req.index] != "":
        return {"error": "Cell already taken"}
    game["board"][req.index] = game["current_player"]
    winner = check_winner(game["board"])
    if winner:
        game["winner"] = winner
        game["scores"][winner] += 1
    elif "" not in game["board"]:
        game["draw"] = True
    else:
        game["current_player"] = "O" if game["current_player"] == "X" else "X"
    return game

# ── Serve Frontend ──────────────────────────────────────────
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Tic-Tac-Toe API running. Visit /docs"}
