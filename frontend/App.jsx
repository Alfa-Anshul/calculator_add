const { useState, useEffect, useCallback } = React;

const API = '/api';

function Cell({ value, index, onClick, isWinner, disabled }) {
  return (
    <button
      className={`cell ${value ? value.toLowerCase() : ''} ${isWinner ? 'winner' : ''} ${!value && !disabled ? 'hoverable' : ''}`}
      onClick={() => onClick(index)}
      disabled={disabled || !!value}
      aria-label={`Cell ${index}`}
    >
      <span className="cell-content">{value}</span>
      {!value && !disabled && <span className="cell-ghost"></span>}
    </button>
  );
}

function ScoreBoard({ scores }) {
  return (
    <div className="scoreboard">
      <div className="score-item x-score">
        <span className="score-label">X</span>
        <span className="score-value">{scores.X}</span>
      </div>
      <div className="score-item draw-score">
        <span className="score-label">DRAW</span>
        <span className="score-value">{scores.draws}</span>
      </div>
      <div className="score-item o-score">
        <span className="score-label">O</span>
        <span className="score-value">{scores.O}</span>
      </div>
    </div>
  );
}

function App() {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [animating, setAnimating] = useState(false);

  const fetchState = useCallback(async () => {
    try {
      const res = await fetch(`${API}/state`);
      const data = await res.json();
      setState(data);
    } catch (e) {
      setError('Cannot connect to server');
    }
  }, []);

  const makeMove = async (index) => {
    if (!state || state.game_over || state.board[index] !== '' || loading) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/move`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ index })
      });
      const data = await res.json();
      setState(data);
      if (data.game_over) setAnimating(true);
    } catch (e) {
      setError('Move failed');
    }
    setLoading(false);
  };

  const startGame = async () => {
    setAnimating(false);
    try {
      const res = await fetch(`${API}/start`, { method: 'POST' });
      const data = await res.json();
      setState(data);
    } catch (e) {
      setError('Could not start game');
    }
  };

  useEffect(() => { fetchState(); }, [fetchState]);

  if (error) return (
    <div className="error-screen">
      <div className="error-box">
        <h2>⚠ Connection Error</h2>
        <p>{error}</p>
        <button onClick={() => { setError(null); fetchState(); }}>Retry</button>
      </div>
    </div>
  );

  if (!state) return (
    <div className="loading-screen">
      <div className="spinner"></div>
      <p>Connecting...</p>
    </div>
  );

  const { board, current_player, winner, game_over, winning_combo, scores } = state;

  const statusMsg = game_over
    ? winner === 'draw'
      ? "It's a Draw!"
      : `Player ${winner} Wins!`
    : `Player ${current_player}'s Turn`;

  const statusClass = game_over
    ? winner === 'draw' ? 'draw' : `win-${winner.toLowerCase()}`
    : `turn-${current_player.toLowerCase()}`;

  return (
    <div className="app">
      <div className="bg-grid"></div>
      <div className="container">
        <header>
          <h1 className="title">TIC<span>TAC</span>TOE</h1>
        </header>

        <ScoreBoard scores={scores} />

        <div className={`status-bar ${statusClass}`}>
          <div className="status-indicator"></div>
          <span>{statusMsg}</span>
        </div>

        <div className={`board ${game_over ? 'game-over' : ''} ${animating ? 'result-anim' : ''}`}>
          {board.map((cell, i) => (
            <Cell
              key={i}
              value={cell}
              index={i}
              onClick={makeMove}
              isWinner={winning_combo.includes(i)}
              disabled={game_over || loading}
            />
          ))}
        </div>

        <button className={`btn-new-game ${game_over ? 'pulse' : ''}`} onClick={startGame}>
          {game_over ? '▶ Play Again' : '↺ New Game'}
        </button>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
