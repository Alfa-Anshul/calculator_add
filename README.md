# Tic Tac Toe Web Game

A modern tic-tac-toe web application built with FastAPI backend and React JSX frontend.

## Features

- 🎮 Interactive tic-tac-toe gameplay
- 📊 Score tracking for X, O, and draws
- 🎨 Beautiful responsive UI
- 🚀 Fast API backend with CORS enabled
- 📱 Mobile-friendly design

## Project Structure

```
├── backend/
│   └── backend.py          # FastAPI application
├── frontend/
│   ├── index.html          # HTML entry point
│   ├── app.jsx             # React component
│   └── style.css           # Styling
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
└── README.md              # This file
```

## Installation

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   uvicorn backend.backend:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Open in browser:**
   ```
   http://localhost:8000
   ```

## Docker Deployment

1. **Build the image:**
   ```bash
   docker build -t tic-tac-toe .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 tic-tac-toe
   ```

## API Endpoints

- `GET /` - Health check
- `GET /state` - Get current game state
- `POST /move` - Make a move (position: 0-8)
- `POST /reset` - Reset the board
- `POST /reset-scores` - Reset all scores
- `GET /docs` - FastAPI interactive documentation

## Game Rules

- Players take turns marking X and O
- First player to get 3 in a row (horizontally, vertically, or diagonally) wins
- If all 9 squares are filled with no winner, it's a draw
- Scores are tracked across multiple games

## Technologies

- **Backend:** FastAPI, Uvicorn
- **Frontend:** React 18, JSX
- **Deployment:** Docker, Docker Compose
- **Server:** Python 3.10

## License

MIT
