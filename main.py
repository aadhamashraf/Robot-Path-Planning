# In src/main.py
from src.algorithms.base_search import BaseSearch
from src.core.game_state import GameState
from src.core.algorithm_manager import AlgorithmManager
from src.environment.maze_generator import MazeGenerator
from src.ui.button_manager import ButtonManager
from src.ui.game_window import GameWindow
from src.utilities.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BUTTON_X,
    BUTTON_Y,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    BUTTON_GAP,
    MAZE_WIDTH,
    MAZE_HEIGHT,
)
import src.environment.mazeSetup as mazeSetup
from src.core.frontier_exporter import FrontierExporter  # Import FrontierExporter
from src.core.metrics_comparison import showDifferences_ExecutionTime
from src.utilities.constants import *

# Import Algorithm Functions
from src.algorithms.uninformed import bfs, dfs, ucs, ids
from src.algorithms.informed import greedy_bfs, astar
from src.algorithms.local import hill_climbing, simulated_annealing
from src.algorithms.genetic_algorithm import genetic_algorithm
from src.core.metrics import Metrics
from src.algorithms.q_learning_algorithm import q_learning  # Import QLearning
import threading
import queue

plot_queue = queue.Queue()


def plot_metrics_main_thread(reward_history, steps_history):
    for idx, (metric, title, ylabel) in enumerate([(reward_history, "Rewards Over Episodes", "Rewards"), (steps_history, "Steps Over Episodes", "Steps")]):
        plt.subplot(1, 2, idx + 1)
        plt.plot(metric)
        plt.title(title)
        plt.xlabel("Episodes")
        plt.ylabel(ylabel)
    plt.show()


def train_q_learning(game_state: GameState):
    ql = q_learning.QLearning(
        size=min(MAZE_WIDTH, MAZE_HEIGHT), maze=game_state.maze)

    episodes = 500  # You can adjust this value
    steps_per_episode = 200  # Adjust as needed
    for episode in range(episodes):
        state = (
            game_state.start_pos[1] * min(MAZE_WIDTH, MAZE_HEIGHT)) + game_state.start_pos[0]
        epsilon = ql.get_epsilon(episode)
        total_reward, steps = 0, 0

        for step in range(steps_per_episode):
            action = ql.take_action(state, epsilon)
            new_pos = list(game_state.start_pos)
            new_pos[0] += DIRECTIONS[action][0]
            new_pos[1] += DIRECTIONS[action][1]
            reward = -1
            new_state = state
            if (new_pos[0] < 0 or new_pos[0] > min(MAZE_WIDTH, MAZE_HEIGHT) - 1 or new_pos[1] < 0 or new_pos[1] > min(MAZE_WIDTH, MAZE_HEIGHT) - 1):
                reward = -5
                new_state = state
            else:
                new_state = (new_pos[1] * min(MAZE_WIDTH,
                             MAZE_HEIGHT)) + new_pos[0]

                if tuple(new_pos) == game_state.goal_pos:
                    reward = 10
                    new_state = state

                state = new_state

            ql.update_q(state, action, reward, new_state)
            total_reward += reward
            steps += 1
            if tuple(new_pos) == game_state.goal_pos:
                break

        ql.log_performance(total_reward, steps)
    plot_queue.put((ql.reward_history, ql.steps_history))


