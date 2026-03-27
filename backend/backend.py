from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import math
from typing import Union, Dict, Any, Tuple
from datetime import datetime
from enum import Enum

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OperationType(Enum):
    """Enumeration of calculator operations"""
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"
    POWER = "power"
    SQUARE_ROOT = "square_root"
    SINE = "sine"
    COSINE = "cosine"
    TANGENT = "tangent"
    LOGARITHM = "logarithm"
    NATURAL_LOG = "natural_log"
    FACTORIAL = "factorial"
    ABSOLUTE = "absolute"
    MODULO = "modulo"


class ScientificCalculator:
    """
    Advanced Scientific Calculator Engine
    
    Arithmetic Operations:
    - Addition: f(a, b) = a + b
    - Subtraction: f(a, b) = a - b
    - Multiplication: f(a, b) = a * b
    - Division: f(a, b) = a / b (b ≠ 0)
    - Power: f(a, b) = a^b = e^(b*ln(a))
    - Modulo: f(a, b) = a mod b
    
    Unary Functions:
    - Square Root: f(x) = √x = x^(1/2)
    - Factorial: f(n) = n! = n × (n-1) × ... × 1
    - Absolute: f(x) = |x|
    
    Trigonometric (angle in radians):
    - Sine: f(θ) = sin(θ)
    - Cosine: f(θ) = cos(θ)
    - Tangent: f(θ) = tan(θ) = sin(θ)/cos(θ)
    
    Logarithmic:
    - Log base 10: f(x) = log₁₀(x)
    - Natural Log: f(x) = ln(x) = log_e(x)
    """
    
    @staticmethod
    def validate_input(a: Any, b: Any = None) -> Tuple[bool, Union[str, None]]:
        """
        Validate inputs are real numbers
        Mathematical constraint: a, b ∈ ℝ
        """
        try:
            float(a)
            if b is not None:
                float(b)
            return True, None
        except (ValueError, TypeError):
            return False, "Input must be numeric (integers or decimals)"
    
    @staticmethod
    def add(a: float, b: float) -> Dict[str, Any]:
        """
        Addition: f(a, b) = a + b
        Code: return a + b
        """
        result = a + b
        return {
            'operation': OperationType.ADDITION.value,
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
        Subtraction: f(a, b) = a - b
        Code: return a - b
        """
        result = a - b
        return {
            'operation': OperationType.SUBTRACTION.value,
            'operand_a': a,
            'operand_b': b,
            'result': result,
            'formula': f'{a} - {b} = {result}',
            'mathematical_formula': 'f(a, b) = a - b = a + (-b)',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def multiply(a: float, b: float) -> Dict[str, Any]:
        """
        Multiplication: f(a, b) = a × b
        Code: return a * b
        """
        result = a * b
        return {
            'operation': OperationType.MULTIPLICATION.value,
            'operand_a': a,
            'operand_b': b,
            'result': result,
            'formula': f'{a} × {b} = {result}',
            'mathematical_formula': 'f(a, b) = a × b',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def divide(a: float, b: float) -> Dict[str, Any]:
        """
        Division: f(a, b) = a / b (b ≠ 0)
        Code: if b == 0 raise error; return a / b
        Mathematical constraint: b ≠ 0 (Division by zero undefined)
        """
        if b == 0:
            raise ValueError("Division by zero is undefined")
        result = a / b
        return {
            'operation': OperationType.DIVISION.value,
            'operand_a': a,
            'operand_b': b,
            'result': result,
            'formula': f'{a} ÷ {b} = {result}',
            'mathematical_formula': 'f(a, b) = a / b, where b ≠ 0',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def power(a: float, b: float) -> Dict[str, Any]:
        """
        Exponentiation: f(a, b) = a^b
        Code: return a ** b or math.pow(a, b)
        Mathematical formula: a^b = e^(b*ln(a))
        """
        result = math.pow(a, b)
        return {
            'operation': OperationType.POWER.value,
            'operand_a': a,
            'operand_b': b,
            'result': result,
            'formula': f'{a}^{b} = {result}',
            'mathematical_formula': 'f(a, b) = a^b = e^(b×ln(a))',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def modulo(a: float, b: float) -> Dict[str, Any]:
        """
        Modulo: f(a, b) = a mod b
        Code: return a % b
        Mathematical formula: a mod b = a - b×⌊a/b⌋
        """
        if b == 0:
            raise ValueError("Modulo by zero is undefined")
        result = a % b
        return {
            'operation': OperationType.MODULO.value,
            'operand_a': a,
            'operand_b': b,
            'result': result,
            'formula': f'{a} mod {b} = {result}',
            'mathematical_formula': 'f(a, b) = a mod b = a - b×⌊a/b⌋',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def square_root(x: float) -> Dict[str, Any]:
        """
        Square Root: f(x) = √x = x^(1/2)
        Code: return math.sqrt(x)
        Mathematical constraint: x ≥ 0 (for real numbers)
        """
        if x < 0:
            raise ValueError("Square root of negative number is undefined in reals")
        result = math.sqrt(x)
        return {
            'operation': OperationType.SQUARE_ROOT.value,
            'operand_a': x,
            'result': result,
            'formula': f'√{x} = {result}',
            'mathematical_formula': 'f(x) = √x = x^(1/2), where x ≥ 0',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def factorial(n: int) -> Dict[str, Any]:
        """
        Factorial: f(n) = n! = n × (n-1) × ... × 1
        Code: return math.factorial(n)
        Mathematical constraint: n ∈ ℕ₀ (non-negative integers)
        Property: 0! = 1
        """
        if n < 0 or n != int(n):
            raise ValueError("Factorial requires non-negative integer")
        result = math.factorial(int(n))
        return {
            'operation': OperationType.FACTORIAL.value,
            'operand_a': n,
            'result': result,
            'formula': f'{int(n)}! = {result}',
            'mathematical_formula': 'f(n) = n! = n×(n-1)×...×1, where n ∈ ℕ₀',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def sine(theta: float) -> Dict[str, Any]:
        """
        Sine: f(θ) = sin(θ)
        Code: return math.sin(theta)
        Input: theta in radians
        Range: [-1, 1]
        """
        result = math.sin(theta)
        return {
            'operation': OperationType.SINE.value,
            'operand_a': theta,
            'result': result,
            'formula': f'sin({theta}) = {result}',
            'mathematical_formula': 'f(θ) = sin(θ), θ ∈ radians, result ∈ [-1, 1]',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def cosine(theta: float) -> Dict[str, Any]:
        """
        Cosine: f(θ) = cos(θ)
        Code: return math.cos(theta)
        Input: theta in radians
        Range: [-1, 1]
        """
        result = math.cos(theta)
        return {
            'operation': OperationType.COSINE.value,
            'operand_a': theta,
            'result': result,
            'formula': f'cos({theta}) = {result}',
            'mathematical_formula': 'f(θ) = cos(θ), θ ∈ radians, result ∈ [-1, 1]',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def tangent(theta: float) -> Dict[str, Any]:
        """
        Tangent: f(θ) = tan(θ) = sin(θ)/cos(θ)
        Code: return math.tan(theta)
        Input: theta in radians
        Note: undefined when cos(θ) = 0
        """
        result = math.tan(theta)
        return {
            'operation': OperationType.TANGENT.value,
            'operand_a': theta,
            'result': result,
            'formula': f'tan({theta}) = {result}',
            'mathematical_formula': 'f(θ) = tan(θ) = sin(θ)/cos(θ), θ ∈ radians',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def logarithm(x: float, base: float = 10) -> Dict[str, Any]:
        """
        Logarithm: f(x) = log_b(x)
        Code: return math.log(x, base)
        Mathematical formula: log_b(x) = ln(x) / ln(b)
        Constraint: x > 0, base > 0, base ≠ 1
        """
        if x <= 0:
            raise ValueError("Logarithm of non-positive number is undefined")
        if base <= 0 or base == 1:
            raise ValueError("Log base must be > 0 and ≠ 1")
        result = math.log(x, base)
        return {
            'operation': OperationType.LOGARITHM.value,
            'operand_a': x,
            'operand_b': base,
            'result': result,
            'formula': f'log_{base}({x}) = {result}',
            'mathematical_formula': f'f(x) = log_b(x) = ln(x)/ln(b), x > 0, b > 0, b ≠ 1',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def natural_log(x: float) -> Dict[str, Any]:
        """
        Natural Logarithm: f(x) = ln(x) = log_e(x)
        Code: return math.log(x)
        Mathematical formula: ln(x) = ∫(1/t)dt from 1 to x
        Constraint: x > 0
        """
        if x <= 0:
            raise ValueError("Natural logarithm of non-positive number is undefined")
        result = math.log(x)
        return {
            'operation': OperationType.NATURAL_LOG.value,
            'operand_a': x,
            'result': result,
            'formula': f'ln({x}) = {result}',
            'mathematical_formula': 'f(x) = ln(x) = log_e(x), where x > 0',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def absolute(x: float) -> Dict[str, Any]:
        """
        Absolute Value: f(x) = |x|
        Code: return abs(x)
        Mathematical formula: |x| = { x if x ≥ 0; -x if x < 0 }
        Property: |x| ≥ 0 for all x ∈ ℝ
        """
        result = abs(x)
        return {
            'operation': OperationType.ABSOLUTE.value,
            'operand_a': x,
            'result': result,
            'formula': f'|{x}| = {result}',
            'mathematical_formula': 'f(x) = |x|, result ∈ ℝ₀⁺',
            'timestamp': datetime.now().isoformat()
        }


calculator = ScientificCalculator()


@app.route('/api/health', methods=['GET'])
def health_check():
    logger.info('Health check requested')
    return jsonify({
        'status': 'healthy',
        'service': 'Scientific Calculator API v2.0',
        'timestamp': datetime.now().isoformat(),
        'operations': [op.value for op in OperationType]
    }), 200


# Binary Operations (two operands)
@app.route('/api/add', methods=['POST'])
def add_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        a = data.get('a')
        b = data.get('b')
        
        is_valid, error_msg = calculator.validate_input(a, b)
        if not is_valid:
            logger.warning(f'Invalid input: a={a}, b={b}')
            return jsonify({'error': error_msg}), 400
        
        result = calculator.add(float(a), float(b))
        logger.info(f'Addition: {a} + {b} = {result["result"]}')
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/subtract', methods=['POST'])
def subtract_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        a = data.get('a')
        b = data.get('b')
        
        is_valid, error_msg = calculator.validate_input(a, b)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.subtract(float(a), float(b))
        logger.info(f'Subtraction: {a} - {b} = {result["result"]}')
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/multiply', methods=['POST'])
def multiply_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        a = data.get('a')
        b = data.get('b')
        
        is_valid, error_msg = calculator.validate_input(a, b)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.multiply(float(a), float(b))
        logger.info(f'Multiplication: {a} * {b} = {result["result"]}')
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/divide', methods=['POST'])
def divide_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        a = data.get('a')
        b = data.get('b')
        
        is_valid, error_msg = calculator.validate_input(a, b)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.divide(float(a), float(b))
        logger.info(f'Division: {a} / {b} = {result["result"]}')
        return jsonify(result), 200
    except ValueError as e:
        logger.warning(f'Division error: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/power', methods=['POST'])
def power_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        a = data.get('a')
        b = data.get('b')
        
        is_valid, error_msg = calculator.validate_input(a, b)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.power(float(a), float(b))
        logger.info(f'Power: {a}^{b} = {result["result"]}')
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/modulo', methods=['POST'])
def modulo_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        a = data.get('a')
        b = data.get('b')
        
        is_valid, error_msg = calculator.validate_input(a, b)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.modulo(float(a), float(b))
        logger.info(f'Modulo: {a} mod {b} = {result["result"]}')
        return jsonify(result), 200
    except ValueError as e:
        logger.warning(f'Modulo error: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


# Unary Operations (one operand)
@app.route('/api/sqrt', methods=['POST'])
def sqrt_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        x = data.get('x')
        
        is_valid, error_msg = calculator.validate_input(x)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.square_root(float(x))
        logger.info(f'Square Root: √{x} = {result["result"]}')
        return jsonify(result), 200
    except ValueError as e:
        logger.warning(f'Sqrt error: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/factorial', methods=['POST'])
def factorial_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        n = data.get('n')
        
        is_valid, error_msg = calculator.validate_input(n)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.factorial(float(n))
        logger.info(f'Factorial: {n}! = {result["result"]}')
        return jsonify(result), 200
    except ValueError as e:
        logger.warning(f'Factorial error: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/sin', methods=['POST'])
def sin_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        theta = data.get('theta')
        
        is_valid, error_msg = calculator.validate_input(theta)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.sine(float(theta))
        logger.info(f'Sine: sin({theta}) = {result["result"]}')
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/cos', methods=['POST'])
def cos_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        theta = data.get('theta')
        
        is_valid, error_msg = calculator.validate_input(theta)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.cosine(float(theta))
        logger.info(f'Cosine: cos({theta}) = {result["result"]}')
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/tan', methods=['POST'])
def tan_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        theta = data.get('theta')
        
        is_valid, error_msg = calculator.validate_input(theta)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.tangent(float(theta))
        logger.info(f'Tangent: tan({theta}) = {result["result"]}')
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/log', methods=['POST'])
def log_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        x = data.get('x')
        base = data.get('base', 10)
        
        is_valid, error_msg = calculator.validate_input(x, base)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.logarithm(float(x), float(base))
        logger.info(f'Logarithm: log_{base}({x}) = {result["result"]}')
        return jsonify(result), 200
    except ValueError as e:
        logger.warning(f'Log error: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/ln', methods=['POST'])
def ln_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        x = data.get('x')
        
        is_valid, error_msg = calculator.validate_input(x)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.natural_log(float(x))
        logger.info(f'Natural Log: ln({x}) = {result["result"]}')
        return jsonify(result), 200
    except ValueError as e:
        logger.warning(f'Ln error: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/abs', methods=['POST'])
def abs_operation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must contain JSON'}), 400
        
        x = data.get('x')
        
        is_valid, error_msg = calculator.validate_input(x)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        result = calculator.absolute(float(x))
        logger.info(f'Absolute: |{x}| = {result["result"]}')
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    logger.info('Starting Scientific Calculator Backend Server...')
    app.run(debug=True, host='0.0.0.0', port=5000)
