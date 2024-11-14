import math
import random
from main import DIRECTIONS
import time

"""Hill Climbing"""

"""Simualted Annealing"""


def probability(deltaE, T):
    k = 1e-2
    exp = -deltaE / (k * T)
    return math.e ** exp


def simulated_annealing(start, goal, grid):
    startTime = time.time()
    current = start
    path = [current]
    frontier = set()
    steps = 0
    T = 100
    T_min = 1e-3
    alpha = 0.9
    while T > T_min:
        steps += 1
        frontier.add(current)
        i, j = random.choice(DIRECTIONS)
        next = (current[0] + i, current[1] + j)
        # moving condition
        if 0 <= next[0] < len(grid[0]) and 0 <= next[1] < len(grid) and not grid[next[1]][next[0]].walls[(i + 2) % 4]:
            path.append(next)
            if next == goal:
                break
            delatE = 1
            if delatE < 0:
                current = next
            else:
                if random.random() < probability(delatE, T):
                    current = next
        T *= alpha
    endTime = time.time()
    return path, frontier, steps, endTime - startTime


"""Genetic Algorithms"""
