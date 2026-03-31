const API = "";

function Cell({ value, onClick, disabled }) {
  return (
    <button
      className={`cell ${value === 'X' ? 'cell-x' : value === 'O' ? 'cell-o' : ''}`}
      onClick={onClick}
      disabled={disabled || value !== ''}
    >
      {value}
    </button>
  );
}

function App() {
  const [state, setState] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const fetchState = async () => {
    const res = await fetch(`${API}/state`);
    const data = await res.json();
    setState(data);
  };

  const startGame = async () => {
    setLoading(true);
    const res = await fetch(`${API}/start`, { method: 'POST' });
    const data = await res.json();
    setState(data);
    setLoading(false);
  };

  const makeMove = async (index) => {
    if (!state || state.winner || state.draw) return;
    const res = await fetch(`${API}/move`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ index })
    });
    const data = await res.json();
    setState(data);
  };

  React.useEffect(() => { fetchState(); }, []);

  const status = !state ? 'Loading...'
    : state.winner ? `🏆 Player ${state.winner} wins!`
    : state.draw ? "🤝 It's a draw!"
    : `Player ${state.current_player}'s turn`;

  return (
    <div className="app">
      <h1>Tic-Tac-Toe</h1>
      <div className="scores">
        <span className="score-x">X: {state?.scores?.X ?? 0}</span>
        <span className="score-o">O: {state?.scores?.O ?? 0}</span>
      </div>
      <div className="status">{status}</div>
      <div className="board">
        {(state?.board ?? Array(9).fill('')).map((val, i) => (
          <Cell
            key={i}
            value={val}
            onClick={() => makeMove(i)}
            disabled={!!state?.winner || !!state?.draw || loading}
          />
        ))}
      </div>
      <button className="btn-new" onClick={startGame} disabled={loading}>
        {loading ? 'Starting...' : 'New Game'}
      </button>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
