from src.algorithms.base_search import BaseSearch
from typing import Callable


class AStarSearch(BaseSearch):
    def search(self, heuristic: Callable):
        self._start_timer()
        frontier = [(heuristic(self.start, self.goal), self.start)]
        came_from = {self.start: None}
        g_score = {self.start: 0}
        f_score = {self.start: heuristic(self.start, self.goal)}
        explored_states = []

        while frontier:
            frontier.sort(key=lambda x: x[0])
            _, current = frontier.pop(0)
            self.counter += 1

            if current == self.goal:
                return self._reconstruct_path(came_from, current), explored_states, self.counter, self._get_elapsed_time()

            temp = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)

                if self._is_valid_position(nx, ny):
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + \
                            heuristic(neighbor, self.goal)
                        frontier.append((f_score[neighbor], neighbor))
                        temp.append(neighbor)

            explored_states.append(temp)

        return None, explored_states, self.counter, self._get_elapsed_time()

    def _reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        return path[::-1]
