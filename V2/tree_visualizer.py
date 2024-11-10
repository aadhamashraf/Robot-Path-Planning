import pygame
import sys
import time
import turtle
from environment import Cell, generate_maze
from algorithms import bfs, dfs, a_star

# Define constants
WIDTH, HEIGHT = 1000, 600
CELL_SIZE = 20
MAZE_WIDTH = WIDTH // CELL_SIZE - 10
MAZE_HEIGHT = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_BORDER_COLOR = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Solver with Algorithms')

# Define TreeNode class for visualization
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def deserialize(string):
    if string == '{}':
        return None
    nodes = [None if val == 'null' else TreeNode(int(val))
             for val in string.strip('[]{}').split(',')]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids: node.left = kids.pop()
            if kids: node.right = kids.pop()
    return root

def drawtree(root):
    def height(root):
        return 1 + max(height(root.left), height(root.right)) if root else -1
    
    def jumpto(x, y):
        t.penup()
        t.goto(x, y)
        t.pendown()
    
    def draw(node, x, y, dx):
        if node:
            t.goto(x, y)
            jumpto(x, y-20)
            t.write(node.val, align='center', font=('Arial', 12, 'normal'))
            draw(node.left, x-dx, y-60, dx/2)
            jumpto(x, y-20)
            draw(node.right, x+dx, y-60, dx/2)
    
    t = turtle.Turtle()
    t.speed(0); turtle.delay(0)
    h = height(root)
    jumpto(0, 30*h)
    draw(root, 0, 30*h, 40*h)
    t.hideturtle()
    turtle.mainloop()

def export_frontier(frontier):
    with open("frontier.txt", "w") as f:
        for node in frontier:
            f.write(f"{node}\n")

def draw_button(screen, text, x, y, width, height):
    font = pygame.font.Font(None, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x, y, width, height), 2)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def draw_path(path):
    for node in path:
        pygame.draw.rect(screen, GREEN, (node[0] * CELL_SIZE, node[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    grid = [[Cell(x, y) for x in range(MAZE_WIDTH)] for y in range(MAZE_HEIGHT)]
    start_cell = grid[0][0]
    generate_maze(grid, start_cell)

    start = (0, 0)
    goal = (MAZE_WIDTH - 1, MAZE_HEIGHT - 1)
    selected_algorithm = None
    path = {}
    frontier = set()
    step_count = 0

    running = True
    clock = pygame.time.Clock()  # Initialize the clock for controlling the frame rate
    tree_root = None  # Initialize tree structure

    while running:
        screen.fill(WHITE)

        # Draw the grid (maze)
        for row in grid:
            for cell in row:
                cell.draw(screen)

        # Draw buttons
        draw_button(screen, 'BFS', 820, 20, 100, 40)
        draw_button(screen, 'DFS', 820, 80, 100, 40)
        draw_button(screen, 'A*', 820, 140, 100, 40)
        draw_button(screen, 'Reset', 820, 200, 100, 40)
        draw_button(screen, 'Export Frontier', 820, 260, 150, 40)
        draw_button(screen, 'Show Tree', 820, 320, 150, 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Button click detection
                if 820 <= x <= 920 and 20 <= y <= 60:
                    selected_algorithm = 'BFS'
                elif 820 <= x <= 920 and 80 <= y <= 120:
                    selected_algorithm = 'DFS'
                elif 820 <= x <= 920 and 140 <= y <= 180:
                    selected_algorithm = 'A*'
                elif 820 <= x <= 920 and 200 <= y <= 240:
                    path, frontier, step_count = {}, set(), 0  # Reset variables
                    generate_maze(grid, start_cell)  # Reset maze
                    tree_root = None  # Reset tree
                elif 820 <= x <= 920 and 260 <= y <= 300:
                    export_frontier(frontier)  # Export frontier to file
                elif 820 <= x <= 920 and 320 <= y <= 360:
                    if tree_root:
                        drawtree(tree_root)  # Call turtle drawing function if tree exists

        # Run the selected algorithm
        if selected_algorithm == 'BFS':
            path, frontier, step_count, tree_root = bfs(start, goal, grid)
        elif selected_algorithm == 'DFS':
            path, frontier, step_count, tree_root = dfs(start, goal, grid)
        elif selected_algorithm == 'A*':
            path, frontier, step_count, tree_root = a_star(start, goal, grid)

        # Progressive path drawing
        draw_path(path)

        # Display step count
        font = pygame.font.Font(None, 30)
        text = font.render(f"Steps: {step_count}", True, BLACK)
        screen.blit(text, (820, 400))

        pygame.display.flip()

        clock.tick(10)  # Control the frame rate (10 frames per second)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
