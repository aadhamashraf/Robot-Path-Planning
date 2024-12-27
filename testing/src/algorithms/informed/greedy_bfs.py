from src.algorithms.base_search import BaseSearch
from typing import Callable


class GreedyBestFirstSearch(BaseSearch):
    def search(self, heuristic: Callable):
        self._start_timer()
        frontier = [(heuristic(self.start, self.goal), self.start)]
        visited = set([self.start])
        parent = {self.start: None}
        explored_states = []

        while frontier:
            frontier.sort(key=lambda x: x[0])
            _, current = frontier.pop(0)
            self.counter += 1

            if current == self.goal:
                return self._reconstruct_path(parent, current), explored_states, self.counter, self._get_elapsed_time()

            temp = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)

                if self._is_valid_position(nx, ny) and neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    frontier.append((heuristic(neighbor, self.goal), neighbor))
                    temp.append(neighbor)

            explored_states.append(temp)

        return None, explored_states, self.counter, self._get_elapsed_time()

    def _reconstruct_path(self, parent, current):
        path = []
        while current in parent:
            path.append(current)
            current = parent[current]
        return path[::-1]
