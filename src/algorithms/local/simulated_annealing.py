import random
import math
from src.algorithms.base_search import BaseSearch
from src.utilities.metrics import manhattan_distance


class SimulatedAnnealing(BaseSearch):
    def search(self, initial_temp=1000.0, cooling_rate=1.0):
        self._start_timer()
        current = self.start
        current_cost = manhattan_distance(current, self.goal)
        temperature = initial_temp
        path = [current]

        while temperature > 1:
            self.counter += 1
            neighbors = []

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if self._is_valid_position(nx, ny):
                    neighbors.append((nx, ny))

            if not neighbors:
                break

            next_node = random.choice(neighbors)
            next_cost = manhattan_distance(next_node, self.goal)

            delta_cost = next_cost - current_cost
            acceptance_probability = math.exp(-delta_cost /
                                              temperature) if delta_cost > 0 else 1.0

            if random.random() < acceptance_probability:
                current = next_node
                current_cost = next_cost
                path.append(current)

            if current == self.goal:
                return path, [], self.counter, self._get_elapsed_time()

            temperature *= cooling_rate

        return None, [], self.counter, self._get_elapsed_time()