def main():
    # Initialize core components
    maze_generator = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
    game_state = GameState()
    frontier_exporter = FrontierExporter()  # Create FrontierExporter instance
    algorithm_manager = AlgorithmManager(
        game_state, frontier_exporter
    )  # Use FrontierExporter

    # Initialize UI components
    button_manager = ButtonManager(
        BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_GAP
    )
    game_window = GameWindow(
        SCREEN_WIDTH, SCREEN_HEIGHT, button_manager, game_state, mazeSetup, plot_queue, plot_metrics_main_thread
    )

    # Function to solve maze with the algo and set ui and gamestate values
    def solve_and_update(algorithm_name, algorithm_func, *args):
        game_window.update_title(algorithm_name)
        game_state.reset_path()
        if algorithm_name == "IDS":
            algorithm_manager.solve_algorithm(
                algorithm_name, algorithm_func, game_state)
        else:
            algorithm_manager.solve_algorithm(
                algorithm_name, algorithm_func, *args)

    # Function to create an instance of class and then pass the search to lambda function
    def create_algorithm_and_solve(algorithm_class, algorithm_name, *args):
        def solve():
            instance: BaseSearch = algorithm_class(
                game_state.maze, game_state.start_pos, game_state.goal_pos
            )
            if algorithm_name == "IDS":
                solve_and_update(algorithm_name, instance.search, game_state)
            else:
                solve_and_update(algorithm_name, instance.search, *args)

        return solve

    # Create buttons for each algorithm
    button_manager.add_button(
        "BFS", 0, action=create_algorithm_and_solve(bfs.BreadthFirstSearch, "BFS")
    )
    button_manager.add_button(
        "DFS", 1, action=create_algorithm_and_solve(dfs.DepthFirstSearch, "DFS")
    )
    button_manager.add_button(
        "UCS", 2, action=create_algorithm_and_solve(ucs.UniformCostSearch, "UCS")
    )
    L_BUTTON_WIDTH = BUTTON_WIDTH // 3

    ids_button = button_manager.add_button(
        "IDS",
        3,
        btn_width=L_BUTTON_WIDTH,
        width_offset=L_BUTTON_WIDTH,
        action=create_algorithm_and_solve(
            ids.IterativeDeepeningSearch, "IDS", game_state
        ),
        subtext=str(game_state.l),
    )

    # L button, that is next to IDS
    button_manager.add_button(
        "-",
        3,
        btn_width=L_BUTTON_WIDTH,
        action=lambda: game_state.l_setter(
            game_state.l - 5) or ids_button.set_subtext(game_state.l),
    )
    button_manager.add_button(
        "+",
        3,
        btn_width=L_BUTTON_WIDTH,
        width_offset=L_BUTTON_WIDTH * 2,
        action=lambda: game_state.l_setter(
            game_state.l + 5) or ids_button.set_subtext(game_state.l),
    )

    # Reset path and reset maze buttons
    button_manager.add_button("Reset Path", 11, action=game_state.reset_path)
    button_manager.add_button(
        "Reset Maze", 12, action=lambda: game_state.reset_maze(maze_generator)
    )

    button_manager.add_button(
        "Greedy BFS (Manhattan)",
        4,
        action=create_algorithm_and_solve(
            greedy_bfs.GreedyBestFirstSearch,
            "Greedy BFS (Manhattan)",
            Metrics.manhattan,
        ),
    )
    button_manager.add_button(
        "Greedy BFS (Euclidean)",
        5,
        action=create_algorithm_and_solve(
            greedy_bfs.GreedyBestFirstSearch,
            "Greedy BFS (Euclidean)",
            Metrics.euclidean,
        ),
    )
    button_manager.add_button(
        "A* (Manhattan)",
        6,
        action=create_algorithm_and_solve(
            astar.AStarSearch, "A* (Manhattan)", Metrics.manhattan
        ),
    )
    button_manager.add_button(
        "A* (Euclidean)",
        7,
        action=create_algorithm_and_solve(
            astar.AStarSearch, "A* (Euclidean)", Metrics.euclidean
        ),
    )

    button_manager.add_button(
        "Hill Climbing",
        8,
        action=create_algorithm_and_solve(
            hill_climbing.HillClimbing, "Hill Climbing"),
    )
    button_manager.add_button(
        "Simulated Annealing",
        9,
        action=create_algorithm_and_solve(
            simulated_annealing.SimulatedAnnealing, "Simulated Annealing"
        ),
    )
    button_manager.add_button(
        "Genetic Algorithm",
        10,
        action=lambda: solve_and_update(
            "Genetic Algorithm", genetic_algorithm.genetic_algorithm
        ),
    )

    # Add the button for comparison.
    button_manager.add_button(
        "Compare Algos",
        13,
        action=lambda: showDifferences_ExecutionTime(
            algorithm_manager.compare_algos),
    )

    button_manager.add_button(
        "Q-Learning",
        14,
        action=lambda: threading.Thread(
            target=train_q_learning, args=(game_state,)).start(),
    )

    # Setup initial game state
    game_state.reset_maze(maze_generator)

    # Run the game
    game_window.run()


if __name__ == "__main__":
    main()
