from Basic_Attributes import *
from Environment import Buttons, comparewell
from Searching_Algorithms import Uninformed_Search, Heuristic_Search, Local_Search
from testing.src.environment import mazeSetup


def manhattan_metric(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean_metric(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def update_title(task):
    pygame.display.set_caption(f"Solving with {task} Algorithm")


compareAlgos = {
    # [Time, Steps]
    "BFS": [0, 0],
    "DFS": [0, 0],
    "UCS": [0, 0],
    "IDS": [0, 0],
    "Greedy BFS (Manhattan)": [0, 0],
    "Greedy BFS (Euclidean)": [0, 0],
    "A* (Manhattan)": [0, 0],
    "A* (Euclidean)": [0, 0],
    "Hill Climbing": [0, 0],
    "Simulated Annealing": [0, 0],
    "Genetic Algorithm": [0, 0]
}
maze = start_pos = goal_pos = path = step_count = elapsed_time = l = 0


def main():
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(r".\Environment\assets\01. Ground Theme.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1, 0.0)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Robot Path Navigator")

    maze, start_pos, goal_pos = mazeSetup.create_maze()
    path = None

    def solve_bfs():
        nonlocal path
        global step_count
        update_title("BFS")
        path, frontier, step_count, elapsed_time = Uninformed_Search.bfs(
            maze, start_pos, goal_pos)
        comparewell.export_frontier(frontier, "BFS")
        compareAlgos["BFS"] = [elapsed_time, step_count]

    def solve_dfs():
        nonlocal path
        global step_count
        update_title("DFS")
        path, frontier, step_count, elapsed_time = Uninformed_Search.dfs(
            maze, start_pos, goal_pos)
        comparewell.export_frontier(frontier, "DFS")
        compareAlgos["DFS"] = [elapsed_time, step_count]

    def solve_ucs():
        nonlocal path
        global step_count
        update_title("UCS")
        path, frontier, step_count, elapsed_time = Uninformed_Search.ucs(
            maze, start_pos, goal_pos)
        comparewell.export_frontier(frontier, "UCS")
        compareAlgos["UCS"] = [elapsed_time, step_count]

    def solve_ids():
        nonlocal path
        global step_count, l
        update_title("IDS")
        path, frontier, step_count, elapsed_time = Uninformed_Search.ids(
            maze, start_pos, goal_pos, l)
        comparewell.export_frontier(frontier, "IDS")
        compareAlgos["IDS"] = [elapsed_time, step_count]

    def increaseL():
        global l
        l += 5
        solve_ids()

    def decreaseL():
        global l
        if l > 0:
            l -= 5
        solve_ids()

    def solve_greedy_bfs(metric, metric_name):
        nonlocal path
        global step_count
        update_title(f"Greedy BFS ({metric_name})")
        path, frontier, step_count, elapsed_time = Heuristic_Search.greedy_bfs(
            maze, start_pos, goal_pos, metric)
        comparewell.export_frontier(frontier, f"Greedy BFS ({metric_name})")
        compareAlgos[f"Greedy BFS ({metric_name})"] = [
            elapsed_time, step_count]

    def solve_a_star(metric, metric_name):
        nonlocal path
        global step_count
        update_title(f"A* ({metric_name})")
        path, frontier, step_count, elapsed_time = Heuristic_Search.a_star(
            maze, start_pos, goal_pos, metric)
        comparewell.export_frontier(frontier, f"A Star ({metric_name})")
        compareAlgos[f"A Star ({metric_name})"] = [elapsed_time, step_count]

    def solve_hill_climbing():
        nonlocal path
        global step_count
        update_title("Hill Climbing")
        path, frontier, step_count, elapsed_time = Local_Search.hill_climbing(
            maze, start_pos, goal_pos)
        comparewell.export_frontier(frontier, "Hill Climbing")
        compareAlgos["Hill Climbing"] = [elapsed_time, step_count]

    def solve_simulated_annealing():
        nonlocal path
        global step_count
        update_title("Simulated Annealing")
        path, frontier, step_count, elapsed_time = Local_Search.simulated_annealing(
            maze, start_pos, goal_pos)
        comparewell.export_frontier(frontier, "Simulated Annealing")
        compareAlgos["Simulated Annealing"] = [elapsed_time, step_count]

    def solve_genetic_algorithm():
        nonlocal path
        global step_count
        update_title("Genetic Algorithm")
        path, frontier, step_count, elapsed_time = Local_Search.genetic_algorithm(
            maze, start_pos, goal_pos)
        comparewell.export_frontier(frontier, "Genetic Algorithm")
        compareAlgos["Genetic Algorithm"] = [elapsed_time, step_count]

    def reset_path():
        nonlocal path
        path = None

    def reset_maze():
        nonlocal maze, start_pos, goal_pos, path
        maze, start_pos, goal_pos = mazeSetup.create_maze()
        path = None

    def compare_execution_time():
        comparewell.showDifferences_ExecutionTime(compareAlgos)

    buttons_properties = [
        ('BFS', button_x, button_y, button_width, button_height, None, solve_bfs),
        ('DFS', button_x, button_y + button_height + button_gap,
         button_width, button_height, None, solve_dfs),
        ('UCS', button_x, button_y + 2 * (button_height + button_gap),
         button_width, button_height, None, solve_ucs),

        ('IDS', button_x, button_y + 3 * (button_height + button_gap),
         button_width - 60, button_height, None, None),
        ('-', button_x + button_width - (button_width / 8) - 42, button_y + 3 *
         (button_height + button_gap), button_width / 8, button_height, None, decreaseL),
        ('+', button_x + button_width - (button_width / 8), button_y + 3 *
         (button_height + button_gap), button_width / 8, button_height, None, increaseL),

        ('Greedy BFS (Manhattan)', button_x, button_y + 4 * (button_height + button_gap),
         button_width, button_height, None, lambda: solve_greedy_bfs(manhattan_metric, "Manhattan")),
        ('Greedy BFS (Euclidean)', button_x, button_y + 5 * (button_height + button_gap),
         button_width, button_height, None, lambda: solve_greedy_bfs(euclidean_metric, "Euclidean")),

        ('A* (Manhattan)', button_x, button_y + 6 * (button_height + button_gap), button_width,
         button_height, None, lambda: solve_a_star(manhattan_metric, "Manhattan")),
        ('A* (Euclidean)', button_x, button_y + 7 * (button_height + button_gap), button_width,
         button_height, None, lambda: solve_a_star(euclidean_metric, "Euclidean")),

        ('Hill Climbing', button_x, button_y + 8 * (button_height + button_gap),
         button_width, button_height, None, solve_hill_climbing),
        ('Simulated Annealing', button_x, button_y + 9 * (button_height + button_gap),
         button_width, button_height, None, solve_simulated_annealing),
        ('Genetic Algorithm', button_x, button_y + 10 * (button_height +
         button_gap), button_width, button_height, None, solve_genetic_algorithm),
        ('Compare Algos', button_x, button_y + 11 * (button_height + button_gap),
         button_width, button_height, None, compare_execution_time),
        ('Reset Path', button_x, button_y + 12 * (button_height + button_gap),
         button_width, button_height, None, reset_path),
        ('Reset Maze', button_x, button_y + 13 * (button_height +
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
                        button.action()
                        break

        screen.fill(WHITE)
        mazeSetup.draw_grid(screen, maze, start_pos, goal_pos, path)
        divider_x = button_x - 50
        pygame.draw.rect(screen, BLACK, (divider_x, 0, 10, SCREEN_HEIGHT - 3))

        for button in buttons:
            button.draw(screen)

        font = pygame.font.SysFont('Arial', 26, bold=True)
        NumSteps = font.render(f"Steps: {step_count}", True, BLACK)
        screen.blit(NumSteps, (button_x, button_y + 70 * button_gap))

        lValue = font.render(f"{l}", True, BLACK)
        screen.blit(lValue, (button_x + button_width - (button_width *
                    2.7 / 8), button_y + 3 * (button_height + button_gap) + 12.5))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
