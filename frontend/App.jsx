const { useState, useEffect, useCallback } = React;

const GRID_SIZE = 20;
const CELL_SIZE = 24;
const API = "";

function App() {
  const [state, setState] = useState(null);
  const [started, setStarted] = useState(false);
  const [loading, setLoading] = useState(false);

  const fetchState = async () => {
    const res = await fetch(`${API}/state`);
    const data = await res.json();
    setState(data.state);
  };

  const startGame = async () => {
    setLoading(true);
    const res = await fetch(`${API}/start`, { method: "POST" });
    const data = await res.json();
    setState(data.state);
    setStarted(true);
    setLoading(false);
  };

  const move = useCallback(async (dir) => {
    if (!started || state?.game_over) return;
    const res = await fetch(`${API}/move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ direction: dir }),
    });
    const data = await res.json();
    setState(data.state);
  }, [started, state]);

  useEffect(() => {
    const handler = (e) => {
      const map = { ArrowUp: "UP", ArrowDown: "DOWN", ArrowLeft: "LEFT", ArrowRight: "RIGHT" };
      if (map[e.key]) { e.preventDefault(); move(map[e.key]); }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [move]);

  useEffect(() => {
    if (!started || state?.game_over) return;
    const interval = setInterval(() => {
      fetch(`${API}/move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ direction: state?.direction || "RIGHT" }),
      }).then(r => r.json()).then(d => setState(d.state));
    }, 200);
    return () => clearInterval(interval);
  }, [started, state?.game_over, state?.direction]);

  const snakeSet = new Set((state?.snake || []).map(([r, c]) => `${r},${c}`));
  const isHead = state?.snake?.[0];
  const food = state?.food;

  return (
    <div className="container">
      <h1>🐍 Snake Game</h1>
      <div className="score-bar">
        <span>Score: <strong>{state?.score ?? 0}</strong></span>
        {state?.game_over && <span className="game-over">GAME OVER!</span>}
      </div>

      <div className="board" style={{ width: GRID_SIZE * CELL_SIZE, height: GRID_SIZE * CELL_SIZE }}>
        {Array.from({ length: GRID_SIZE }).map((_, row) =>
          Array.from({ length: GRID_SIZE }).map((_, col) => {
            const key = `${row},${col}`;
            const isSnake = snakeSet.has(key);
            const isHeadCell = isHead && isHead[0] === row && isHead[1] === col;
            const isFood = food && food[0] === row && food[1] === col;
            return (
              <div
                key={key}
                className={`cell ${isHeadCell ? 'head' : isSnake ? 'snake' : ''} ${isFood ? 'food' : ''}`}
                style={{ width: CELL_SIZE, height: CELL_SIZE, left: col * CELL_SIZE, top: row * CELL_SIZE }}
              />
            );
          })
        )}
      </div>

      <div className="controls">
        <div className="row"><button onClick={() => move("UP")}>▲ Up</button></div>
        <div className="row">
          <button onClick={() => move("LEFT")}>◀ Left</button>
          <button onClick={() => move("DOWN")}>▼ Down</button>
          <button onClick={() => move("RIGHT")}>Right ▶</button>
        </div>
      </div>

      <button className="start-btn" onClick={startGame} disabled={loading}>
        {loading ? "Starting..." : started ? "Restart" : "Start Game"}
      </button>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
