import pygame
import random
CELL_SIZE = 20
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True]

    def draw(self, screen, color=(0, 0, 0)):
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE
        if self.walls[0]:
            pygame.draw.line(screen, color, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]:
            pygame.draw.line(screen, color, (x + CELL_SIZE, y),
                             (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]:
            pygame.draw.line(screen, color, (x, y + CELL_SIZE),
                             (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[3]:
            pygame.draw.line(screen, color, (x, y), (x, y + CELL_SIZE), 2)


def generate_maze(grid, start_cell):
    stack = [start_cell]
    start_cell.visited = True
    while stack:
        current = stack[-1]
        neighbors = []
        for i, (dx, dy) in enumerate(DIRECTIONS):
            nx, ny = current.x + dx, current.y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and not grid[ny][nx].visited:
                neighbors.append((grid[ny][nx], i))
        if neighbors:
            neighbor, direction = random.choice(neighbors)
            current.walls[direction] = False
            neighbor.walls[(direction + 2) % 4] = False
            neighbor.visited = True
            stack.append(neighbor)
        else:
            stack.pop()

def export_frontier(frontier , algorithm):
    dir = rf"{os.getcwd()}\Forntier Results" 

    if not os.path.exists(dir):
        os.mkdir(dir)
    
    with open(os.path.join(dir, f"frontier_{algorithm}.txt"), "w") as f:
        for node in frontier:
            f.write(f"{node}\n")

def draw_button(screen, text, x, y, width, height):
    font = pygame.font.Font(None, 20)
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x, y, width, height), 2)
    
    if ' ' in text: 
        lines = text.split(' ', 1)
        line1 = font.render(lines[0], True, BLACK)
        line2 = font.render(lines[1], True, BLACK)
        screen.blit(line1, (x + (width - line1.get_width()) // 2, y + 5))
        screen.blit(line2, (x + (width - line2.get_width()) // 2, y + height // 2 + 5))
    else:
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

def draw_path(path):
    for node in path:
        pygame.draw.rect(screen, GREEN, (node[0] * CELL_SIZE, node[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def showDifferences_ExcutionTime(compareAlgos) :
    plt.bar(compareAlgos.index , compareAlgos.values , marker = 'o' , linestyle = "-")
    plt.xlabel("Searching Algorithm")
    plt.xticks(rotation = 90)
    plt.ylabel ("Excution Time")
    plt.grid(True)
    plt.show()
