import random
import time
from enum import Enum
from typing import List, Tuple

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self, width: int = 20, height: int = 10):
        self.width = width
        self.height = height
        self.reset_game()
    
    def reset_game(self):
        # Initialize snake in the middle
        self.snake: List[Tuple[int, int]] = [(self.width // 2, self.height // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
    
    def spawn_food(self) -> Tuple[int, int]:
        """Spawn food at a random location not occupied by snake"""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def set_direction(self, direction: Direction):
        """Set the next direction for the snake"""
        # Prevent snake from reversing into itself
        if (direction.value[0] * -1, direction.value[1] * -1) != (self.direction.value[0], self.direction.value[1]):
            self.next_direction = direction
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()
    
    def get_state(self) -> dict:
        """Return current game state"""
        return {
            'snake': self.snake,
            'food': self.food,
            'score': self.score,
            'game_over': self.game_over,
            'width': self.width,
            'height': self.height
        }

if __name__ == '__main__':
    game = SnakeGame()
    print(f"Snake Game Started - Size: {game.width}x{game.height}")
    print(f"Initial State: {game.get_state()}")
