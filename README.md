# Tic-Tac-Toe — FastAPI + React

A full-stack Tic-Tac-Toe web app with a FastAPI backend and React JSX frontend.

## Run locally

```bash
pip install -r requirements.txt
uvicorn backend.backend:app --reload --port 8000
```

Open http://localhost:8000

## Docker

```bash
docker build -t tictactoe .
docker run -p 8000:8000 tictactoe
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/state` | Current game state |
| POST | `/move` | Make a move `{"index": 0-8}` |
| POST | `/start` | Reset the game |
