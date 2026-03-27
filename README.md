# 🧮 Calculator Application

A simple yet elegant calculator built with **Flask** (backend) and **React** (frontend) that performs addition and subtraction operations.

## 📋 Project Structure

```
calculator_app/
├── backend/
│   ├── backend.py          # Flask API server
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── Calculator.jsx       # Main calculator component
│   ├── Calculator.css       # Styling
│   ├── App.jsx             # Root component
│   ├── App.css             # App styles
│   ├── vite.config.js      # Vite configuration
│   └── package.json        # Node dependencies
└── README.md
```

## 🔧 Installation & Setup

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python backend.py
```

Backend runs on: `http://localhost:5000`

**Endpoints:**
- `GET /api/health` - Health check
- `POST /api/add` - Addition operation
- `POST /api/subtract` - Subtraction operation

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:5173`

## 📐 Mathematical Operations

### Addition
```
Formula: f(a, b) = a + b
Properties:
- Closure: a + b ∈ ℝ
- Identity: a + 0 = a
- Associative: (a + b) + c = a + (b + c)
- Commutative: a + b = b + a
```

### Subtraction
```
Formula: f(a, b) = a - b = a + (-b)
Properties:
- Non-associative: (a - b) - c ≠ a - (b - c)
- Non-commutative: a - b ≠ b - a
```

## 🚀 API Documentation

### Add Operation

**Request:**
```http
POST /api/add
Content-Type: application/json

{
  "a": 10,
  "b": 5
}
```

**Response:**
```json
{
  "operation": "addition",
  "operand_a": 10,
  "operand_b": 5,
  "result": 15,
  "formula": "10 + 5 = 15",
  "mathematical_formula": "f(a, b) = a + b",
  "timestamp": "2026-03-27T08:30:00.000000"
}
```

### Subtract Operation

**Request:**
```http
POST /api/subtract
Content-Type: application/json

{
  "a": 10,
  "b": 5
}
```

**Response:**
```json
{
  "operation": "subtraction",
  "operand_a": 10,
  "operand_b": 5,
  "result": 5,
  "formula": "10 - 5 = 5",
  "mathematical_formula": "f(a, b) = a - b = a + (-b)",
  "timestamp": "2026-03-27T08:30:00.000000"
}
```

## ✨ Features

✅ **Real-time Calculations** - Instant results via API  
✅ **Backend Health Check** - Automatic connection monitoring  
✅ **Calculation History** - Keep track of all operations  
✅ **Error Handling** - Comprehensive input validation  
✅ **Dark Theme UI** - Modern, elegant interface  
✅ **Responsive Design** - Works on all devices  
✅ **Mathematical Notation** - Display formulas and properties  

## 🔐 Technical Stack

- **Backend:** Flask 2.3.2, Flask-CORS, Python 3.8+
- **Frontend:** React 18.2, Vite 4.3, CSS3
- **Architecture:** REST API with JSON
- **Deployment Ready:** Includes Gunicorn config

## 📝 Code Mathematics

Every operation is expressed in both code and mathematical notation:

```python
# Python Code
result = a + b

# Mathematical Formula
f(a, b) = a + b ∈ ℝ
```

```javascript
// JavaScript Code
const result = a + b;

// Mathematical Formula
f(a, b) = a + b
```

## 🌐 CORS Configuration

The backend is configured to accept requests from any origin. For production, update the CORS settings in `backend.py`:

```python
CORS(app, resources={r"/*": {"origins": ["https://yourdomain.com"]}})
```

## 📄 License

MIT License - Feel free to use this project for learning and development.

---

**Built with 🔥 for learning and mastery**
