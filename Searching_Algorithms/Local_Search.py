import math
import random
import time
from Basic_Attributes import *
from Environment import comparewell

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

"""Hill Climbing"""

"""Simulated Annealing"""

# Probability function


def probability(deltaE, T):
    k = 1e-2  # Boltzmann constant
    return math.exp(-deltaE / (k * T))


def simulated_annealing(maze, start, goal, n_iterations=1000, temp=1000):
    start_time = time.time()  # Track the start time

    current = start  # Current position
    best = start  # Best position found so far
    came_from = {start: None}  # To reconstruct the path
    frontier = []  # Store visited nodes for visualization
    step_count = 0  # Number of steps taken

    # Manhattan distance to goal
    current_eval = abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    for iteration in range(n_iterations):
        step_count += 1  # Increment step count
        dx, dy = random.choice(DIRECTIONS)  # Random direction
        # Calculate neighbor position
        neighbor = (current[0] + dx, current[1] + dy)

        # Ensure the neighbor is within bounds and not a wall
        if 0 <= neighbor[0] < MAZE_WIDTH and 0 <= neighbor[1] < MAZE_HEIGHT:
            if maze[neighbor[1]][neighbor[0]] == 0:  # 0 indicates free space
                neighbor_eval = abs(
                    # Evaluation
                    neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])

                delta_e = neighbor_eval - current_eval  # Change in evaluation
                temperature = temp / (iteration + 1)  # Cooling schedule

                # Accept new state if it improves or with probability
                if delta_e < 0 or random.random() < probability(delta_e, temperature):
                    current = neighbor
                    current_eval = neighbor_eval
                    came_from[neighbor] = current  # Track parent node
                    # Add to frontier for visualization
                    frontier.append(neighbor)

                # Update best position found
                if neighbor_eval < abs(best[0] - goal[0]) + abs(best[1] - goal[1]):
                    best = neighbor

                # Stop if the goal is reached
                if current == goal:
                    break

    # Reconstruct the path from best position
    path = []
    while best in came_from:
        path.append(best)
        best = came_from[best]
    path.reverse()  # Reverse to get the correct order

    end_time = time.time()  # Track the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time

    comparewell.export_frontier(
        frontier, "Simulated Annealing")  # Export frontier
    return path, frontier, step_count, elapsed_time


"""Genetic Algorithms"""
