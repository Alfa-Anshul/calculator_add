import React, { useState, useEffect } from 'react';
import './Calculator.css';

const Calculator = () => {
  /*
  State Management - Mathematical Variable Space:
  
  State Vector S = (inputA, inputB, result, loading, error, history)
  
  Where:
  - inputA: First operand (a ∈ ℝ) - First real number
  - inputB: Second operand (b ∈ ℝ) - Second real number  
  - result: Output of operation f(a, b) ∈ ℝ
  - loading: Boolean flag for async state
  - error: Error message string
  - history: List of all computations
  */
  const [inputA, setInputA] = useState('');
  const [inputB, setInputB] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastOperation, setLastOperation] = useState('');
  const [history, setHistory] = useState([]);
  const [backendStatus, setBackendStatus] = useState('disconnected');

  // API Configuration
  const API_URL = 'http://localhost:5000/api';

  /**
   * Check backend health on component mount
   * 
   * Purpose: Verify backend server is running before operations
   * HTTP Method: GET
   * Endpoint: /api/health
   */
  useEffect(() => {
    checkBackendHealth();
    const healthCheckInterval = setInterval(checkBackendHealth, 30000); // Every 30s
    return () => clearInterval(healthCheckInterval);
  }, []);

  const checkBackendHealth = async () => {
    try {
      const response = await fetch(`${API_URL}/health`);
      if (response.ok) {
        setBackendStatus('connected');
      } else {
        setBackendStatus('disconnected');
      }
    } catch (err) {
      setBackendStatus('disconnected');
    }
  };

  /**
   * Perform mathematical operation via API
   * 
   * Mathematical Formula:
   * For Addition: f(a, b) = a + b
   * For Subtraction: f(a, b) = a - b = a + (-b)
   * 
   * HTTP Contract:
   * Method: POST
   * Headers: Content-Type: application/json
   * Body: {"a": float, "b": float}
   * 
   * Code Flow:
   * 1. Validate inputs (a, b ∈ ℝ)
   * 2. Send POST request with operands
   * 3. Receive result = f(a, b)
   * 4. Update state and history
   */
  const performOperation = async (operation) => {
    // Input Validation: Check if inputs are non-empty
    if (!inputA || !inputB) {
      setError('❌ Please enter both operands (a and b)');
      return;
    }

    // Type Conversion & Validation: String → Float
    const a = parseFloat(inputA);
    const b = parseFloat(inputB);

    // Mathematical Constraint Check: a, b ∈ ℝ (Real numbers)
    if (isNaN(a) || isNaN(b)) {
      setError('❌ Invalid number format. Use integers or decimals.');
      return;
    }

    // Set loading state during async operation
    setLoading(true);
    setError(null);

    try {
      // Determine endpoint based on operation
      const endpoint = operation === 'add' ? '/add' : '/subtract';
      
      // Execute HTTP POST request
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

      // Handle HTTP response status
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'API request failed');
      }

      // Parse JSON response
      const data = await response.json();
      
      // Update result state
      setResult(data);
      setLastOperation(operation);
      
      // Add to calculation history
      setHistory([...history, data]);
    } catch (err) {
      // Error handling
      setError('❌ Backend Error: ' + err.message);
      setResult(null);
    } finally {
      // Always clear loading state
      setLoading(false);
    }
  };

  /**
   * Clear all calculator states
   * Reset: S = (empty, empty, null, false, null, [])
   */
  const clearCalculator = () => {
    setInputA('');
    setInputB('');
    setResult(null);
    setError(null);
    setLastOperation('');
  };

  /**
   * Clear calculation history
   */
  const clearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="calculator-container">
      {/* Backend Status Indicator */}
      <div className={`status-indicator status-${backendStatus}`}>
        <span className="status-dot"></span>
        <span className="status-text">
          {backendStatus === 'connected' ? '✓ Backend Connected' : '✗ Backend Disconnected'}
        </span>
      </div>

      <div className="calculator">
        <div className="header">
          <h1>🧮 Calculator</h1>
          <p className="subtitle">Addition & Subtraction Engine</p>
        </div>

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
              onKeyPress={(e) => {
                if (e.key === 'Enter') performOperation('add');
              }}
              placeholder="Enter first number"
              disabled={loading || backendStatus === 'disconnected'}
              className="input-field"
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
              onKeyPress={(e) => {
                if (e.key === 'Enter') performOperation('subtract');
              }}
              placeholder="Enter second number"
              disabled={loading || backendStatus === 'disconnected'}
              className="input-field"
            />
          </div>
        </div>

        {/* Operation Buttons */}
        <div className="button-section">
          <button
            className="btn btn-add"
            onClick={() => performOperation('add')}
            disabled={loading || backendStatus === 'disconnected'}
            title="Addition: a + b"
          >
            {loading && lastOperation === 'add' ? '⏳ Computing...' : '➕ Add (a + b)'}
          </button>
          <button
            className="btn btn-subtract"
            onClick={() => performOperation('subtract')}
            disabled={loading || backendStatus === 'disconnected'}
            title="Subtraction: a - b"
          >
            {loading && lastOperation === 'subtract' ? '⏳ Computing...' : '➖ Subtract (a - b)'}
          </button>
          <button
            className="btn btn-clear"
            onClick={clearCalculator}
            disabled={loading}
            title="Clear current inputs"
          >
            🔄 Clear
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        {/* Result Display */}
        {result && (
          <div className="result-section">
            <h2>📊 Result</h2>
            
            {/* Mathematical Formula */}
            <div className="result-formula">
              <code>{result.formula}</code>
            </div>

            {/* Result Value with Math Notation */}
            <div className="result-value">
              <span className="label">f(a, b) =</span>
              <span className="value">{result.result}</span>
            </div>

            {/* Mathematical Details */}
            <div className="result-details">
              <p><strong>Operation:</strong> {result.operation.toUpperCase()}</p>
              <p><strong>Formula:</strong> {result.mathematical_formula}</p>
              <p><strong>Operands:</strong> a = {result.operand_a}, b = {result.operand_b}</p>
              <p><strong>Timestamp:</strong> {new Date(result.timestamp).toLocaleString()}</p>
            </div>
          </div>
        )}

        {/* History Section */}
        {history.length > 0 && (
          <div className="history-section">
            <div className="history-header">
              <h3>📜 Calculation History</h3>
              <button
                className="btn-mini btn-clear-history"
                onClick={clearHistory}
                disabled={loading}
              >
                Clear
              </button>
            </div>
            <div className="history-list">
              {history.map((item, idx) => (
                <div key={idx} className="history-item">
                  <span className="history-index">{idx + 1}.</span>
                  <span className="history-formula">{item.formula}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Calculator;
