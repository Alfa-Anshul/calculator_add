const { useState, useEffect } = React;

const API = "";

function App() {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchState = async () => {
    const res = await fetch(`${API}/state`);
    const data = await res.json();
    setState(data);
  };

  const makeMove = async (index) => {
    if (!state || state.game_over || state.board[index] !== "") return;
    setLoading(true);
    const res = await fetch(`${API}/move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ index })
    });
    const data = await res.json();
    setState(data);
    setLoading(false);
  };

  const startGame = async () => {
    const res = await fetch(`${API}/start`, { method: "POST" });
    const data = await res.json();
    setState(data);
  };

  useEffect(() => { fetchState(); }, []);

  if (!state) return <div className="loading">Loading...</div>;

  const statusMsg = state.game_over
    ? state.winner === "draw" ? "🤝 It's a Draw!" : `🏆 Player ${state.winner} Wins!`
    : `Player ${state.current_player}'s Turn`;

  return (
    <div className="container">
      <h1>Tic-Tac-Toe</h1>
      <div className="scores">
        <span>X: {state.scores.X}</span>
        <span>Draws: {state.scores.draws}</span>
        <span>O: {state.scores.O}</span>
      </div>
      <div className={`status ${state.game_over ? 'game-over' : ''}`}>{statusMsg}</div>
      <div className="board">
        {state.board.map((cell, i) => (
          <button
            key={i}
            className={`cell ${cell.toLowerCase()} ${state.game_over ? 'disabled' : ''}`}
            onClick={() => makeMove(i)}
            disabled={loading || state.game_over || cell !== ""}
          >
            {cell}
          </button>
        ))}
      </div>
      <button className="restart-btn" onClick={startGame}>New Game</button>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
