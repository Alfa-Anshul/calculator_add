from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from typing import List, Optional

app = FastAPI(title="Tic Tac Toe API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game state storage (in-memory)
game_state = {
    "board": [None] * 9,
    "current_player": "X",
    "game_over": False,
    "winner": None,
    "x_score": 0,
    "o_score": 0,
    "draws": 0
}

# Winning combinations
WINNING_COMBOS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

def check_winner(board: List) -> Optional[str]:
    """Check if there's a winner."""
    for combo in WINNING_COMBOS:
        if board[combo[0]] and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]]
    return None

def check_draw(board: List) -> bool:
    """Check if the game is a draw."""
    return None not in board

@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Tic Tac Toe API is running"}

@app.get("/state")
async def get_state():
    """Get current game state."""
    return game_state

@app.post("/move")
async def make_move(position: int):
    """Make a move on the board."""
    if position < 0 or position > 8:
        return {"error": "Invalid position", "status": "error"}
    
    if game_state["board"][position] is not None:
        return {"error": "Position already taken", "status": "error"}
    
    if game_state["game_over"]:
        return {"error": "Game is over", "status": "error"}
    
    # Make the move
    game_state["board"][position] = game_state["current_player"]
    
    # Check for winner
    winner = check_winner(game_state["board"])
    if winner:
        game_state["game_over"] = True
        game_state["winner"] = winner
        if winner == "X":
            game_state["x_score"] += 1
        else:
            game_state["o_score"] += 1
        return {"status": "win", "winner": winner, "game_state": game_state}
    
    # Check for draw
    if check_draw(game_state["board"]):
        game_state["game_over"] = True
        game_state["draws"] += 1
        return {"status": "draw", "game_state": game_state}
    
    # Switch player
    game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"
    
    return {"status": "ok", "game_state": game_state}

@app.post("/reset")
async def reset_game():
    """Reset the game board."""
    x_score = game_state["x_score"]
    o_score = game_state["o_score"]
    draws = game_state["draws"]
    
    game_state["board"] = [None] * 9
    game_state["current_player"] = "X"
    game_state["game_over"] = False
    game_state["winner"] = None
    game_state["x_score"] = x_score
    game_state["o_score"] = o_score
    game_state["draws"] = draws
    
    return {"status": "reset", "game_state": game_state}

@app.post("/reset-scores")
async def reset_scores():
    """Reset all scores."""
    game_state["board"] = [None] * 9
    game_state["current_player"] = "X"
    game_state["game_over"] = False
    game_state["winner"] = None
    game_state["x_score"] = 0
    game_state["o_score"] = 0
    game_state["draws"] = 0
    
    return {"status": "scores_reset", "game_state": game_state}

# Serve static files
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
