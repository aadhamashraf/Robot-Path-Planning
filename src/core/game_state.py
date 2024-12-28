class GameState:
    def __init__(self):
        self.maze = None
        self.start_pos = None
        self.goal_pos = None
        self.path = None
        self.step_count = 0
        self.elapsed_time = 0
        self.l = 1  # For IDS algorithm

    def reset_path(self):
        self.path = None

    def reset_maze(self, maze_generator):
        self.maze, self.start_pos, self.goal_pos = maze_generator.create_maze()
        self.path = None
        self.l = 1

    def l_setter(self, value):
        self.l = value
