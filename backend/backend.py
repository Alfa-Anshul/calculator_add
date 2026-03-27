from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Union, Dict, Any
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CalculatorEngine:
    """
    Mathematical Calculator Engine
    
    Operations:
    - Addition: f(a, b) = a + b ∈ ℝ
    - Subtraction: f(a, b) = a - b ∈ ℝ
    
    Mathematical Properties:
    Addition:
      • Closure: a + b ∈ ℝ
      • Identity: a + 0 = a
      • Associative: (a + b) + c = a + (b + c)
      • Commutative: a + b = b + a
    
    Subtraction:
      • Non-associative: (a - b) - c ≠ a - (b - c)
      • Non-commutative: a - b ≠ b - a
      • Right-cancellative: a - c = b - c → a = b
    """
    
    @staticmethod
    def validate_input(a: Any, b: Any) -> tuple[bool, Union[str, None]]:
        """
        Input validation: Check if inputs are valid real numbers
        Mathematical constraint: a, b ∈ ℝ
        """
        try:
            float(a)
            float(b)
            return True, None
        except (ValueError, TypeError):
            return False, "Input must be numeric (integers or decimals)"
    
    @staticmethod
    def add(a: float, b: float) -> Dict[str, Any]:
        """
        Addition: result = a + b
        
        Mathematical Formula:
        f_add(a, b) = a + b
        
        Code Implementation:
        return a + b
        """
        result = a + b
        return {
            'operation': 'addition',
            'operand_a': a,
            'operand_b': b,
            'result': result,
            'formula': f'{a} + {b} = {result}',
            'mathematical_formula': 'f(a, b) = a + b',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def subtract(a: float, b: float) -> Dict[str, Any]:
        """
        Subtraction: result = a - b = a + (-b)
        
        Mathematical Formula:
        f_sub(a, b) = a - b = a + (-b)
        
        Code Implementation:
        return a - b
        """
        result = a - b
        return {
            'operation': 'subtraction',
            'operand_a': a,
            'operand_b': b,
            'result': result,
            'formula': f'{a} - {b} = {result}',
            'mathematical_formula': 'f(a, b) = a - b = a + (-b)',
            'timestamp': datetime.now().isoformat()
        }


calculator = CalculatorEngine()


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint: Verify backend is running
    Response: {status: 'healthy'}
    """
    logger.info('Health check requested')
    return jsonify({
        'status': 'healthy',
        'service': 'Calculator API v1.0',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/add', methods=['POST'])
def add_operation():
    """
    Addition endpoint
    
    Request: POST /api/add
    Body: {"a": float, "b": float}
    
    Response: {
        "operation": "addition",
        "operand_a": float,
        "operand_b": float,
        "result": float,
        "formula": "a + b = result"
    }
    
    Mathematical Operation: f(a, b) = a + b
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        a = data.get('a')
        b = data.get('b')
        
        # Validate input
        is_valid, error_msg = calculator.validate_input(a, b)
        if not is_valid:
            logger.warning(f'Invalid input for addition: a={a}, b={b}')
            return jsonify({'error': error_msg}), 400
        
        a = float(a)
        b = float(b)
        
        result = calculator.add(a, b)
        logger.info(f'Addition: {a} + {b} = {result["result"]}')
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f'Addition operation failed: {str(e)}')
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.route('/api/subtract', methods=['POST'])
def subtract_operation():
    """
    Subtraction endpoint
    
    Request: POST /api/subtract
    Body: {"a": float, "b": float}
    
    Response: {
        "operation": "subtraction",
        "operand_a": float,
        "operand_b": float,
        "result": float,
        "formula": "a - b = result"
    }
    
    Mathematical Operation: f(a, b) = a - b
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        a = data.get('a')
        b = data.get('b')
        
        # Validate input
        is_valid, error_msg = calculator.validate_input(a, b)
        if not is_valid:
            logger.warning(f'Invalid input for subtraction: a={a}, b={b}')
            return jsonify({'error': error_msg}), 400
        
        a = float(a)
        b = float(b)
        
        result = calculator.subtract(a, b)
        logger.info(f'Subtraction: {a} - {b} = {result["result"]}')
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f'Subtraction operation failed: {str(e)}')
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    logger.info('Starting Calculator Backend Server...')
    app.run(debug=True, host='0.0.0.0', port=5000)
