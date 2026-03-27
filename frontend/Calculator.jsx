import React, { useState } from 'react';
import './Calculator.css';

const Calculator = () => {
  /*
  State Management:
  - inputA: First operand (a ∈ ℝ)
  - inputB: Second operand (b ∈ ℝ)
  - result: Output of operation f(a, b)
  - loading: Pending API call state
  - error: Error handling state
  */
  const [inputA, setInputA] = useState('');
  const [inputB, setInputB] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastOperation, setLastOperation] = useState('');

  // API Base URL
  const API_URL = 'http://localhost:5000';

  /**
   * Perform operation via API
   * Mathematical formula: result = f(a, b) where f is operation function
   * For addition: f(a, b) = a + b
   * For subtraction: f(a, b) = a - b = a + (-b)
   */
  const performOperation = async (operation) => {
    // Input validation
    if (!inputA || !inputB) {
      setError('Please enter both numbers');
      return;
    }

    const a = parseFloat(inputA);
    const b = parseFloat(inputB);

    if (isNaN(a) || isNaN(b)) {
      setError('Invalid number format');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const endpoint = operation === 'add' ? '/add' : '/subtract';
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          a: a,
          b: b,
        }),
      });

      if (!response.ok) {
        throw new Error('API request failed');
      }

      const data = await response.json();
      setResult(data);
      setLastOperation(operation);
    } catch (err) {
      setError('Failed to connect to backend: ' + err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  // Clear all states
  const clearCalculator = () => {
    setInputA('');
    setInputB('');
    setResult(null);
    setError(null);
    setLastOperation('');
  };

  return (
    <div className="calculator-container">
      <div className="calculator">
        <h1>Simple Calculator</h1>
        <p className="subtitle">Addition & Subtraction Operations</p>

        {/* Input Section */}
        <div className="input-section">
          <div className="input-group">
            <label htmlFor="inputA">Operand A (a):</label>
            <input
              id="inputA"
              type="number"
              step="0.01"
              value={inputA}
              onChange={(e) => setInputA(e.target.value)}
              placeholder="Enter first number"
              disabled={loading}
            />
          </div>

          <div className="input-group">
            <label htmlFor="inputB">Operand B (b):</label>
            <input
              id="inputB"
              type="number"
              step="0.01"
              value={inputB}
              onChange={(e) => setInputB(e.target.value)}
              placeholder="Enter second number"
              disabled={loading}
            />
          </div>
        </div>

        {/* Operation Buttons */}
        <div className="button-section">
          <button
            className="btn btn-add"
            onClick={() => performOperation('add')}
            disabled={loading}
          >
            {loading && lastOperation === 'add' ? 'Calculating...' : 'Add (a + b)'}
          </button>
          <button
            className="btn btn-subtract"
            onClick={() => performOperation('subtract')}
            disabled={loading}
          >
            {loading && lastOperation === 'subtract' ? 'Calculating...' : 'Subtract (a - b)'}
          </button>
          <button
            className="btn btn-clear"
            onClick={clearCalculator}
            disabled={loading}
          >
            Clear
          </button>
        </div>

        {/* Error Display */}
        {error && <div className="error-message">{error}</div>}

        {/* Result Display */}
        {result && (
          <div className="result-section">
            <h2>Result</h2>
            <div className="result-formula">
              {result.formula}
            </div>
            <div className="result-value">
              <span className="label">f(a, b) =</span>
              <span className="value">{result.result}</span>
            </div>
            <div className="result-details">
              <p>Operation: {result.operation.toUpperCase()}</p>
              <p>a = {result.operand_a}, b = {result.operand_b}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Calculator;
