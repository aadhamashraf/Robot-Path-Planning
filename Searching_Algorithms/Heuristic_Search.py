from Basic_Attributes import *
from Environment import comparewell, mazeSetup


# def manhattan_metric(a, b):
#     x = abs(a[0] - b[0])
#     y = abs(a[1] - b[1])
#     return x + y

# def eclduien_metric(a, b):
#     x = pow(a[0] - b[0] , 2)
#     y = pow(a[1] - b[1] , 2)
#     return math.sqrt(x + y)

def greedy_bfs(grid, start, goal , metric):
    started = time.time()
    priorityqueue, at, es, visited = [], {}, [], set()
    counter = 0
    priorityqueue.append((0, start))
    visited.add(start)

    while (priorityqueue):
        priorityqueue.sort(key=lambda x: x[0])
        cost, n = priorityqueue.pop(0)
        temp = []
        counter += 1

        if (n == goal):
            p = []
            while (n in at):
                p.append(n)
                n = at[n]
            p.append(start)
            return p[::-1], es, counter, time.time() - started

        x = n[0]
        y = n[1]

        for di in DIRECTIONS:
            nei_x = x + di[0]
            nei_y = y + di[1]
            nei = (nei_x, nei_y)

            within_x = (0 <= nei_x < len(grid[0]))
            within_y = (0 <= nei_y < len(grid))

            if (within_x and within_y):
                is_walkable = grid[nei_y][nei_x] == 0
                is_not_visited = nei not in visited

                if (is_walkable and is_not_visited):
                    visited.add(nei)
                    at[nei] = n
                    priorityqueue.append((metric(nei, goal), nei))

        for node in priorityqueue:
            temp.append(node[-1])
        es.append(temp)

    return None, es, counter, time.time() - started


def a_star(grid, start, goal , metric):
    t = time.time()
    priorityqueue, am, tc, pc, vl, tj = [], {}, {start: 0}, {
        start: metric(start, goal)}, set(), []
    counter = 0
    priorityqueue.append((0, start))

    while priorityqueue:
        priorityqueue.sort(key=lambda x: x[0])
        cost, n = priorityqueue.pop(0)
        counter += 1

        if n == goal:
            p = []
            while n in am:
                p.append(n)
                n = am[n]
            p.append(start)
            return p[::-1], tj, counter, time.time() - t

        vl.add(n)
        x = n[0]
        y = n[1]

        for di in DIRECTIONS:
            nei_x = x + di[0]
            nei_y = y + di[1]
            nei = (nei_x, nei_y)

            within_x = 0 <= nei_x < len(grid[0])
            within_y = 0 <= nei_y < len(grid)

            if within_x and within_y:
                is_walkable = grid[nei_y][nei_x] == 0

                if is_walkable:
                    ic = tc[n] + 1
                    if nei not in vl or ic < tc.get(nei, float('inf')):
                        am[nei] = n
                        tc[nei] = ic
                        pc[nei] = ic + metric(nei, goal)
                        priorityqueue.append((pc[nei], nei))

        temp = []
        for i in priorityqueue:
            temp.append(i[1])
        tj.append(temp)

    return None, tj, counter, time.time() - t
