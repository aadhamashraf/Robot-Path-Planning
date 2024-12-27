from src.core.game_state import GameState
from src.core.algorithm_manager import AlgorithmManager
from src.environment.maze_generator import MazeGenerator
from src.ui.button_manager import ButtonManager
from src.ui.game_window import GameWindow
from src.utilities.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_GAP,
    MAZE_WIDTH, MAZE_HEIGHT
)


def main():
    # Initialize core components
    maze_generator = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
    game_state = GameState()
    algorithm_manager = AlgorithmManager(game_state, maze_generator)

    # Initialize UI components
    button_manager = ButtonManager(
        BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_GAP)
    game_window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT,
                             button_manager, game_state, maze_generator)

    # Setup initial game state
    game_state.reset_maze(maze_generator)

    # Run the game
    game_window.run()


if __name__ == "__main__":
    main()
