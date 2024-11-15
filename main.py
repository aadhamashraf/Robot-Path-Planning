import pygame
import sys
import os 
import os.path
import time 
import random 
import matplotlib.pyplot as plt
from environment import Cell, generate_maze #, export_frontier , draw_button , draw_path , showDifferences_ExcutionTime
from Searching_Algorithms import Uninformed_Search, Local_Search, Heuristic_Search
from collections import deque
plt.style.use('dark_background')

compareAlgos = {
    # [Time]
    "BFS" :0, 
    "DFS" : 0, 
    "UCS" : 0,
    "IDS" : 0,
    "Greedy BFS" :0 ,
    "A Star" :0,
    "Hill Climbing Stairs":0,
    "Simulated Annealing":0,
    "Genetic Algos":0
}

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
WIDTH, HEIGHT = 1300, 650
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
    dir = rf"{os.getcwd()}\Forntier Results" 

    if not os.path.exists(dir):
        os.mkdir(dir)
    
    with open(os.path.join(dir, f"frontier_{algorithm}.txt"), "w") as f:
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

def showDifferences_ExecutionTime(compareAlgos):
    sorted_compareAlgos = dict(sorted(compareAlgos.items(), key=lambda item: item[1]))
    
    plt.figure(figsize=(10, 10))
    plt.barh(list(sorted_compareAlgos.keys()), list(sorted_compareAlgos.values()))
    plt.title("Searching Algorithms Execution Time")
    plt.xlabel("Execution Time")
    plt.ylabel("Searching Algorithm")
    plt.grid(True)
    plt.show()
    
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
    l = 10
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
        draw_button(screen, '-'  , button_x + button_width + 5, button_y + 3 * button_gap, button_width/8, button_height)
        draw_button(screen, '+'  , button_x + button_width + 40, button_y + 3 * button_gap, button_width/8, button_height)
        draw_button(screen, 'Greedy BFS', button_x, button_y + 4 * button_gap, button_width, button_height)
        draw_button(screen, 'A Star', button_x, button_y + 5 * button_gap, button_width, button_height)
        draw_button(screen, 'Hill Climbing', button_x, button_y + 6 * button_gap, button_width, button_height)
        draw_button(screen, 'Simulated Annealing', button_x, button_y + 7 * button_gap, button_width, button_height)
        draw_button(screen, 'Genetic Algos', button_x, button_y + 8 * button_gap, button_width, button_height)
        draw_button(screen, 'Compare Excution Time', button_x, button_y + 9 * button_gap, button_width, button_height)

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
                elif button_x + button_width + 5 <= x <= button_x + button_width + 5 + button_width/8 and button_y + 3 * button_gap <= y <= button_y + 3 * button_gap + button_height:
                    if l > 0:
                        l-=5
                elif button_x + button_width + 40 <= x <= button_x + button_width + 40 + button_width/8 and button_y + 3 * button_gap <= y <= button_y + 3 * button_gap + button_height:
                    l+=5
                elif button_x <= x <= button_x + button_width and button_y + 4 * button_gap <= y <= button_y + 4 * button_gap + button_height:
                    selected_algorithm = 'Greedy BFS'
                elif button_x <= x <= button_x + button_width and button_y + 5 * button_gap <= y <= button_y + 5 * button_gap + button_height:
                    selected_algorithm = 'A Star'
                elif button_x <= x <= button_x + button_width and button_y + 6 * button_gap <= y <= button_y + 6 * button_gap + button_height:
                    selected_algorithm = 'Hill Climbing'
                elif button_x <= x <= button_x + button_width and button_y + 7 * button_gap <= y <= button_y + 7 * button_gap + button_height:
                    selected_algorithm = 'Simulated Annealing'
                elif button_x <= x <= button_x + button_width and button_y + 8 * button_gap <= y <= button_y + 8 * button_gap + button_height:
                    selected_algorithm = 'Genetic Algos'
                elif button_x <= x <= button_x + button_width and button_y + 9 * button_gap <= y <= button_y + 9 * button_gap + button_height:
                    showDifferences_ExecutionTime(compareAlgos)

        if selected_algorithm == 'BFS':
            path, frontier, step_count , timeTaken = Uninformed_Search.bfs(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'BFS')
            compareAlgos['BFS'] = timeTaken
           
        elif selected_algorithm == 'DFS':
            path, frontier, step_count, timeTaken = Uninformed_Search.dfs(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'DFS')
            compareAlgos['DFS'] = timeTaken

        elif selected_algorithm == 'A Star':
            path, frontier, step_count , timeTaken= Heuristic_Search.a_star(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'A Star')
            compareAlgos['A Star'] = timeTaken

        elif selected_algorithm == 'UCS':
            path, frontier, step_count, timeTaken = Uninformed_Search.ucs(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'UCS')
            compareAlgos['UCS'] = timeTaken

        
        elif selected_algorithm == 'IDS':
            path, frontier, step_count, timeTaken = Uninformed_Search.ids(start, goal, grid, l)
            draw_path(path)
            export_frontier(frontier , 'IDS')
            compareAlgos['IDS'] = timeTaken

        
        elif selected_algorithm == 'Greedy BFS':
            path, frontier, step_count, timeTaken = Heuristic_Search.greedy_bfs(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'Greedy BFS')
            compareAlgos['Greedy BFS'] = timeTaken

        
        elif selected_algorithm == 'Hill Climbing':
            path, frontier, step_count, timeTaken = Local_Search.hill_climbing(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'Hill Climbing')
            compareAlgos['Hill Climbing'] = timeTaken

        
        elif selected_algorithm == 'Simulated Annealing':
            path, frontier, step_count, timeTaken = Local_Search.simulated_annealing(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'Simulated Annealing')
            compareAlgos['Simulated Annealing'] = timeTaken

        
        elif selected_algorithm == 'Genetic Algos':
            path, frontier, step_count, timeTaken = Local_Search.genetic_algorithm(start, goal, grid)
            draw_path(path)
            export_frontier(frontier , 'Genetic Algos')
            compareAlgos['Genetic Algos'] = timeTaken


        font = pygame.font.Font(None, 25)
        text = font.render(f"Steps: {step_count}", True, BLACK)
        
        screen.blit(text, (button_x, button_y + 10 * button_gap))

        lIds = font.render(f"{l}", True, BLACK)
        screen.blit(lIds, (button_x+button_width+19, button_y + 3 * button_gap + button_height/3 ))
        pygame.display.flip()

        clock.tick(10)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
