from main import DIRECTIONS
from main import deque

""" BFS Algorithm """
def bfs(start, goal, grid):
    queue = deque([start])
    parent = {start: None}
    frontier = set()
    steps = 0
    while queue:
        current = queue.popleft()
        frontier.add(current)
        steps += 1
        if current == goal:
            break
        for i, (dx, dy) in enumerate(DIRECTIONS):
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and not grid[ny][nx].walls[(i + 2) % 4]:
                if (nx, ny) not in parent:
                    parent[(nx, ny)] = current
                    queue.append((nx, ny))
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]
    return path[::-1], frontier, steps

""" DFS Algorithm """
def dfs(start, goal, grid):
    stack = [start]
    parent = {start: None}
    frontier = set()
    steps = 0

    while stack:
        current = stack.pop()
        frontier.add(current)
        steps += 1
        if current == goal:
            break
        for i, (dx, dy) in enumerate(DIRECTIONS):
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and not grid[ny][nx].walls[(i + 2) % 4]:
                if (nx, ny) not in parent:
                    parent[(nx, ny)] = current
                    stack.append((nx, ny))

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]
    return path[::-1], frontier, steps 

""" UCS Algorithm """

""" IDS Algorithm """