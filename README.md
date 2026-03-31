# Tic-Tac-Toe Web App

Full-stack Tic-Tac-Toe game built with **FastAPI** (backend) + **React JSX** (frontend), containerized with Docker.

## Stack
- Backend: FastAPI + Uvicorn
- Frontend: React 18 (CDN, no build step) + Babel standalone
- Container: Python 3.10-slim Docker

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Serves frontend |
| GET | `/health` | Health check |
| GET | `/state` | Current game state |
| POST | `/start` | Reset/start new game |
| POST | `/move` | Make a move `{"index": 0-8}` |
| GET | `/docs` | Swagger UI |

## Run Locally
```bash
docker build -t tictactoe .
docker run -p 8000:8000 tictactoe
```
Open: http://localhost:8000

## Board Index Map
```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```
