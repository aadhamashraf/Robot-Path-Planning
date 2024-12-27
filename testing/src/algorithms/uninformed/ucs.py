import heapq
from src.algorithms.base_search import BaseSearch


class UniformCostSearch(BaseSearch):
    def search(self):
        self._start_timer()
        visited = set()
        frontier = []
        parent = {self.start: None}
        costs = {self.start: 0}
        heapq.heappush(frontier, (0, self.start))

        while frontier:
            current_cost, current = heapq.heappop(frontier)
            self.counter += 1

            if current in visited:
                continue

            visited.add(current)
            if current == self.goal:
                return self._reconstruct_path(parent, current), frontier, self.counter, self._get_elapsed_time()

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)

                if self._is_valid_position(nx, ny) and neighbor not in visited:
                    new_cost = current_cost + 1
                    if neighbor not in costs or new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        heapq.heappush(frontier, (new_cost, neighbor))
                        parent[neighbor] = current

        return None, frontier, self.counter, self._get_elapsed_time()

    def _reconstruct_path(self, parent, current):
        path = []
        while current is not None:
            path.append(current)
            current = parent[current]
        return path[::-1]
