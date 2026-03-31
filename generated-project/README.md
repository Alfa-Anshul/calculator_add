# Sudoku Terminal Game

A simple terminal-based Sudoku game written in Python.

## Features

- Simple and lightweight implementation
- Terminal-based interface
- Auto-generates random Sudoku puzzles
- Move validation
- Hint system (shows solution)
- Win detection

## Requirements

- Python 3.6+
- No external dependencies

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. Enter moves in the format: `row col number`
   - `row`: 0-8 (top to bottom)
   - `col`: 0-8 (left to right)
   - `number`: 1-9 to place, or 0 to clear a cell

3. Commands:
   - `hint` - Shows the complete solution
   - `quit` - Exit the game

## Example Move

```
Enter move (row col num): 0 0 5
```

This places the number 5 at row 0, column 0.

## Game Rules

- Fill the 9x9 grid with numbers 1-9
- Each row must contain all digits 1-9
- Each column must contain all digits 1-9
- Each 3x3 box must contain all digits 1-9
- No duplicates allowed in any row, column, or box

## License

MIT License
