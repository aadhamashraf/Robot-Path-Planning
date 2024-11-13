import pygame
import sys
# import pandas as pd
import os 
import time 
import random 

from environment import Cell, generate_maze
from Searching_Algorithms import Uninformed_Search, Local_Search, Heuristic_Search
from collections import deque

compareAlgos = {
    "BFS" : [0], 
    "DFS" : [0], 
    "UCS" : [0],
    "IDS" : [0],
    "Greedy BFS" :[0] ,
    "A*" :[0],
    "Hill Climbing Stairs":[0],
    "Simulated Annealing":[0],
    "Genetic Algos":[0]
}

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
WIDTH, HEIGHT = 1300, 640
CELL_SIZE = 20
MAZE_WIDTH = WIDTH // CELL_SIZE - 10
MAZE_HEIGHT = HEIGHT // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_BORDER_COLOR = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def export_frontier(frontier , algorithm):
    with open(f"frontier_{algorithm}.txt", "w") as f:
        for node in frontier:
            f.write(f"{node}\n")


def draw_button(screen, text, x, y, width, height):
    font = pygame.font.Font(None, 20)
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x, y, width, height), 2)
    
    if ' ' in text: 
        lines = text.split(' ', 1)
        line1 = font.render(lines[0], True, BLACK)
        line2 = font.render(lines[1], True, BLACK)
        screen.blit(line1, (x + (width - line1.get_width()) // 2, y + 5))
        screen.blit(line2, (x + (width - line2.get_width()) // 2, y + height // 2 + 5))
    else:
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
    timeTaken = 0
    running = True
    clock = pygame.time.Clock()

    button_x = 1125 
    button_width = 110
    button_height = 45
    button_y = 30
    button_gap = 60 

    while running:
        screen.fill(WHITE)

        for row in grid:
            for cell in row:
                cell.draw(screen)

        # Draw buttons for each algorithm
        draw_button(screen, 'BFS', button_x, button_y, button_width, button_height)
        draw_button(screen, 'DFS', button_x, button_y + button_gap, button_width, button_height)
        draw_button(screen, 'UCS', button_x, button_y + 2 * button_gap, button_width, button_height)
        draw_button(screen, 'IDS', button_x, button_y + 3 * button_gap, button_width, button_height)
        draw_button(screen, 'Greedy BFS', button_x, button_y + 4 * button_gap, button_width, button_height)
        draw_button(screen, 'A*', button_x, button_y + 5 * button_gap, button_width, button_height)
        draw_button(screen, 'Hill Climbing', button_x, button_y + 6 * button_gap, button_width, button_height)
        draw_button(screen, 'Simulated Annealing', button_x, button_y + 7 * button_gap, button_width, button_height)
        draw_button(screen, 'Genetic Algos', button_x, button_y + 8 * button_gap, button_width, button_height)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
                    selected_algorithm = 'BFS'
                elif button_x <= x <= button_x + button_width and button_y + button_gap <= y <= button_y + button_gap + button_height:
                    selected_algorithm = 'DFS'
                elif button_x <= x <= button_x + button_width and button_y + 2 * button_gap <= y <= button_y + 2 * button_gap + button_height:
                    selected_algorithm = 'UCS'
                elif button_x <= x <= button_x + button_width and button_y + 3 * button_gap <= y <= button_y + 3 * button_gap + button_height:
                    selected_algorithm = 'IDS'
                elif button_x <= x <= button_x + button_width and button_y + 4 * button_gap <= y <= button_y + 4 * button_gap + button_height:
                    selected_algorithm = 'Greedy BFS'
                elif button_x <= x <= button_x + button_width and button_y + 5 * button_gap <= y <= button_y + 5 * button_gap + button_height:
                    selected_algorithm = 'A*'
                elif button_x <= x <= button_x + button_width and button_y + 6 * button_gap <= y <= button_y + 6 * button_gap + button_height:
                    selected_algorithm = 'Hill Climbing'
                elif button_x <= x <= button_x + button_width and button_y + 7 * button_gap <= y <= button_y + 7 * button_gap + button_height:
                    selected_algorithm = 'Simulated Annealing'
                elif button_x <= x <= button_x + button_width and button_y + 8 * button_gap <= y <= button_y + 8 * button_gap + button_height:
                    selected_algorithm = 'Genetic Algos'
            
        if selected_algorithm == 'BFS':
            path, frontier, step_count , timeTaken = Uninformed_Search.bfs(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'BFS')

        elif selected_algorithm == 'DFS':
            path, frontier, step_count, timeTaken = Uninformed_Search.dfs(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'DFS')
        
        elif selected_algorithm == 'A*':
            path, frontier, step_count , timeTaken= Heuristic_Search.a_star(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'A*')
        
        elif selected_algorithm == 'UCS':
            path, frontier, step_count, timeTaken = Uninformed_Search.ucs(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'UCS')
        
        elif selected_algorithm == 'IDS':
            path, frontier, step_count, timeTaken = Uninformed_Search.ids(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'IDS')
        
        elif selected_algorithm == 'Greedy BFS':
            path, frontier, step_count, timeTaken = Heuristic_Search.greedy_bfs(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'Greedy BFS')
        
        elif selected_algorithm == 'Hill Climbing':
            path, frontier, step_count, timeTaken = Local_Search.hill_climbing(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'Hill Climbing')
        
        elif selected_algorithm == 'Simulated Annealing':
            path, frontier, step_count, timeTaken = Local_Search.simulated_annealing(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'Simulated Annealing')
        
        elif selected_algorithm == 'Genetic Algos':
            path, frontier, step_count, timeTaken = Local_Search.genetic_algorithm(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'Genetic Algos')

        font = pygame.font.Font(None, 25)
        text = font.render(f"Steps: {step_count}", True, BLACK)
        time_taken = font.render(f"Time Taken : {timeTaken* 1e-2}",True , BLACK)

        screen.blit(text, (button_x, button_y + 9 * button_gap))
        screen.blit(time_taken, (button_x, button_y + 9.5 * button_gap))

        pygame.display.flip()

        clock.tick(10)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
