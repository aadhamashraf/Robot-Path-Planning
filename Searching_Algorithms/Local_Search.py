import math
import random
import time
from Basic_Attributes import *
from Environment import comparewell

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

"""Hill Climbing"""

"""Simulated Annealing"""

# Simulated Annealing Algorithm
def simulated_annealing(maze, start, goal, initial_temperature=100, cooling_rate=0.95, max_iterations=10000):
    startTime = time.time()

    current = start
    path = [current]
    temperature = initial_temperature
    frontier = []
    steps = 0

    def calculate_cost(position):
        """Heuristic cost function: Manhattan distance to the goal."""
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    current_cost = calculate_cost(current)

    for iteration in range(max_iterations):
        steps += 1
        if current == goal:
            break

        neighbors = []
        for dx, dy in DIRECTIONS:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0:
                neighbors.append((nx, ny))

        if not neighbors:
            break  # Dead end, no valid moves

        # Randomly pick a neighbor
        next_position = random.choice(neighbors)
        next_cost = calculate_cost(next_position)

        # Acceptance probability
        delta_cost = next_cost - current_cost
        acceptance_probability = math.exp(-delta_cost / temperature) if delta_cost > 0 else 1

        # Decide whether to accept the move
        if random.random() < acceptance_probability:
            current = next_position
            current_cost = next_cost
            path.append(current)

        frontier.append(list(neighbors))  # Add neighbors to the frontier

        # Cool down the temperature
        temperature *= cooling_rate

        # Stop if temperature is very low
        if temperature < 1e-3:
            break

    endTime = time.time()
    return path, frontier, steps, endTime - startTime

"""Genetic Algorithms"""
