# Tic-Tac-Toe Web App

FastAPI backend + React JSX frontend, Dockerized.

## Run locally
```bash
docker build -t tictactoe .
docker run -p 8000:8000 tictactoe
```
Open: http://localhost:8000

## API Endpoints
- `GET /` — health check
- `GET /state` — current game state
- `POST /move` — `{ "index": 0-8 }`
- `POST /start` — reset game
- `GET /docs` — Swagger UI
