<<<<<<< HEAD
import math
import random
import time
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
=======
from Basic_Attributes import * 
>>>>>>> 13dae46523ddcaa7a8216d4c3bff890f40393ea4

"""Hill Climbing"""

"""Simualted Annealing"""

<<<<<<< HEAD

# Probability function
def probability(deltaE, T):
    k = 1e-2  # Boltzmann constant
    return math.exp(-deltaE / (k * T))

# Simulated Annealing algorithm for grid-based pathfinding


def simulated_annealing(start, goal, grid, n_iterations=1000, temp=1000):
    start_time = time.time()
    current = start
    best = current
    parent = {start: None}
    frontier = {start}
    steps = 0
    curr_eval = abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    for i in range(n_iterations):
        steps += 1
        i, j = random.choice(DIRECTIONS)
        next_node = (current[0] + i, current[1] + j)

        if (
            0 <= next_node[0] < len(grid[0]) and
            0 <= next_node[1] < len(grid) and
            # Assuming 0 is free, 1 is wall
            grid[next_node[1]][next_node[0]] == 0
        ):
            candidate_eval = abs(
                next_node[0] - goal[0]) + abs(next_node[1] - goal[1])
            deltaE = candidate_eval - curr_eval

            T = temp / float(i + 1)  # Cooling schedule
            if deltaE < 0 or random.random() < probability(deltaE, T):
                current = next_node
                curr_eval = candidate_eval
                parent[next_node] = best
                frontier.add(next_node)

            if candidate_eval < abs(best[0] - goal[0]) + abs(best[1] - goal[1]):
                best = next_node

            if current == goal:
                break

    path = []
    node = best
    while node:
        path.append(node)
        node = parent.get(node)

    end_time = time.time()
    return path[::-1], frontier, steps, end_time - start_time


=======
>>>>>>> 13dae46523ddcaa7a8216d4c3bff890f40393ea4
"""Genetic Algorithms"""
