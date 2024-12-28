from collections import deque
from src.algorithms.base_search import BaseSearch


class BreadthFirstSearch(BaseSearch):
    def search(self):
        self._start_timer()
        visited = [[False] * len(self.maze[0]) for _ in range(len(self.maze))]
        queue = deque([self.start])
        parent = {self.start: None}

        visited[self.start[1]][self.start[0]] = True

        while queue:
            x, y = queue.popleft()
            self.counter += 1

            if (x, y) == self.goal:
                return self._reconstruct_path(parent, x, y), queue, self.counter, self._get_elapsed_time()

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if self._is_valid_position(nx, ny) and not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((nx, ny))
                    parent[(nx, ny)] = (x, y)

        return None, queue, self.counter, self._get_elapsed_time()

    def _reconstruct_path(self, parent, x, y):
        path = []
        while parent[(x, y)] is not None:
            path.append((x, y))
            x, y = parent[(x, y)]
        path.append(self.start)
        return path[::-1]
