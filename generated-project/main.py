#!/usr/bin/env python3
"""
Simple Terminal-Based Sudoku Game
A basic implementation for playing Sudoku in the terminal.
"""

import random
import copy

class SudokuGame:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.solution = [[0] * 9 for _ in range(9)]
        self.generate_puzzle()
        self.player_board = copy.deepcopy(self.board)

    def is_valid(self, board, row, col, num):
        """Check if placing num at (row, col) is valid"""
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True

    def solve(self, board):
        """Solve Sudoku using backtracking"""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def generate_puzzle(self):
        """Generate a random Sudoku puzzle"""
        # Fill diagonal 3x3 boxes with random numbers
        for box in range(3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    self.board[box * 3 + i][box * 3 + j] = nums[i * 3 + j]
        
        # Solve the puzzle to get a valid solution
        self.solution = copy.deepcopy(self.board)
        self.solve(self.solution)
        
        # Remove numbers to create puzzle (remove 40 numbers for medium difficulty)
        cells_to_remove = 40
        removed = 0
        while removed < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1

    def display_board(self):
        """Display the current game board"""
        print("\n")
        print("  " + " " * 24 + "SUDOKU")
        print("  " + "-" * 26)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("  " + "-" * 26)
            row_str = "  "
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                if self.player_board[i][j] == 0:
                    row_str += ". "
                else:
                    row_str += str(self.player_board[i][j]) + " "
            print(row_str)
        print("  " + "-" * 26)
        print()

    def is_complete(self):
        """Check if the puzzle is solved"""
        for row in self.player_board:
            if 0 in row:
                return False
        return self.player_board == self.solution

    def is_valid_move(self, row, col, num):
        """Check if a move is valid"""
        if self.board[row][col] != 0:  # Cell was pre-filled
            print("Cannot modify pre-filled cells!")
            return False
        
        # Check if number is already in the row, column, or box
        if num in self.player_board[row]:
            return False
        if num in [self.player_board[i][col] for i in range(9)]:
            return False
        
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.player_board[i][j] == num:
                    return False
        
        return True

    def make_move(self, row, col, num):
        """Place a number on the board"""
        if row < 0 or row > 8 or col < 0 or col > 8 or num < 0 or num > 9:
            print("Invalid input! Row and column must be 0-8, number must be 0-9.")
            return False
        
        if num == 0:
            self.player_board[row][col] = 0
            return True
        
        if self.is_valid_move(row, col, num):
            self.player_board[row][col] = num
            return True
        else:
            print("Invalid move! Number already exists in row, column, or box.")
            return False

    def play(self):
        """Main game loop"""
        print("\n" + "="*30)
        print("Welcome to Sudoku!")
        print("="*30)
        print("\nInstructions:")
        print("- Enter moves as: row col number")
        print("- Row and column are 0-8")
        print("- Number is 1-9 (or 0 to clear)")
        print("- Type 'quit' to exit")
        print("- Type 'hint' to see the solution")
        
        while True:
            self.display_board()
            
            if self.is_complete():
                print("🎉 Congratulations! You solved the Sudoku!")
                break
            
            user_input = input("Enter move (row col num) or 'quit'/'hint': ").strip().lower()
            
            if user_input == 'quit':
                print("Thanks for playing!")
                break
            elif user_input == 'hint':
                print("\nSolution:")
                print("(Note: This is the solution, not recommended!)\n")
                for row in self.solution:
                    print(" ".join(str(x) for x in row))
                print()
            else:
                try:
                    parts = user_input.split()
                    if len(parts) != 3:
                        print("Invalid input! Please enter: row col number")
                        continue
                    
                    row, col, num = int(parts[0]), int(parts[1]), int(parts[2])
                    self.make_move(row, col, num)
                except ValueError:
                    print("Invalid input! Please enter three numbers.")

if __name__ == "__main__":
    game = SudokuGame()
    game.play()
