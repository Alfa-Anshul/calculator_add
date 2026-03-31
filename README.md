# 🐍 Snake Web Game — FastAPI + React

A classic Snake game with a FastAPI backend and React frontend, served as static files.

## Structure

```
backend/backend.py   # FastAPI app + game logic
frontend/App.jsx     # React game UI
frontend/index.html  # Entry point
frontend/style.css   # Styles
requirements.txt
Dockerfile
```

## Endpoints

| Method | Path     | Description          |
|--------|----------|----------------------|
| GET    | /        | Health check         |
| POST   | /start   | Start new game       |
| POST   | /move    | Move snake (body: `{"direction": "UP"}`) |
| GET    | /state   | Get current state    |

## Run Locally

```bash
pip install -r requirements.txt
uvicorn backend.backend:app --reload
```

Open: http://localhost:8000

## Docker

```bash
docker build -t snake-game .
docker run -p 8000:8000 snake-game
```

API Docs: http://localhost:8000/docs
