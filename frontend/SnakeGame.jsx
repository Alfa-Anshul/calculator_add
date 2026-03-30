import React, { useState, useEffect, useRef } from 'react';
import './SnakeGame.css';

const GRID_WIDTH = 20;
const GRID_HEIGHT = 10;
const CELL_SIZE = 30;
const GAME_SPEED = 150; // milliseconds

const Direction = {
  UP: { x: 0, y: -1 },
  DOWN: { x: 0, y: 1 },
  LEFT: { x: -1, y: 0 },
  RIGHT: { x: 1, y: 0 },
};

const SnakeGame = () => {
  const [snake, setSnake] = useState([{ x: 10, y: 5 }]);
  const [food, setFood] = useState({ x: 15, y: 5 });
  const [direction, setDirection] = useState(Direction.RIGHT);
  const [nextDirection, setNextDirection] = useState(Direction.RIGHT);
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);
  const gameLoopRef = useRef(null);

  // Spawn food at random location not occupied by snake
  const spawnFood = (currentSnake) => {
    let newFood;
    do {
      newFood = {
        x: Math.floor(Math.random() * GRID_WIDTH),
        y: Math.floor(Math.random() * GRID_HEIGHT),
      };
    } while (currentSnake.some((segment) => segment.x === newFood.x && segment.y === newFood.y));
    return newFood;
  };

  // Handle keyboard input
  useEffect(() => {
    const handleKeyPress = (e) => {
      switch (e.key.toLowerCase()) {
        case 'arrowup':
        case 'w':
          if (direction.y === 0) setNextDirection(Direction.UP);
          e.preventDefault();
          break;
        case 'arrowdown':
        case 's':
          if (direction.y === 0) setNextDirection(Direction.DOWN);
          e.preventDefault();
          break;
        case 'arrowleft':
        case 'a':
          if (direction.x === 0) setNextDirection(Direction.LEFT);
          e.preventDefault();
          break;
        case 'arrowright':
        case 'd':
          if (direction.x === 0) setNextDirection(Direction.RIGHT);
          e.preventDefault();
          break;
        case 'enter':
          if (!gameStarted || gameOver) {
            resetGame();
            setGameStarted(true);
          }
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [direction, gameStarted, gameOver]);

  // Game loop
  useEffect(() => {
    if (!gameStarted || gameOver) return;

    gameLoopRef.current = setInterval(() => {
      setSnake((prevSnake) => {
        setDirection(nextDirection);
        const head = prevSnake[0];
        const newHead = {
          x: head.x + nextDirection.x,
          y: head.y + nextDirection.y,
        };

        // Check wall collision
        if (newHead.x < 0 || newHead.x >= GRID_WIDTH || newHead.y < 0 || newHead.y >= GRID_HEIGHT) {
          setGameOver(true);
          return prevSnake;
        }

        // Check self collision
        if (prevSnake.some((segment) => segment.x === newHead.x && segment.y === newHead.y)) {
          setGameOver(true);
          return prevSnake;
        }

        let newSnake = [newHead, ...prevSnake];

        // Check food collision
        if (newHead.x === food.x && newHead.y === food.y) {
          setScore((prev) => prev + 10);
          setFood(spawnFood(newSnake));
        } else {
          newSnake.pop();
        }

        return newSnake;
      });
    }, GAME_SPEED);

    return () => clearInterval(gameLoopRef.current);
  }, [gameStarted, gameOver, nextDirection, food]);

  const resetGame = () => {
    setSnake([{ x: 10, y: 5 }]);
    setFood(spawnFood([{ x: 10, y: 5 }]));
    setDirection(Direction.RIGHT);
    setNextDirection(Direction.RIGHT);
    setScore(0);
    setGameOver(false);
  };

  const handleStartGame = () => {
    resetGame();
    setGameStarted(true);
  };

  const handleResetGame = () => {
    resetGame();
    setGameStarted(false);
  };

  return (
    <div className="game-container">
      <h1>🐍 Snake Game</h1>
      <div className="info-panel">
        <div className="score">Score: <span>{score}</span></div>
        <div className="status">
          {!gameStarted ? '⏸ Not Started' : gameOver ? '💀 Game Over!' : '▶ Playing'}
        </div>
      </div>

      <div
        className="game-board"
        style={{
          width: `${GRID_WIDTH * CELL_SIZE}px`,
          height: `${GRID_HEIGHT * CELL_SIZE}px`,
        }}
      >
        {/* Grid background */}
        {Array.from({ length: GRID_HEIGHT }).map((_, y) =>
          Array.from({ length: GRID_WIDTH }).map((_, x) => (
            <div
              key={`${x}-${y}`}
              className="grid-cell"
              style={{
                left: `${x * CELL_SIZE}px`,
                top: `${y * CELL_SIZE}px`,
                width: `${CELL_SIZE}px`,
                height: `${CELL_SIZE}px`,
              }}
            />
          ))
        )}

        {/* Food */}
        <div
          className="food"
          style={{
            left: `${food.x * CELL_SIZE}px`,
            top: `${food.y * CELL_SIZE}px`,
            width: `${CELL_SIZE}px`,
            height: `${CELL_SIZE}px`,
          }}
        />

        {/* Snake */}
        {snake.map((segment, index) => (
          <div
            key={index}
            className={`snake-segment ${index === 0 ? 'head' : 'body'}`}
            style={{
              left: `${segment.x * CELL_SIZE}px`,
              top: `${segment.y * CELL_SIZE}px`,
              width: `${CELL_SIZE}px`,
              height: `${CELL_SIZE}px`,
            }}
          />
        ))}
      </div>

      <div className="controls">
        <button className="btn btn-primary" onClick={handleStartGame} disabled={gameStarted && !gameOver}>
          {gameStarted ? 'Game Running' : 'Start Game'}
        </button>
        <button className="btn btn-secondary" onClick={handleResetGame}>
          Reset Game
        </button>
      </div>

      <div className="instructions">
        <h3>How to Play:</h3>
        <ul>
          <li>Use <strong>Arrow Keys</strong> or <strong>WASD</strong> to move the snake</li>
          <li>Eat the 🔴 food to grow and gain points</li>
          <li>Avoid hitting walls and yourself</li>
          <li>Press <strong>Enter</strong> to start/restart the game</li>
        </ul>
      </div>
    </div>
  );
};

export default SnakeGame;
