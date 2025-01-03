class GameState:
    def __init__(self):
        self.maze = None
        self.start_pos = None
        self.goal_pos = None
        self.path = None
        self.step_count = 0
        self.elapsed_time = 0
        self.l = 5  # For IDS algorithm

    def reset_path(self):
        self.path = None

    def reset_maze(self, maze_generator):
        self.maze, self.start_pos, self.goal_pos = maze_generator.create_maze()
        self.path = None
        self.l = 5

    def l_setter(self, value):
        print(self.l)
        self.l = value
