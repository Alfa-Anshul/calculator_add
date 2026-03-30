# Simple Calculator

This is a small full-stack calculator website with:

- `backend/backend.py` for the Flask API
- `frontend/App.jsx` for the React UI

It supports only two operations:

- Addition
- Subtraction

## Run the backend

```bash
cd backend
pip install -r requirements.txt
python backend.py
```

The API starts on `http://localhost:5000`.

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend calls the backend at `http://localhost:5000/api`.

## API endpoints

- `GET /api/health`
- `POST /api/add`
- `POST /api/subtract`
