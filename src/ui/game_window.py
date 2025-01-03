import matplotlib.pyplot as plt
import queue
import src.environment.mazeSetup as maze_setup
from src.core.metrics import Metrics
import pygame


class GameWindow:
    def __init__(self, screen_width, screen_height, button_manager, game_state, maze_setup):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()  # Initialize the font module
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.button_manager = button_manager
        self.game_state = game_state
        self.maze_setup = maze_setup
        self.font = pygame.font.Font(None, 24)  # Initialize font

        self._setup_audio()

    def _setup_audio(self):
        pygame.mixer.music.load(
            r"src\\environment\\assets\\01. Ground Theme.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1, 0.0)

    def update_title(self, task):
        pygame.display.set_caption(f"Solving with {task} Algorithm")

    def run(self):
        running = True
        while running:
            running = self._handle_events()
            self._draw()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.button_manager.handle_click(pygame.mouse.get_pos())
        return True

    def _draw(self):
        self.screen.fill((255, 255, 255))  # WHITE
        self.maze_setup.draw_grid(
            self.screen,
            self.game_state.maze,
            self.game_state.start_pos,
            self.game_state.goal_pos,
            self.game_state.path
        )
        self._draw_l_value()
        self.button_manager.draw_all(self.screen)
        pygame.display.flip()

    def _draw_l_value(self):
        l_text = self.font.render(
            f"Explored Nodes: {self.game_state.l}", True, (0, 0, 0)  # Black
        )
        self.screen.blit(l_text, (10, 10))  # Adjust position as needed
