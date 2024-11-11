from main import pygame
from main import random 
from main import CELL_SIZE
from main import DIRECTIONS

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True]

    def draw(self, screen, color=(0, 0, 0)):
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE
        if self.walls[0]:  
            pygame.draw.line(screen, color, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]:  
            pygame.draw.line(screen, color, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]:  
            pygame.draw.line(screen, color, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[3]:  
            pygame.draw.line(screen, color, (x, y), (x, y + CELL_SIZE), 2)


def generate_maze(grid, start_cell):
    stack = [start_cell]
    start_cell.visited = True
    while stack:
        current = stack[-1]
        neighbors = []
        for i, (dx, dy) in enumerate(DIRECTIONS):
            nx, ny = current.x + dx, current.y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and not grid[ny][nx].visited:
                neighbors.append((grid[ny][nx], i))
        if neighbors:
            neighbor, direction = random.choice(neighbors)
            current.walls[direction] = False
            neighbor.walls[(direction + 2) % 4] = False
            neighbor.visited = True
            stack.append(neighbor)
        else:
            stack.pop()
