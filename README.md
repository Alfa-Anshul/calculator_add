# ⚡ Tic-Tac-Toe Web App

A full-stack Tic-Tac-Toe game built with **FastAPI** (backend) and **React JSX** (frontend), served in a single Docker container.

## Stack
- **Backend**: FastAPI + Uvicorn
- **Frontend**: React 18 (CDN, in-browser Babel)
- **Container**: Docker (python:3.10-slim)

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Serve frontend |
| GET | `/health` | Health check |
| GET | `/state` | Get game state |
| POST | `/start` | Start/reset game |
| POST | `/move` | Make a move `{index: 0-8}` |
| GET | `/docs` | Swagger UI |

## Run Locally
```bash
docker build -t tictactoe .
docker run -p 8000:8000 tictactoe
```
Open: http://localhost:8000
