import random
from typing import Tuple, List


class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def create_maze(self) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
        while True:
            maze = [[1 for _ in range(self.width)] for _ in range(self.height)]

            start_x = random.randint(0, self.width // 4)
            start_y = random.randint(0, self.height // 4)
            goal_x = random.randint(3 * self.width // 4, self.width - 1)
            goal_y = random.randint(3 * self.height // 4, self.height - 1)

            maze[start_y][start_x] = 0
            maze[goal_y][goal_x] = 0

            if self._generate_paths(maze, start_x, start_y):
                self._add_random_paths(maze)
                start = (start_x, start_y)
                goal = (goal_x, goal_y)
                if self._is_solvable(maze, start, goal):
                    return maze, start, goal

    def _generate_paths(self, maze: List[List[int]], start_x: int, start_y: int) -> bool:
        stack = [(start_x, start_y)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while stack:
            current_x, current_y = stack[-1]
            neighbors = []

            for dx, dy in directions:
                nx, ny = current_x + dx * 2, current_y + dy * 2
                if (0 <= nx < self.width and 0 <= ny < self.height and
                        maze[ny][nx] == 1):
                    neighbors.append((nx, ny))

            if neighbors:
                next_x, next_y = random.choice(neighbors)
                maze[next_y][next_x] = 0
                maze[current_y + (next_y - current_y) //
                     2][current_x + (next_x - current_x) // 2] = 0
                stack.append((next_x, next_y))
            else:
                stack.pop()

        return True

    def _add_random_paths(self, maze: List[List[int]]) -> None:
        for _ in range(random.randint(50, 100)):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            maze[y][x] = 0

    def _is_solvable(self, maze: List[List[int]], start: Tuple[int, int],
                     goal: Tuple[int, int]) -> bool:
        from src.algorithms.uninformed.bfs import BreadthFirstSearch
        bfs = BreadthFirstSearch(maze, start, goal)
        path, _, _, _ = bfs.search()
        return path is not None
