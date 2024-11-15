import math
import random
import time
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

"""Hill Climbing"""

"""Simualted Annealing"""


# Probability function
def probability(deltaE, T):
    k = 1e-2  # Boltzmann constant
    exp = -deltaE / (k * T)
    return math.e ** exp

# Simulated Annealing search algorithm


def simulated_annealing(start, goal, grid):
    startTime = time.time()  # Start timing
    current = start
    parent = {start: None}  # Track parent nodes
    frontier = set()
    steps = 0  # Step counter
    T = 100  # Initial temperature
    T_min = 1e-3  # Minimum temperature
    alpha = 0.9  # Cooling rate

    while T > T_min:
        steps += 1
        frontier.add(current)

        # Choose a random direction
        i, j = random.choice(DIRECTIONS)
        next_node = (current[0] + i, current[1] + j)

        # Check if the next node is valid
        if 0 <= next_node[0] < len(grid[0]) and 0 <= next_node[1] < len(grid) and not grid[next_node[1]][next_node[0]].walls[(i + 2) % 4]:
            if next_node not in parent:  # Check if node is already visited
                deltaE = 1  # Example energy difference; can vary based on the problem

                # Decide to move based on probability
                if deltaE < 0 or random.random() < probability(deltaE, T):
                    parent[next_node] = current
                    current = next_node
                    if current == goal:
                        break

        T *= alpha  # Reduce the temperature

    # Reconstruct the path using the parent dictionary
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent.get(current)
        if current is None:
            break
    path.append(start)

    endTime = time.time()  # End timing
    return path[::-1], frontier, steps, endTime - startTime


"""Genetic Algorithms"""
