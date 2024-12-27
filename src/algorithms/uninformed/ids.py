from src.algorithms.base_search import BaseSearch


class IterativeDeepeningSearch(BaseSearch):
    def search(self, depth_limit=1):
        self._start_timer()
        frontier = [self.start]
        parent = {self.start: None}

        current = self.start
        while frontier and depth_limit > 0:
            current = frontier.pop()
            self.counter += 1

            if current == self.goal:
                return self._reconstruct_path(parent, current), frontier, self.counter, self._get_elapsed_time()

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if self._is_valid_position(nx, ny) and (nx, ny) not in parent:
                    parent[(nx, ny)] = current
                    frontier.append((nx, ny))
            depth_limit -= 1

        return None, frontier, self.counter, self._get_elapsed_time()

    def _reconstruct_path(self, parent, current):
        path = []
        while current != self.start:
            path.append(current)
            current = parent[current]
        return path[::-1]
