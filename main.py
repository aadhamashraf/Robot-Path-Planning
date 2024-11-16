from Basic_Attributes import *
from Environment import mazeSetup, Buttons, comparewell
from Searching_Algorithms import Uninformed_Search, Heuristic_Search, Local_Search

compareAlgos = {
    "BFS": 0,
    "DFS": 0,
    "UCS": 0,
    "IDS": 0,
    "Greedy BFS": 0,
    "A Star": 0,
    "Hill Climbing Stairs": 0,
    "Simulated Annealing": 0,
    "Genetic Algos": 0
}

maze = start_pos = goal_pos = path = step_count = 0


def main():
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(
        r"C:\Users\Prof.Ashraf\source\repos\Trial_AI_15_11\Trial_AI_15_11\Environment\assets\01. Ground Theme.mp3")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1, 0.0)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Robot Path Navigator")

    maze, start_pos, goal_pos = mazeSetup.create_maze()
    print(maze)
    path = None

    def solve_bfs():
        nonlocal path
        path, frontier, step_count, elapsed_time = Uninformed_Search.bfs(
            maze, start_pos, goal_pos)
        compareAlgos['BFS'] = elapsed_time

    def solve_dfs():
        nonlocal path
        path, frontier, steps, timetaken = Uninformed_Search.dfs(
            maze, start_pos, goal_pos)
        comparewell.export_frontier(frontier, "DFS")
        compareAlgos["DFS"] = timetaken

    def solve_greedy_BFS():
        print("Solving with Greedy BFS...")
        path, frontier, step_count, elapsed_time = Heuristic_Search.greedy_bfs(
            maze, start_pos, goal_pos)
        compareAlgos['Greedy BFS'] = elapsed_time

    def solve_Astar():
        print("Solving with A*...")
        path, frontier, step_count, elapsed_time = Heuristic_Search.a_star(
            maze, start_pos, goal_pos)
        compareAlgos['A Star'] = elapsed_time

    def reset_path():
        nonlocal path
        path = None

    def reset_maze():
        nonlocal maze, start_pos, goal_pos, path
        maze, start_pos, goal_pos = mazeSetup.create_maze()
        path = None

    def compare_ExcutionTime():
        comparewell.showDifferences_ExecutionTime(compareAlgos)

    buttons_properties = [
        ('BFS', button_x, button_y, button_width, button_height, None, solve_bfs),
        ('DFS', button_x, button_y + button_height + button_gap,
         button_width, button_height, None, solve_dfs),
        ('UCS', button_x, button_y + 2 * (button_height + button_gap),
         button_width, button_height, None, solve_dfs),
        ('IDS', button_x, button_y + 3 * (button_height + button_gap),
         button_width - 60, button_height, None, None),
        ('-', button_x + button_width - 2 * (button_width / 8) - 10, button_y + 3 *
         (button_height + button_gap), button_width / 8, button_height, None, None),
        ('+', button_x + button_width - (button_width / 8) - 10, button_y + 3 *
         (button_height + button_gap), button_width / 8, button_height, None, None),
        ('Greedy BFS', button_x, button_y + 4 * (button_height + button_gap),
         button_width, button_height, None, solve_greedy_BFS),
        ('A Star', button_x, button_y + 5 * (button_height + button_gap),
         button_width, button_height, None, solve_Astar),
        ('Hill Climbing', button_x, button_y + 6 * (button_height +
         button_gap), button_width, button_height, None, None),
        ('Simulated Annealing', button_x, button_y + 7 *
         (button_height + button_gap), button_width, button_height, None, None),
        ('Genetic Algos', button_x, button_y + 8 * (button_height +
         button_gap), button_width, button_height, None, None),
        ('Compare Algos', button_x, button_y + 9 * (button_height + button_gap),
         button_width, button_height, None, compare_ExcutionTime),
        ('Reset path', button_x, button_y + 10 * (button_height + button_gap),
         button_width, button_height, None, reset_path),
        ('Reset Maze', button_x, button_y + 11 * (button_height +
         button_gap), button_width, button_height, None, reset_maze)

    ]

    buttons = []
    for text, x, y, width, height, subtext, action in buttons_properties:
        button = Buttons.Button(x, y, width, height, text, subtext, action)
        buttons.append(button)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_hover(pygame.mouse.get_pos()):
                        button.click()

        screen.fill(WHITE)

        mazeSetup.draw_maze(screen, maze, start_pos, goal_pos, path)

        divider_x = button_x - 50
        pygame.draw.rect(screen, BLACK, (divider_x, 0, 10, SCREEN_HEIGHT - 3))

        for button in buttons:
            button.draw(screen, button.is_hover(pygame.mouse.get_pos()))

        font = pygame.font.Font(None, 25)
        text = font.render(f"Steps: {step_count}", True, BLACK)
        screen.blit(text, (button_x, button_y + 60 * button_gap))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
