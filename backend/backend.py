from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Calculator:
    """
    Simple Calculator for Addition and Subtraction
    Mathematical Operations:
    - Addition: f(a, b) = a + b ∈ ℝ
    - Subtraction: f(a, b) = a - b ∈ ℝ
    """
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """
        Addition operation: result = a + b
        Mathematical property: Closure under addition
        Identity element: a + 0 = a
        Associative: (a + b) + c = a + (b + c)
        """
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """
        Subtraction operation: result = a - b = a + (-b)
        Not associative: (a - b) - c ≠ a - (b - c)
        """
        return a - b

calc = Calculator()

@app.route('/add', methods=['POST'])
def add():
    """Endpoint for addition"""
    try:
        data = request.json
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        result = calc.add(a, b)
        return jsonify({
            'operation': 'addition',
            'operand_a': a,
            'operand_b': b,
            'result': result,
            'formula': f'{a} + {b} = {result}'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/subtract', methods=['POST'])
def subtract():
    """Endpoint for subtraction"""
    try:
        data = request.json
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        result = calc.subtract(a, b)
        return jsonify({
            'operation': 'subtraction',
            'operand_a': a,
            'operand_b': b,
            'result': result,
            'formula': f'{a} - {b} = {result}'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'Calculator backend running'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
