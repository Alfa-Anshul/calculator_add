# 🐍 Snake Game — FastAPI + React

Refactored from calculator app. Snake game with FastAPI backend and JSX frontend.

## Run Locally
```bash
pip install -r requirements.txt
uvicorn backend.backend:app --host 0.0.0.0 --port 8000
```

## Docker
```bash
docker build -t snake-game .
docker run -p 8000:8000 snake-game
```

## API Endpoints
- `GET /` — Health check
- `POST /start` — Start new game
- `POST /move` — Move snake `{"direction": "UP|DOWN|LEFT|RIGHT"}`
- `GET /state` — Get current game state
- `GET /docs` — Swagger UI
