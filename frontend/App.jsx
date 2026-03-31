const API = '';

function App() {
  const [state, setState] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const fetchState = async () => {
    const res = await fetch(`${API}/state`);
    const data = await res.json();
    setState(data);
  };

  React.useEffect(() => { fetchState(); }, []);

  const handleMove = async (index) => {
    if (!state || state.game_over || state.board[index] !== '') return;
    setLoading(true);
    const res = await fetch(`${API}/move`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ index }),
    });
    const data = await res.json();
    setState(data);
    setLoading(false);
  };

  const handleRestart = async () => {
    const res = await fetch(`${API}/start`, { method: 'POST' });
    const data = await res.json();
    setState(data);
  };

  if (!state) return <div className="loading">Loading...</div>;

  const { board, current_player, winner, game_over, scores } = state;

  let statusMsg = '';
  if (winner === 'draw') statusMsg = "It's a Draw!";
  else if (winner) statusMsg = `Player ${winner} Wins! 🎉`;
  else statusMsg = `Player ${current_player}'s Turn`;

  return (
    <div className="app">
      <header>
        <h1><span className="bracket">[</span> TIC-TAC-TOE <span className="bracket">]</span></h1>
      </header>

      <div className="scoreboard">
        <div className="score-item"><span className="label">X</span><span className="value x-color">{scores.X}</span></div>
        <div className="score-item"><span className="label">DRAWS</span><span className="value">{scores.draws}</span></div>
        <div className="score-item"><span className="label">O</span><span className="value o-color">{scores.O}</span></div>
      </div>

      <div className={`status ${winner === 'draw' ? 'draw' : winner ? 'win' : ''}`}>{statusMsg}</div>

      <div className="board">
        {board.map((cell, i) => (
          <button
            key={i}
            className={`cell ${cell === 'X' ? 'x-cell' : cell === 'O' ? 'o-cell' : ''} ${game_over ? 'disabled' : ''}`}
            onClick={() => handleMove(i)}
            disabled={loading || game_over || cell !== ''}
          >
            {cell}
          </button>
        ))}
      </div>

      {game_over && (
        <button className="restart-btn" onClick={handleRestart}>↺ NEW GAME</button>
      )}
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
