const { useState, useEffect } = React;

const TicTacToe = () => {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [currentPlayer, setCurrentPlayer] = useState("X");
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);
  const [xScore, setXScore] = useState(0);
  const [oScore, setOScore] = useState(0);
  const [draws, setDraws] = useState(0);
  const [apiUrl, setApiUrl] = useState("");

  // Determine API URL
  useEffect(() => {
    const protocol = window.location.protocol;
    const host = window.location.host;
    setApiUrl(`${protocol}//${host}`);
  }, []);

  // Fetch game state on mount
  useEffect(() => {
    if (apiUrl) {
      fetchGameState();
    }
  }, [apiUrl]);

  const fetchGameState = async () => {
    try {
      const response = await fetch(`${apiUrl}/state`);
      const data = await response.json();
      setBoard(data.board);
      setCurrentPlayer(data.current_player);
      setGameOver(data.game_over);
      setWinner(data.winner);
      setXScore(data.x_score);
      setOScore(data.o_score);
      setDraws(data.draws);
    } catch (error) {
      console.error("Error fetching game state:", error);
    }
  };

  const handleMove = async (position) => {
    if (board[position] !== null || gameOver) {
      return;
    }

    try {
      const response = await fetch(`${apiUrl}/move`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ position }),
      });
      const data = await response.json();

      if (data.game_state) {
        const state = data.game_state;
        setBoard(state.board);
        setCurrentPlayer(state.current_player);
        setGameOver(state.game_over);
        setWinner(state.winner);
        setXScore(state.x_score);
        setOScore(state.o_score);
        setDraws(state.draws);
      }
    } catch (error) {
      console.error("Error making move:", error);
    }
  };

  const handleReset = async () => {
    try {
      const response = await fetch(`${apiUrl}/reset`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();

      if (data.game_state) {
        const state = data.game_state;
        setBoard(state.board);
        setCurrentPlayer(state.current_player);
        setGameOver(state.game_over);
        setWinner(state.winner);
        setXScore(state.x_score);
        setOScore(state.o_score);
        setDraws(state.draws);
      }
    } catch (error) {
      console.error("Error resetting game:", error);
    }
  };

  const handleResetScores = async () => {
    try {
      const response = await fetch(`${apiUrl}/reset-scores`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();

      if (data.game_state) {
        const state = data.game_state;
        setBoard(state.board);
        setCurrentPlayer(state.current_player);
        setGameOver(state.game_over);
        setWinner(state.winner);
        setXScore(state.x_score);
        setOScore(state.o_score);
        setDraws(state.draws);
      }
    } catch (error) {
      console.error("Error resetting scores:", error);
    }
  };

  const renderSquare = (index) => (
    <button
      className="square"
      onClick={() => handleMove(index)}
      disabled={gameOver || board[index] !== null}
    >
      {board[index]}
    </button>
  );

  let status;
  if (gameOver) {
    if (winner) {
      status = `Game Over! Player ${winner} wins!`;
    } else {
      status = "Game Over! It's a draw!";
    }
  } else {
    status = `Current Player: ${currentPlayer}`;
  }

  return (
    <div className="game-container">
      <h1>Tic Tac Toe</h1>
      <div className="scoreboard">
        <div className="score">
          <span>X: {xScore}</span>
        </div>
        <div className="score">
          <span>Draws: {draws}</span>
        </div>
        <div className="score">
          <span>O: {oScore}</span>
        </div>
      </div>
      <div className="status">{status}</div>
      <div className="board">
        <div className="board-row">
          {renderSquare(0)}
          {renderSquare(1)}
          {renderSquare(2)}
        </div>
        <div className="board-row">
          {renderSquare(3)}
          {renderSquare(4)}
          {renderSquare(5)}
        </div>
        <div className="board-row">
          {renderSquare(6)}
          {renderSquare(7)}
          {renderSquare(8)}
        </div>
      </div>
      <div className="buttons">
        <button className="btn-reset" onClick={handleReset}>
          New Game
        </button>
        <button className="btn-reset-scores" onClick={handleResetScores}>
          Reset Scores
        </button>
      </div>
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<TicTacToe />);
