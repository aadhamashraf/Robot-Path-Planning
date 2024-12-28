from src.core.metrics import Metrics


class AlgorithmManager:
    def __init__(self, game_state, frontier_exporter):
        self.game_state = game_state
        self.frontier_exporter = frontier_exporter
        self.compare_algos = {
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

    def solve_algorithm(self, algorithm_name, algorithm_func, *args):
        if hasattr(algorithm_func, '__self__'):  # Check if it's a bound method (instance method)
            instance = algorithm_func.__self__
            result = instance.search(*args)
        else:  # Else it's a function (such as ids)
            result = algorithm_func(
                self.game_state.maze, self.game_state.start_pos, self.game_state.goal_pos, *args)

        if result is not None:
            self.game_state.path, frontier, self.game_state.step_count, elapsed_time = result
            self.frontier_exporter.export_frontier(frontier, algorithm_name)
            self.compare_algos[algorithm_name] = [
                elapsed_time, self.game_state.step_count]

        else:
            self.game_state.path = None
            self.game_state.step_count = 0
            self.compare_algos[algorithm_name] = [0, 0]
