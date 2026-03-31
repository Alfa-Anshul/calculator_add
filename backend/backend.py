from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import random

app = FastAPI(title="Snake Game")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GRID_SIZE = 20

game_state = {
    "snake": [(10, 10), (10, 9), (10, 8)],
    "food": (5, 5),
    "direction": "RIGHT",
    "score": 0,
    "game_over": False,
    "started": False,
}

def spawn_food(snake):
    while True:
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if pos not in snake:
            return pos

@app.get("/")
def health():
    return {"status": "Snake Game API running"}

@app.post("/start")
def start_game():
    global game_state
    snake = [(10, 10), (10, 9), (10, 8)]
    game_state = {
        "snake": snake,
        "food": spawn_food(snake),
        "direction": "RIGHT",
        "score": 0,
        "game_over": False,
        "started": True,
    }
    return game_state

class MoveRequest(BaseModel):
    direction: str

@app.post("/move")
def move_snake(req: MoveRequest):
    global game_state
    if game_state["game_over"] or not game_state["started"]:
        return game_state

    direction = req.direction.upper()
    opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
    if direction in opposite and opposite[direction] != game_state["direction"]:
        game_state["direction"] = direction

    head = game_state["snake"][0]
    d = game_state["direction"]
    if d == "UP":    new_head = (head[0] - 1, head[1])
    elif d == "DOWN":  new_head = (head[0] + 1, head[1])
    elif d == "LEFT":  new_head = (head[0], head[1] - 1)
    else:              new_head = (head[0], head[1] + 1)

    # Wall collision
    if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
        game_state["game_over"] = True
        return game_state

    # Self collision
    if new_head in game_state["snake"]:
        game_state["game_over"] = True
        return game_state

    game_state["snake"] = [new_head] + game_state["snake"]

    if new_head == game_state["food"]:
        game_state["score"] += 10
        game_state["food"] = spawn_food(game_state["snake"])
    else:
        game_state["snake"].pop()

    return game_state

@app.get("/state")
def get_state():
    return game_state

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
