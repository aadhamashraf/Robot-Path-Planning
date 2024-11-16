from Basic_Attributes import *  
from Environment import comparewell  , mazeSetup

def heuristic_manhattan(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def greedy_bfs(maze, start, goal):
    start_time = time.time()
    open_nodes = []
    visited_nodes = set()
    path_from = {}
    exploration_frontier = []  
    step_counter = 0  

    heapq.heappush(open_nodes, (0, start))  
    visited_nodes.add(start)

    while open_nodes:
        cost, current_node = heapq.heappop(open_nodes)  
        step_counter += 1

        if current_node == goal:  
            path = []
            while current_node in path_from:
                path.append(current_node)
                current_node = path_from[current_node]
            path.reverse()

            return path, exploration_frontier, step_counter, time.time() - start_time 

        x, y = current_node

        # DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in DIRECTIONS:
            neighbor_node = (x + dx, y + dy)
            if (0 <= neighbor_node[0] < MAZE_WIDTH) and (0 <= neighbor_node[1] < MAZE_HEIGHT):
                if maze[neighbor_node[1]][neighbor_node[0]] == 0 and neighbor_node not in visited_nodes:
                    visited_nodes.add(neighbor_node)  
                    path_from[neighbor_node] = current_node  
                    heapq.heappush(open_nodes, (heuristic_manhattan(neighbor_node , goal), neighbor_node))  

        exploration_frontier.append([node[1] for node in open_nodes])

    return None, exploration_frontier, step_counter, time.time() - start_time 

def a_star(maze, start, goal):
    start_time = time.time()

    open_nodes = []
    path_from = {}
    g_cost = {start: 0}  
    f_cost = {start: abs(start[0] - goal[0]) + abs(start[1] - goal[1])}  
    visited_nodes = set()  
    exploration_frontier = []  
    step_counter = 0  

    heapq.heappush(open_nodes, (0, start)) 

    while open_nodes:
        cost, current_node = heapq.heappop(open_nodes)  
        step_counter += 1

        if current_node == goal:  
            path = []
            while current_node in path_from:
                path.append(current_node)
                current_node = path_from[current_node]
            path.reverse()  
            return path, exploration_frontier, step_counter, time.time() - start_time

        visited_nodes.add(current_node)  

        x, y = current_node

        # DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in DIRECTIONS:
            neighbor_node = (x + dx, y + dy)

            if 0 <= neighbor_node[0] < MAZE_WIDTH and 0 <= neighbor_node[1] < MAZE_HEIGHT:
                if maze[neighbor_node[1]][neighbor_node[0]] == 0:  
                    tentative_g_cost = g_cost[current_node] + 1  

                    if neighbor_node not in visited_nodes or tentative_g_cost < g_cost.get(neighbor_node, float('inf')):
                        path_from[neighbor_node] = current_node  
                        g_cost[neighbor_node] = tentative_g_cost
                        f_cost[neighbor_node] = tentative_g_cost + heuristic_manhattan(neighbor_node , goal)
                        heapq.heappush(open_nodes, (f_cost[neighbor_node], neighbor_node))  

        exploration_frontier.append([node[1] for node in open_nodes])
    return None, exploration_frontier, step_counter, time.time() - start_time  
