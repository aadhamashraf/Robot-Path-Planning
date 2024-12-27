from src.algorithms.base_search import BaseSearch


class DepthFirstSearch(BaseSearch):
    def search(self):
        self._start_timer()
        stack = [self.start]
        parent = {self.start: None}
        frontier = set()

        while stack:
            current = stack.pop()
            frontier.add(current)
            self.counter += 1

            if current == self.goal:
                return self._reconstruct_path(parent), frontier, self.counter, self._get_elapsed_time()

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if self._is_valid_position(nx, ny) and (nx, ny) not in parent:
                    parent[(nx, ny)] = current
                    stack.append((nx, ny))

        return None, frontier, self.counter, self._get_elapsed_time()

    def _reconstruct_path(self, parent):
        path = []
        current = self.goal
        while current != self.start:
            path.append(current)
            current = parent[current]
        return path[::-1]
