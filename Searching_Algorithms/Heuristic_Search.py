from Basic_Attributes import *  
from Environment import comparewell

def greedy_bfs(maze, start, goal):
    start_time = time.time()  

    open_list = []  
    heapq.heappush(open_list, (0, start))  
    came_from = {}  
    g_score = {start: 0}  
    frontier = []  
    step_count = 0  

    while open_list:
        _, current = heapq.heappop(open_list)
        step_count += 1  

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()  

            end_time = time.time()  
            elapsed_time = end_time - start_time  

            comparewell.export_frontier(frontier, "Greedy BFS")
            return path, frontier, step_count, elapsed_time  

        x, y = current
        for dx, dy in DIRECTIONS:
            neighbor = (x + dx, y + dy)

            if 0 <= neighbor[0] < MAZE_WIDTH and 0 <= neighbor[1] < MAZE_HEIGHT:
                if maze[neighbor[1]][neighbor[0]] == 0:  

                    h = abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])  

                    if neighbor not in g_score or g_score[neighbor] > g_score[current] + 1:
                        g_score[neighbor] = g_score[current] + 1
                        came_from[neighbor] = current
                        heapq.heappush(open_list, (h, neighbor))

        frontier.append(list(open_list))  

    return path, frontier, step_count, elapsed_time

def a_star(maze, start, goal):
    start_time = time.time()  

    open_list = []  
    heapq.heappush(open_list, (0, start))  
    came_from = {}  
    g_score = {start: 0}  
    f_score = {start: abs(start[0] - goal[0]) + abs(start[1] - goal[1])}  
    frontier = []  
    step_count = 0  

    while open_list:
        _, current = heapq.heappop(open_list)
        step_count += 1  

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()  

            end_time = time.time()  
            elapsed_time = end_time - start_time  

            comparewell.export_frontier(frontier, "A Star")
            return path, frontier, step_count, elapsed_time  

        x, y = current
        for dx, dy in DIRECTIONS:
            neighbor = (x + dx, y + dy)

            if 0 <= neighbor[0] < MAZE_WIDTH and 0 <= neighbor[1] < MAZE_HEIGHT:
                if maze[neighbor[1]][neighbor[0]] == 0:  
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                        came_from[neighbor] = current
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

        frontier.append(list(open_list))  

    return path, frontier, step_count, elapsed_time
