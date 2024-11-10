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

def export_frontier(frontier):
    with open("frontier.txt", "w") as f:
        for node in frontier:
            f.write(f"{node}\n")

def draw_tree_with_turtle(frontier, path):
    # Initialize turtle
    turtle.setup(800, 600)
    turtle.speed(0)
    turtle.hideturtle()
    
    # Set starting position for turtle drawing
    turtle.penup()
    turtle.goto(0, 250)
    turtle.pendown()

    # Draw nodes and connect them with lines to represent the tree
    node_positions = {}
    y_offset = 100

    for idx, node in enumerate(frontier):
        x = (idx % 10) * 60 - 300  # Adjust x position based on node index
        y = 250 - (idx // 10) * y_offset  # Adjust y position based on rows

        # Store node position for drawing lines later
        node_positions[node] = (x, y)

        # Draw the node (circle)
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.circle(15)  # Draw circle to represent the node

        # Label the node (e.g., with its coordinates or ID)
        turtle.penup()
        turtle.goto(x - 5, y + 5)  # Position the label inside the circle
        turtle.pendown()
        turtle.write(f"{node}", font=("Arial", 8, "normal"))

    # Draw lines between parent and child nodes to represent the tree structure
    for node in path:
        parent = path[node]  # Assuming path contains parent-child relationships

        if parent in node_positions:
            parent_pos = node_positions[parent]
            node_pos = node_positions[node]
            
            turtle.penup()
            turtle.goto(parent_pos[0], parent_pos[1])
            turtle.pendown()
            turtle.goto(node_pos[0], node_pos[1])  # Draw line between parent and child node

    turtle.done()

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
                elif 820 <= x <= 920 and 260 <= y <= 300:
                    export_frontier(frontier)  # Export frontier to file
                elif 820 <= x <= 920 and 320 <= y <= 360:
                    draw_tree_with_turtle(frontier, path)  # Call turtle drawing function

        # Run the selected algorithm
        if selected_algorithm == 'BFS':
            path, frontier, step_count = bfs(start, goal, grid)
        elif selected_algorithm == 'DFS':
            path, frontier, step_count = dfs(start, goal, grid)
        elif selected_algorithm == 'A*':
            path, frontier, step_count = a_star(start, goal, grid)

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
