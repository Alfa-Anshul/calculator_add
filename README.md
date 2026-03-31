# Tic-Tac-Toe (FastAPI + React)

A full-stack Tic-Tac-Toe web app.

## Stack
- **Backend**: FastAPI (Python 3.10)
- **Frontend**: React JSX (served as static files)
- **Deploy**: Docker on EC2

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/state` | Get current game state |
| POST | `/move` | Make a move `{"index": 0-8}` |
| POST | `/reset` | Reset the board |
| GET | `/app` | Frontend UI |
| GET | `/docs` | Swagger UI |

## Run locally
```bash
pip install -r requirements.txt
uvicorn backend.backend:app --reload
```

## Docker
```bash
docker build -t tictactoe .
docker run -p 8000:8000 tictactoe
```
