const { useState, useEffect, useCallback } = React;

const GRID_SIZE = 20;
const CELL_SIZE = 24;
const API = "";

function SnakeGame() {
  const [state, setState] = useState(null);
  const [started, setStarted] = useState(false);

  const fetchState = async () => {
    const res = await fetch(`${API}/state`);
    const data = await res.json();
    setState(data);
  };

  const startGame = async () => {
    const res = await fetch(`${API}/start`, { method: "POST" });
    const data = await res.json();
    setState(data);
    setStarted(true);
  };

  const move = useCallback(async (dir) => {
    if (!started || state?.game_over) return;
    const res = await fetch(`${API}/move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ direction: dir }),
    });
    const data = await res.json();
    setState(data);
  }, [started, state]);

  useEffect(() => {
    const handler = (e) => {
      const map = { ArrowUp: "UP", ArrowDown: "DOWN", ArrowLeft: "LEFT", ArrowRight: "RIGHT" };
      if (map[e.key]) move(map[e.key]);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [move]);

  useEffect(() => {
    if (!started || state?.game_over) return;
    const interval = setInterval(() => {
      move(state?.direction || "RIGHT");
    }, 200);
    return () => clearInterval(interval);
  }, [started, state?.direction, state?.game_over, move]);

  const renderGrid = () => {
    if (!state) return null;
    const snakeSet = new Set(state.snake.map(([r, c]) => `${r},${c}`));
    const [fr, fc] = state.food;
    const cells = [];
    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        const key = `${r},${c}`;
        let cls = "cell";
        if (snakeSet.has(key)) cls += state.snake[0][0] === r && state.snake[0][1] === c ? " head" : " body";
        else if (r === fr && c === fc) cls += " food";
        cells.push(<div key={key} className={cls} />);
      }
    }
    return cells;
  };

  return (
    <div className="container">
      <h1>🐍 Snake Game</h1>
      <div className="score">Score: {state?.score ?? 0}</div>
      {state?.game_over && <div className="game-over">💀 GAME OVER</div>}
      <div className="grid" style={{ gridTemplateColumns: `repeat(${GRID_SIZE}, ${CELL_SIZE}px)` }}>
        {renderGrid()}
      </div>
      <div className="controls">
        <div><button onClick={() => move("UP")}>▲</button></div>
        <div>
          <button onClick={() => move("LEFT")}>◀</button>
          <button onClick={() => move("DOWN")}>▼</button>
          <button onClick={() => move("RIGHT")}>▶</button>
        </div>
      </div>
      <button className="start-btn" onClick={startGame}>
        {started ? "🔄 Restart" : "▶ Start Game"}
      </button>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<SnakeGame />);
