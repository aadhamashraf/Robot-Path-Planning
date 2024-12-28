from abc import ABC, abstractmethod
from typing import Tuple, List, Set, Optional
import time


class BaseSearch(ABC):
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.start_time = 0
        self.counter = 0

    def _start_timer(self):
        self.start_time = time.time()

    def _get_elapsed_time(self):
        return time.time() - self.start_time

    @abstractmethod
    def search(self) -> Tuple[Optional[List], Set, int, float]:
        """Returns: (path, frontier, steps, elapsed_time)"""
        pass

    def _is_valid_position(self, x: int, y: int) -> bool:
        return (0 <= x < len(self.maze[0]) and
                0 <= y < len(self.maze) and
                self.maze[y][x] == 0)
