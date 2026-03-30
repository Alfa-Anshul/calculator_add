import { useState } from "react";

const API_BASE_URL = "http://localhost:5000/api";

const styles = {
  page: {
    minHeight: "100vh",
    display: "grid",
    placeItems: "center",
    margin: 0,
    padding: "24px",
    background:
      "radial-gradient(circle at top, #20344f 0%, #102033 45%, #08131f 100%)",
    color: "#f7f4ea",
    fontFamily: '"Trebuchet MS", "Segoe UI", sans-serif',
  },
  card: {
    width: "100%",
    maxWidth: "440px",
    padding: "28px",
    borderRadius: "28px",
    background: "rgba(7, 17, 28, 0.88)",
    border: "1px solid rgba(255, 255, 255, 0.12)",
    boxShadow: "0 24px 60px rgba(0, 0, 0, 0.35)",
  },
  eyebrow: {
    margin: "0 0 10px",
    color: "#8ac6ff",
    fontSize: "0.8rem",
    letterSpacing: "0.16em",
    textTransform: "uppercase",
  },
  title: {
    margin: "0 0 12px",
    fontSize: "2.4rem",
    lineHeight: 1,
  },
  subtitle: {
    margin: "0 0 22px",
    color: "#b9c7d6",
    lineHeight: 1.5,
  },
  field: {
    display: "grid",
    gap: "8px",
    marginBottom: "16px",
  },
  label: {
    color: "#d8e4ef",
    fontSize: "0.95rem",
  },
  input: {
    padding: "14px 16px",
    borderRadius: "14px",
    border: "1px solid rgba(255, 255, 255, 0.14)",
    background: "rgba(255, 255, 255, 0.06)",
    color: "#ffffff",
    fontSize: "1rem",
    outline: "none",
  },
  buttons: {
    display: "grid",
    gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
    gap: "12px",
    marginTop: "20px",
  },
  button: {
    padding: "14px 12px",
    border: "none",
    borderRadius: "14px",
    fontSize: "0.98rem",
    fontWeight: 700,
    cursor: "pointer",
  },
  add: {
    background: "#7df0a6",
    color: "#0a2b15",
  },
  subtract: {
    background: "#ffd27d",
    color: "#402300",
  },
  clear: {
    background: "#1f344a",
    color: "#f4f8fb",
  },
  panel: {
    marginTop: "18px",
    padding: "16px",
    borderRadius: "16px",
    background: "rgba(255, 255, 255, 0.06)",
  },
  error: {
    marginTop: "18px",
    padding: "16px",
    borderRadius: "16px",
    background: "rgba(255, 120, 120, 0.14)",
    color: "#ffd7d7",
  },
};

function App() {
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function runOperation(operation) {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/${operation}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ a, b }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Request failed.");
      }

      setResult(data);
    } catch (err) {
      setResult(null);
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function clearCalculator() {
    setA("");
    setB("");
    setResult(null);
    setError("");
  }

  return (
    <main style={styles.page}>
      <section style={styles.card}>
        <p style={styles.eyebrow}>Simple Website</p>
        <h1 style={styles.title}>Calculator</h1>
        <p style={styles.subtitle}>
          A tiny full-stack calculator for addition and subtraction.
        </p>

        <div style={styles.field}>
          <label htmlFor="first-number" style={styles.label}>
            First number
          </label>
          <input
            id="first-number"
            type="number"
            value={a}
            onChange={(event) => setA(event.target.value)}
            placeholder="Enter the first value"
            style={styles.input}
          />
        </div>

        <div style={styles.field}>
          <label htmlFor="second-number" style={styles.label}>
            Second number
          </label>
          <input
            id="second-number"
            type="number"
            value={b}
            onChange={(event) => setB(event.target.value)}
            placeholder="Enter the second value"
            style={styles.input}
          />
        </div>

        <div style={styles.buttons}>
          <button
            type="button"
            style={{ ...styles.button, ...styles.add }}
            onClick={() => runOperation("add")}
            disabled={loading}
          >
            {loading ? "..." : "Add"}
          </button>
          <button
            type="button"
            style={{ ...styles.button, ...styles.subtract }}
            onClick={() => runOperation("subtract")}
            disabled={loading}
          >
            {loading ? "..." : "Subtract"}
          </button>
          <button
            type="button"
            style={{ ...styles.button, ...styles.clear }}
            onClick={clearCalculator}
            disabled={loading}
          >
            Clear
          </button>
        </div>

        {result && (
          <div style={styles.panel}>
            <strong>Result:</strong> {result.result}
            <div style={{ marginTop: "8px", color: "#b9c7d6" }}>{result.formula}</div>
          </div>
        )}

        {error && <div style={styles.error}>{error}</div>}
      </section>
    </main>
  );
}

export default App;
