from src.algorithms.base_search import BaseSearch
from src.utilities.metrics import manhattan_distance


class HillClimbing(BaseSearch):
    def search(self):
        self._start_timer()
        current = self.start
        visited = {self.start}
        path = [current]
        frontier = {self.start}
        stack = []

        while current != self.goal:
            self.counter += 1
            neighbors = []

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if self._is_valid_position(nx, ny) and (nx, ny) not in visited:
                    neighbors.append((nx, ny))

            if neighbors:
                current_distance = manhattan_distance(current, self.goal)
                better_neighbors = [n for n in neighbors
                                    if manhattan_distance(n, self.goal) < current_distance]

                if better_neighbors:
                    next_pos = min(better_neighbors,
                                   key=lambda n: manhattan_distance(n, self.goal))
                else:
                    next_pos = min(neighbors,
                                   key=lambda n: manhattan_distance(n, self.goal))

                stack.append(current)
                current = next_pos
                visited.add(current)
                frontier.add(current)
                path.append(current)
            else:
                if stack:
                    current = stack.pop()
                    while path[-1] != current:
                        path.pop()
                else:
                    return None, frontier, self.counter, self._get_elapsed_time()

            if self.counter > len(self.maze) * len(self.maze[0]) * 2:
                return None, frontier, self.counter, self._get_elapsed_time()

        return path, frontier, self.counter, self._get_elapsed_time()
