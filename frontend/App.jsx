const API = "";

function Cell({ value, onClick, isWinning }) {
  return (
    <button
      className={`cell ${value === "X" ? "cell-x" : value === "O" ? "cell-o" : ""} ${isWinning ? "cell-winning" : ""}`}
      onClick={onClick}
      disabled={!!value}
    >
      {value}
    </button>
  );
}

function Board() {
  const [state, setState] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  const fetchState = async () => {
    try {
      const res = await fetch(`${API}/state`);
      const data = await res.json();
      setState(data);
    } catch (e) {
      setError("Cannot reach server");
    }
  };

  React.useEffect(() => { fetchState(); }, []);

  const startGame = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/start`, { method: "POST" });
      const data = await res.json();
      setState(data.state);
    } catch (e) { setError("Start failed"); }
    setLoading(false);
  };

  const makeMove = async (index) => {
    if (!state || state.game_over || state.board[index]) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index }),
      });
      const data = await res.json();
      if (data.state) setState(data.state);
      if (data.error) setError(data.error);
    } catch (e) { setError("Move failed"); }
    setLoading(false);
  };

  const getStatus = () => {
    if (!state) return "Loading...";
    if (state.winner === "Draw") return "🤝 It's a Draw!";
    if (state.winner) return `🏆 Player ${state.winner} Wins!`;
    return `Player ${state.current_player}'s Turn`;
  };

  return (
    <div className="app">
      <h1 className="title">⚡ Tic-Tac-Toe</h1>

      {state && (
        <div className="scoreboard">
          <span className="score score-x">X: {state.scores.X}</span>
          <span className="score score-draw">Draw: {state.scores.draws}</span>
          <span className="score score-o">O: {state.scores.O}</span>
        </div>
      )}

      <div className={`status ${state?.winner ? "status-winner" : ""}`}>
        {getStatus()}
      </div>

      {error && <div className="error">{error}</div>}

      <div className="board">
        {state ? state.board.map((cell, i) => (
          <Cell
            key={i}
            value={cell}
            onClick={() => makeMove(i)}
            isWinning={false}
          />
        )) : Array(9).fill(null).map((_, i) => (
          <Cell key={i} value="" onClick={() => {}} />
        ))}
      </div>

      <button
        className={`btn-start ${loading ? "btn-loading" : ""}`}
        onClick={startGame}
        disabled={loading}
      >
        {loading ? "..." : state?.game_over ? "🔁 Play Again" : "🆕 New Game"}
      </button>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Board />);
