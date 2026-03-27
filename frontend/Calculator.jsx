import React, { useState, useEffect } from 'react';
import './Calculator.css';

const Calculator = () => {
  const [mode, setMode] = useState('basic');
  const [inputA, setInputA] = useState('');
  const [inputB, setInputB] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [backendStatus, setBackendStatus] = useState('disconnected');

  const API_URL = 'http://localhost:5000/api';

  useEffect(() => {
    checkBackendHealth();
    const healthCheckInterval = setInterval(checkBackendHealth, 30000);
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

  const performBinaryOperation = async (operation) => {
    if (!inputA || !inputB) {
      setError('❌ Enter both operands (a and b)');
      return;
    }

    const a = parseFloat(inputA);
    const b = parseFloat(inputB);

    if (isNaN(a) || isNaN(b)) {
      setError('❌ Invalid number format');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/${operation}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ a: a, b: b }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'API request failed');
      }

      const data = await response.json();
      setResult(data);
      setHistory([...history, data]);
    } catch (err) {
      setError('❌ Error: ' + err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const performUnaryOperation = async (operation, value, paramName) => {
    if (!value) {
      setError(`❌ Enter value for ${paramName}`);
      return;
    }

    const num = parseFloat(value);
    if (isNaN(num)) {
      setError('❌ Invalid number format');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const payload = { [paramName]: num };
      const response = await fetch(`${API_URL}/${operation}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'API request failed');
      }

      const data = await response.json();
      setResult(data);
      setHistory([...history, data]);
    } catch (err) {
      setError('❌ Error: ' + err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const clearCalculator = () => {
    setInputA('');
    setInputB('');
    setResult(null);
    setError(null);
  };

  const clearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="calculator-container">
      <div className={`status-indicator status-${backendStatus}`}>
        <span className="status-dot"></span>
        <span className="status-text">
          {backendStatus === 'connected' ? '✓ Backend Connected' : '✗ Disconnected'}
        </span>
      </div>

      <div className="calculator">
        <div className="header">
          <h1>🧮 Scientific Calculator</h1>
          <div className="mode-toggle">
            <button
              className={`mode-btn ${mode === 'basic' ? 'active' : ''}`}
              onClick={() => setMode('basic')}
            >
              Basic
            </button>
            <button
              className={`mode-btn ${mode === 'scientific' ? 'active' : ''}`}
              onClick={() => setMode('scientific')}
            >
              Scientific
            </button>
          </div>
        </div>

        {mode === 'basic' && (
          <>
            <div className="input-section">
              <div className="input-group">
                <label>Operand A (a):</label>
                <input
                  type="number"
                  step="0.01"
                  value={inputA}
                  onChange={(e) => setInputA(e.target.value)}
                  placeholder="Enter first number"
                  disabled={loading || backendStatus === 'disconnected'}
                />
              </div>
              <div className="input-group">
                <label>Operand B (b):</label>
                <input
                  type="number"
                  step="0.01"
                  value={inputB}
                  onChange={(e) => setInputB(e.target.value)}
                  placeholder="Enter second number"
                  disabled={loading || backendStatus === 'disconnected'}
                />
              </div>
            </div>

            <div className="button-section">
              <button className="btn btn-add" onClick={() => performBinaryOperation('add')} disabled={loading}>
                {loading ? '⏳ Computing...' : '➕ Add (a + b)'}
              </button>
              <button className="btn btn-subtract" onClick={() => performBinaryOperation('subtract')} disabled={loading}>
                {loading ? '⏳ Computing...' : '➖ Subtract (a - b)'}
              </button>
              <button className="btn btn-multiply" onClick={() => performBinaryOperation('multiply')} disabled={loading}>
                {loading ? '⏳ Computing...' : '✕ Multiply (a × b)'}
              </button>
              <button className="btn btn-divide" onClick={() => performBinaryOperation('divide')} disabled={loading}>
                {loading ? '⏳ Computing...' : '÷ Divide (a ÷ b)'}
              </button>
              <button className="btn btn-power" onClick={() => performBinaryOperation('power')} disabled={loading}>
                {loading ? '⏳ Computing...' : '^  Power (a^b)'}
              </button>
              <button className="btn btn-modulo" onClick={() => performBinaryOperation('modulo')} disabled={loading}>
                {loading ? '⏳ Computing...' : 'mod  Modulo (a mod b)'}
              </button>
              <button className="btn btn-clear" onClick={clearCalculator} disabled={loading}>
                🔄 Clear
              </button>
            </div>
          </>
        )}

        {mode === 'scientific' && (
          <>
            <div className="scientific-section">
              <div className="sci-input-group">
                <label>Input Value:</label>
                <input
                  type="number"
                  step="0.01"
                  value={inputA}
                  onChange={(e) => setInputA(e.target.value)}
                  placeholder="Enter value"
                  disabled={loading}
                />
              </div>
            </div>

            <div className="scientific-buttons">
              <div className="button-grid">
                <button className="btn btn-sci" onClick={() => performUnaryOperation('sqrt', inputA, 'x')} disabled={loading}>
                  √ Sqrt
                </button>
                <button className="btn btn-sci" onClick={() => performUnaryOperation('factorial', inputA, 'n')} disabled={loading}>
                  n! Fact
                </button>
                <button className="btn btn-sci" onClick={() => performUnaryOperation('abs', inputA, 'x')} disabled={loading}>
                  |x| Abs
                </button>
                <button className="btn btn-sci" onClick={() => performUnaryOperation('sin', inputA, 'theta')} disabled={loading}>
                  sin θ
                </button>
                <button className="btn btn-sci" onClick={() => performUnaryOperation('cos', inputA, 'theta')} disabled={loading}>
                  cos θ
                </button>
                <button className="btn btn-sci" onClick={() => performUnaryOperation('tan', inputA, 'theta')} disabled={loading}>
                  tan θ
                </button>
                <button className="btn btn-sci" onClick={() => performUnaryOperation('ln', inputA, 'x')} disabled={loading}>
                  ln(x)
                </button>
                <button className="btn btn-sci" onClick={() => performUnaryOperation('log', inputA, 'x')} disabled={loading}>
                  log(x)
                </button>
              </div>
              <button className="btn btn-clear" onClick={clearCalculator} disabled={loading}>
                🔄 Clear
              </button>
            </div>
          </>
        )}

        {error && <div className="error-message" role="alert">{error}</div>}

        {result && (
          <div className="result-section">
            <h2>📊 Result</h2>
            <div className="result-formula">
              <code>{result.formula}</code>
            </div>
            <div className="result-value">
              <span className="label">f(x) =</span>
              <span className="value">{result.result}</span>
            </div>
            <div className="result-details">
              <p><strong>Operation:</strong> {result.operation.toUpperCase()}</p>
              <p><strong>Formula:</strong> {result.mathematical_formula}</p>
              <p><strong>Time:</strong> {new Date(result.timestamp).toLocaleTimeString()}</p>
            </div>
          </div>
        )}

        {history.length > 0 && (
          <div className="history-section">
            <div className="history-header">
              <h3>📝 History</h3>
              <button className="btn-mini" onClick={clearHistory} disabled={loading}>
                Clear
              </button>
            </div>
            <div className="history-list">
              {history.slice(-10).reverse().map((item, idx) => (
                <div key={idx} className="history-item">
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
