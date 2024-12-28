from src.utilities.constants import *
from src.algorithms.uninformed import bfs


def is_solvable(maze, start, goal):
    return True if bfs(maze, start, goal) else False


def create_maze():
    while True:
        maze = [[1 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]

        start_x = random.randint(0, MAZE_WIDTH // 4)
        start_y = random.randint(0, MAZE_HEIGHT // 4)
        goal_x = random.randint(3 * MAZE_WIDTH // 4, MAZE_WIDTH - 1)
        goal_y = random.randint(3 * MAZE_HEIGHT // 4, MAZE_HEIGHT - 1)

        maze[start_y][start_x] = 0
        maze[goal_y][goal_x] = 0

        stack = [(start_x, start_y)]
        while stack:
            current_x, current_y = stack[-1]
            neighbors = []
            for dx, dy in DIRECTIONS:
                nx, ny = current_x + dx * 2, current_y + dy * 2
                if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 1:
                    neighbors.append((nx, ny))
            if neighbors:
                next_x, next_y = random.choice(neighbors)
                maze[next_y][next_x] = 0
                maze[current_y + (next_y - current_y) // 2][
                    current_x + (next_x - current_x) // 2
                ] = 0
                stack.append((next_x, next_y))
            else:
                stack.pop()

        for _ in range(random.randint(50, 100)):
            random_x = random.randint(1, MAZE_WIDTH - 2)
            random_y = random.randint(1, MAZE_HEIGHT - 2)
            maze[random_y][random_x] = 0

        start, goal = (start_x, start_y), (goal_x, goal_y)
        if is_solvable(maze, start, goal):
            return maze, start, goal


def draw_grid(screen, maze, start, goal, path=None):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(
                    screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
    base_path = os.path.dirname(__file__)
    robot_path = os.path.join(base_path, "./assets/robot.png")
    flag_path = os.path.join(base_path, "./assets/flag.jpg")
    robot_img = pygame.image.load(robot_path)
    flag_img = pygame.image.load(flag_path)

    robot_img = pygame.transform.scale(robot_img, (40, 40))
    flag_img = pygame.transform.scale(flag_img, (40, 40))
    screen.blit(
        robot_img,
        (
            start[0] * CELL_SIZE + (CELL_SIZE - 40) // 2,
            start[1] * CELL_SIZE + (CELL_SIZE - 40) // 2,
        ),
    )
    screen.blit(
        flag_img,
        (
            goal[0] * CELL_SIZE + (CELL_SIZE - 40) // 2,
            goal[1] * CELL_SIZE + (CELL_SIZE - 40) // 2,
        ),
    )
    if path:
        for x, y in path:
            pygame.draw.rect(
                screen,
                GREEN,
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 5, CELL_SIZE - 5),
            )
