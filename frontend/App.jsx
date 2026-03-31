const API = '';

function Cell({ value, onClick, isWinning }) {
  return (
    <button
      className={`cell ${value === 'X' ? 'cell-x' : value === 'O' ? 'cell-o' : ''} ${isWinning ? 'cell-win' : ''}`}
      onClick={onClick}
    >
      {value}
    </button>
  );
}

function Board() {
  const [state, setState] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [winCells, setWinCells] = React.useState([]);

  const WINNING_COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
  ];

  function findWinCells(board) {
    for (const combo of WINNING_COMBOS) {
      const [a,b,c] = combo;
      if (board[a] && board[a] === board[b] && board[a] === board[c]) return combo;
    }
    return [];
  }

  async function fetchState() {
    const res = await fetch(`${API}/state`);
    const data = await res.json();
    setState(data);
    setWinCells(findWinCells(data.board));
  }

  async function makeMove(idx) {
    if (loading || !state || state.game_over || state.board[idx]) return;
    setLoading(true);
    const res = await fetch(`${API}/move`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ index: idx })
    });
    const data = await res.json();
    setState(data);
    setWinCells(findWinCells(data.board));
    setLoading(false);
  }

  async function resetGame() {
    const res = await fetch(`${API}/reset`, { method: 'POST' });
    const data = await res.json();
    setState(data);
    setWinCells([]);
  }

  React.useEffect(() => { fetchState(); }, []);

  if (!state) return <div className="loading">Loading game...</div>;

  const statusMsg = state.game_over
    ? state.winner === 'Draw' ? "It's a Draw! 🤝" : `Player ${state.winner} Wins! 🎉`
    : `Player ${state.current_player}'s Turn`;

  return (
    <div className="container">
      <h1 className="title">Tic-Tac-Toe</h1>
      <div className="scoreboard">
        <div className="score score-x">X: {state.scores.X}</div>
        <div className="score score-draw">Draws: {state.scores.draws}</div>
        <div className="score score-o">O: {state.scores.O}</div>
      </div>
      <div className={`status ${state.game_over ? 'status-over' : ''}`}>{statusMsg}</div>
      <div className="board">
        {state.board.map((cell, i) => (
          <Cell
            key={i}
            value={cell}
            isWinning={winCells.includes(i)}
            onClick={() => makeMove(i)}
          />
        ))}
      </div>
      <button className="reset-btn" onClick={resetGame}>New Game</button>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Board />);
