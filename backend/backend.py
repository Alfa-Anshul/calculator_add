from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import random

app = FastAPI(title="Snake Game API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GRID_SIZE = 20

game_state = {
    "snake": [],
    "food": None,
    "direction": "RIGHT",
    "score": 0,
    "game_over": False,
    "started": False,
}


def random_food(snake):
    while True:
        pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
        if pos not in snake:
            return pos


class MoveRequest(BaseModel):
    direction: str


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Snake Game API running"}


@app.post("/start")
def start_game():
    mid = GRID_SIZE // 2
    snake = [[mid, mid], [mid, mid - 1], [mid, mid - 2]]
    game_state.update({
        "snake": snake,
        "food": random_food(snake),
        "direction": "RIGHT",
        "score": 0,
        "game_over": False,
        "started": True,
    })
    return {"status": "started", "state": game_state}


@app.post("/move")
def move_snake(req: MoveRequest):
    if not game_state["started"] or game_state["game_over"]:
        return {"error": "Game not active", "state": game_state}

    direction = req.direction.upper()
    opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
    if direction in opposites and opposites[direction] != game_state["direction"]:
        game_state["direction"] = direction

    head = game_state["snake"][0][:]
    d = game_state["direction"]
    if d == "UP":    head[0] -= 1
    elif d == "DOWN":  head[0] += 1
    elif d == "LEFT":  head[1] -= 1
    elif d == "RIGHT": head[1] += 1

    # Wall collision
    if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
        game_state["game_over"] = True
        return {"state": game_state}

    # Self collision
    if head in game_state["snake"]:
        game_state["game_over"] = True
        return {"state": game_state}

    game_state["snake"].insert(0, head)

    if head == game_state["food"]:
        game_state["score"] += 10
        game_state["food"] = random_food(game_state["snake"])
    else:
        game_state["snake"].pop()

    return {"state": game_state}


@app.get("/state")
def get_state():
    return {"state": game_state}


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
