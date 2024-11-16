from Basic_Attributes import *

# BFS Algorithm


def bfs(maze, start, goal):
    startTime = time.time()
    visited = [[False] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
    queue = deque([start])
    parent = {start: None}

    visited[start[1]][start[0]] = True

    steps = 0
    while queue:
        x, y = queue.popleft()
        print(f"Exploring BFS: ({x}, {y})")
        steps += 1
        # DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and not visited[ny][nx] and maze[ny][nx] == 0:
                visited[ny][nx] = True
                queue.append((nx, ny))
                parent[(nx, ny)] = (x, y)
            if (x, y) == goal:
                endTime = time.time()
                path = []
                while parent[(x, y)] is not None:
                    path.append((x, y))
                    x, y = parent[(x, y)]
                path.append(start)

                return path[::-1], queue, steps, endTime-startTime
    return None

# DFS Algorithm


def dfs(maze, start, goal):
    startTime = time.time()
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
        for dx, dy in (DIRECTIONS):
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0:
                if (nx, ny) not in parent:
                    parent[(nx, ny)] = current
                    stack.append((nx, ny))

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]
    endTime = time.time()
    return path[::-1], frontier, steps, endTime-startTime

# IDS Algorithm


def ids(maze, start, goal, l=1):
    startTime = time.time()
    frontier = [start]
    parent = {start: None}
    steps = 0
    current = 0
    while frontier:
        current = frontier.pop()
        steps += 1
        if current == goal:
            break
        if l == 0:
            break
        for i, (dx, dy) in enumerate(DIRECTIONS):
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0:
                if (nx, ny) not in parent:
                    parent[(nx, ny)] = current
                    frontier.append((nx, ny))
        l -= 1
    path = []

    while current != start:
        path.append(current)
        current = parent[current]
    endTime = time.time()
    return path[::-1], frontier, steps, endTime-startTime
# UCS Algorithm


def ucs(maze, start, goal):
    startTime = time.time()
    visited = set()
    frontier = []
    parent = {start: None}
    costs = {start: 0}
    heapq.heappush(frontier, (0, start))
    steps = 0

    while frontier:
        current_cost, current = heapq.heappop(frontier)
        steps += 1
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            endTime = time.time()
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1], frontier, steps, endTime - startTime
        for dx, dy in DIRECTIONS:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            if (0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0 and neighbor not in visited):
                new_cost = current_cost + 1
                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))
                    parent[neighbor] = current
    return None, frontier, steps, time.time() - startTime
