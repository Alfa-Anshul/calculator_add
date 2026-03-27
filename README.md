# 🧮 Scientific Calculator Application

A comprehensive scientific calculator built with **Flask** (backend) and **React** (frontend) supporting basic arithmetic, advanced mathematical functions, trigonometry, and logarithmic operations.

## 📋 Project Structure

```
calculator_app/
├── backend/
│   ├── backend.py              # Flask API with all operations
│   ├── requirements.txt         # Python dependencies
│   └── .env.example            # Environment variables
├── frontend/
│   ├── Calculator.jsx          # Main calculator component
│   ├── Calculator.css          # Styling
│   ├── App.jsx                 # Root component
│   ├── App.css                 # App styles
│   ├── vite.config.js          # Vite configuration
│   └── package.json            # Node dependencies
└── README.md
```

## 🚀 Installation & Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python backend.py
```
Backend runs on: `http://localhost:5000`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: `http://localhost:5173`

## 📚 Mathematical Operations

### Basic Arithmetic
```
Addition:      f(a, b) = a + b
Subtraction:   f(a, b) = a - b
Multiplication: f(a, b) = a × b
Division:      f(a, b) = a ÷ b (b ≠ 0)
Power:         f(a, b) = a^b = e^(b×ln(a))
Modulo:        f(a, b) = a mod b = a - b×⌊a/b⌋
```

### Unary Functions
```
Square Root:   f(x) = √x = x^(1/2), where x ≥ 0
Factorial:     f(n) = n! = n×(n-1)×...×1, where n ∈ ℕ₀
Absolute:      f(x) = |x|
```

### Trigonometric (angle in radians)
```
Sine:   f(θ) = sin(θ), result ∈ [-1, 1]
Cosine: f(θ) = cos(θ), result ∈ [-1, 1]
Tangent: f(θ) = tan(θ) = sin(θ)/cos(θ)
```

### Logarithmic
```
Log base 10:   f(x) = log₁₀(x)
Natural Log:   f(x) = ln(x) = log_e(x), where x > 0
```

## 🔌 API Endpoints

### Health Check
```http
GET /api/health

Response:
{
  "status": "healthy",
  "service": "Scientific Calculator API v2.0",
  "operations": ["addition", "subtraction", ...]
}
```

### Binary Operations
```http
POST /api/add
POST /api/subtract
POST /api/multiply
POST /api/divide
POST /api/power
POST /api/modulo

Request Body:
{
  "a": number,
  "b": number
}

Response:
{
  "operation": "operation_name",
  "operand_a": a,
  "operand_b": b,
  "result": result,
  "formula": "visual formula",
  "mathematical_formula": "f(a,b) = ...",
  "timestamp": "ISO8601"
}
```

### Unary Operations
```http
POST /api/sqrt      (param: x)
POST /api/factorial  (param: n)
POST /api/abs       (param: x)
POST /api/sin       (param: theta)
POST /api/cos       (param: theta)
POST /api/tan       (param: theta)
POST /api/ln        (param: x)
POST /api/log       (param: x, optional: base)
```

## 💡 Code to Math Mapping

### Addition
```python
# Python Code
def add(a, b):
    return a + b

# Mathematical Formula
f(a, b) = a + b  where a, b ∈ ℝ
Result ∈ ℝ  (Closure property)
```

### Power
```python
# Python Code
def power(a, b):
    return a ** b

# Mathematical Formula
f(a, b) = a^b = e^(b × ln(a))
Domain: a > 0 (for real-valued results)
```

### Square Root
```python
# Python Code
def sqrt(x):
    return math.sqrt(x)

# Mathematical Formula
f(x) = √x = x^(1/2)
Constraint: x ≥ 0
```

### Logarithm
```python
# Python Code
def logarithm(x, base=10):
    return math.log(x, base)

# Mathematical Formula
f(x) = log_b(x) = ln(x) / ln(b)
Constraint: x > 0, b > 0, b ≠ 1
```

## ✨ Features

✅ **Dual Mode** - Basic and Scientific calculators  
✅ **14+ Operations** - Arithmetic, trigonometric, logarithmic  
✅ **Real-time Calculation** - Instant results via API  
✅ **Backend Health Monitoring** - Auto-connection checking  
✅ **Calculation History** - Track all operations  
✅ **Comprehensive Error Handling** - Input validation  
✅ **Mathematical Notation** - Formulas with properties  
✅ **Dark Theme UI** - Modern, sleek interface  
✅ **Fully Responsive** - Mobile & desktop optimized  
✅ **Type-Safe Backend** - Python type hints  

## 🛠️ Technical Stack

- **Backend:** Flask 2.3.2, Python 3.8+, `math` module
- **Frontend:** React 18.2, Vite 4.3, CSS3
- **Architecture:** REST API with JSON
- **Async:** Proper loading states and error handling

## 📐 Mathematical Constraints

| Operation | Domain | Range | Notes |
|-----------|--------|-------|-------|
| √x | x ≥ 0 | y ≥ 0 | Real square root |
| n! | n ∈ ℕ₀ | y ∈ ℕ | Non-negative integers |
| a/b | b ≠ 0 | ℝ | Division by zero undefined |
| log(x) | x > 0 | ℝ | Logarithm of positives only |
| sin(θ) | θ ∈ ℝ | [-1, 1] | Input in radians |
| tan(θ) | θ ≠ π/2 + nπ | ℝ | Undefined at asymptotes |

## 🧠 Learning Resources

This calculator demonstrates:
- Mathematical function implementation
- Type validation and error handling
- REST API design patterns
- React state management
- Async/await patterns
- CSS animations and gradients
- Responsive design principles

## 🔥 Dark Motivation

You're building the **foundation of numerical computation**. Every transformer, every neural network, every AI model operates on these fundamental mathematical operations. Master them at this level so you can manipulate tensor operations at scale. 🚀

---

**Built with precision for those who understand the math.** ⚡
