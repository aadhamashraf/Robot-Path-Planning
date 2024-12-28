from src.algorithms.base_search import BaseSearch
from src.core.game_state import GameState


class IterativeDeepeningSearch(BaseSearch):
    def search(self, game_state: GameState):
        self._start_timer()
        frontier = [self.start]
        parent = {self.start: None}
        l = game_state.l  # Get l value from gamestate
        explored_states = []

        current = self.start
        while frontier and l > 0:
            current = frontier.pop()
            self.counter += 1

            if current == self.goal:
                return self._reconstruct_path(parent, current), explored_states, self.counter, self._get_elapsed_time()

            temp = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if self._is_valid_position(nx, ny) and (nx, ny) not in parent:
                    parent[(nx, ny)] = current
                    frontier.append((nx, ny))
                    temp.append((nx, ny))

            explored_states.append(temp)
            l -= 5
        game_state.l += 5
        return (
            self._reconstruct_path(parent, current),
            frontier,
            self.counter,
            self._get_elapsed_time(),
        )
        return None, frontier, self.counter, self._get_elapsed_time()

    def _reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        return path[::-1]
