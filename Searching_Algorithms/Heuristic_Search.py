import time
import heapq
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


'''Greedy Best-First Search'''

'''A*'''
def a_star(start, goal, grid):
    startTime = time.time()
    open_set = []
    heapq.heappush(open_set, (0, start))
    parent = {start: None}
    g_cost = {start: 0}
    frontier = set()
    steps = 0

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    while open_set:
        _, current = heapq.heappop(open_set)
        frontier.add(current)
        steps += 1
        if current == goal:
            break

        for i, (dx, dy) in enumerate(DIRECTIONS):
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and not grid[ny][nx].walls[(i + 2) % 4]:
                tentative_g = g_cost[current] + 1
                if (nx, ny) not in g_cost or tentative_g < g_cost[(nx, ny)]:
                    g_cost[(nx, ny)] = tentative_g
                    f_cost = tentative_g + heuristic((nx, ny), goal)
                    heapq.heappush(open_set, (f_cost, (nx, ny)))
                    parent[(nx, ny)] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]
    endTime = time.time()
    return path[::-1], frontier, steps, endTime-startTime
