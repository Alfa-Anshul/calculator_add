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

# ── Game State ──────────────────────────────────────────────
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
    [0,4,8],[2,4,6],
]

def check_winner(board):
    for combo in WINNING_COMBOS:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def check_draw(board):
    return all(cell != "" for cell in board)

# ── Endpoints ───────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "Tic-Tac-Toe API"}

@app.get("/state")
def get_state():
    return game_state

@app.post("/start")
def start_game():
    game_state["board"] = [""] * 9
    game_state["current_player"] = "X"
    game_state["winner"] = None
    game_state["game_over"] = False
    return {"message": "Game started", "state": game_state}

class MoveRequest(BaseModel):
    index: int

@app.post("/move")
def make_move(req: MoveRequest):
    idx = req.index
    if game_state["game_over"]:
        return {"error": "Game is over. Start a new game.", "state": game_state}
    if idx < 0 or idx > 8:
        return {"error": "Invalid index", "state": game_state}
    if game_state["board"][idx] != "":
        return {"error": "Cell already taken", "state": game_state}

    game_state["board"][idx] = game_state["current_player"]
    winner = check_winner(game_state["board"])

    if winner:
        game_state["winner"] = winner
        game_state["game_over"] = True
        game_state["scores"][winner] += 1
    elif check_draw(game_state["board"]):
        game_state["winner"] = "Draw"
        game_state["game_over"] = True
        game_state["scores"]["draws"] += 1
    else:
        game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"

    return {"state": game_state}

# ── Serve Frontend ──────────────────────────────────────────
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def root():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Tic-Tac-Toe API running. Visit /docs"}
