from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import copy

app = FastAPI(title="Tic-Tac-Toe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game state
game_state = {
    "board": [""] * 9,
    "current_player": "X",
    "winner": None,
    "game_over": False,
    "scores": {"X": 0, "O": 0, "draws": 0}
}

WINNING_COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],  # rows
    [0,3,6],[1,4,7],[2,5,8],  # cols
    [0,4,8],[2,4,6]           # diags
]

def check_winner(board):
    for combo in WINNING_COMBOS:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "draw"
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
    idx = req.index
    if game_state["game_over"] or game_state["board"][idx] != "":
        return {"error": "Invalid move", **game_state}
    game_state["board"][idx] = game_state["current_player"]
    result = check_winner(game_state["board"])
    if result:
        game_state["game_over"] = True
        if result == "draw":
            game_state["winner"] = "draw"
            game_state["scores"]["draws"] += 1
        else:
            game_state["winner"] = result
            game_state["scores"][result] += 1
    else:
        game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"
    return game_state

@app.post("/start")
def start_game():
    game_state["board"] = [""] * 9
    game_state["current_player"] = "X"
    game_state["winner"] = None
    game_state["game_over"] = False
    return game_state

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
