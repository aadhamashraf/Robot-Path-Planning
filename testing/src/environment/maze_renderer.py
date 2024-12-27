import pygame
from typing import List, Tuple, Optional


class MazeRenderer:
    def __init__(self, cell_size: int):
        self.cell_size = cell_size
        self.robot_img = self._load_and_scale_image("robot.png")
        self.flag_img = self._load_and_scale_image("flag.jpg")

    def _load_and_scale_image(self, filename: str) -> pygame.Surface:
        img = pygame.image.load(f"Environment/assets/{filename}")
        return pygame.transform.scale(img, (40, 40))

    def draw_grid(self, screen: pygame.Surface, maze: List[List[int]],
                  start: Tuple[int, int], goal: Tuple[int, int],
                  path: Optional[List[Tuple[int, int]]] = None) -> None:
        self._draw_walls(screen, maze)
        self._draw_path(screen, path)
        self._draw_markers(screen, start, goal)

    def _draw_walls(self, screen: pygame.Surface, maze: List[List[int]]) -> None:
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, (0, 0, 0),  # BLACK
                                     (x * self.cell_size, y * self.cell_size,
                                      self.cell_size, self.cell_size))

    def _draw_path(self, screen: pygame.Surface,
                   path: Optional[List[Tuple[int, int]]]) -> None:
        if path:
            for (x, y) in path:
                pygame.draw.rect(screen, (0, 255, 0),  # GREEN
                                 (x * self.cell_size, y * self.cell_size,
                                  self.cell_size - 5, self.cell_size - 5))

    def _draw_markers(self, screen: pygame.Surface, start: Tuple[int, int],
                      goal: Tuple[int, int]) -> None:
        offset = (self.cell_size - 40) // 2
        screen.blit(self.robot_img,
                    (start[0] * self.cell_size + offset,
                     start[1] * self.cell_size + offset))
        screen.blit(self.flag_img,
                    (goal[0] * self.cell_size + offset,
                     goal[1] * self.cell_size + offset))
