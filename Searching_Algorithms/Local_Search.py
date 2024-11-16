import math
import random
import time
from Basic_Attributes import *
from Environment import comparewell

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

"""Hill Climbing"""


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def hill_climbing(maze, start, goal):
    startTime = time.time()
    current = start
    visited = set([start])
    path = [current]
    frontier = set([start])
    steps = 0
    stack = []

    while current != goal:
        steps += 1
        neighbors = []
        for dx, dy in DIRECTIONS:
            nx, ny = current[0] + dx, current[1] + dy
            if (0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and
                    maze[ny][nx] == 0 and (nx, ny) not in visited):
                neighbors.append((nx, ny))

        if len(neighbors) > 0:
            current_distance = manhattan_distance(current, goal)

            better_neighbors = []
            for n in neighbors:
                if manhattan_distance(n, goal) < current_distance:
                    better_neighbors.append(n)

            if len(better_neighbors) > 0:
                next_pos = better_neighbors[0]
                min_distance = manhattan_distance(next_pos, goal)
                for n in better_neighbors:
                    distance = manhattan_distance(n, goal)
                    if distance < min_distance:
                        next_pos = n
                        min_distance = distance
            else:
                next_pos = neighbors[0]
                min_distance = manhattan_distance(next_pos, goal)
                for n in neighbors:
                    distance = manhattan_distance(n, goal)
                    if distance < min_distance:
                        next_pos = n
                        min_distance = distance

            stack.append(current)
            current = next_pos
            visited.add(current)
            frontier.add(current)
            path.append(current)
        else:
            if len(stack) > 0:
                current = stack.pop()
                while path[-1] != current:
                    path.pop()
            else:
                return None, frontier, steps, time.time() - startTime

        if steps > MAZE_WIDTH * MAZE_HEIGHT * 2:
            return None, frontier, steps, time.time() - startTime

    endTime = time.time()
    return path, frontier, steps, endTime - startTime


"""Simulated Annealing"""


def simulated_annealing(maze, start, goal):
    def calculate_cost(position):
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    start_time = time.time()
    current = start
    current_cost = calculate_cost(current)
    temperature = 1000.0
    cooling_rate = 1.0
    path = [current]
    steps = 0

    while temperature > 1:
        steps += 1

        neighbors = []
        for dx, dy in DIRECTIONS:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0:
                neighbors.append((nx, ny))

        if not neighbors:
            break

        next_node = random.choice(neighbors)
        next_cost = calculate_cost(next_node)

        delta_cost = next_cost - current_cost
        acceptance_probability = math.exp(-delta_cost /
                                          temperature) if delta_cost > 0 else 1.0

        if random.random() < acceptance_probability:
            current = next_node
            current_cost = next_cost
            path.append(current)

        if current == goal:
            end_time = time.time()
            return path, [], steps, end_time - start_time

        temperature *= cooling_rate

    end_time = time.time()
    return None, [], steps, end_time - start_time


"""Genetic Algorithms"""


def genetic_algorithm(maze, start, goal, population_size=500, generations=1000, mutation_rate=0.1):
    def fitness(individual):
        """Calculate fitness as the negative distance to the goal."""
        position = simulate_path(individual)
        return -abs(position[0] - goal[0]) - abs(position[1] - goal[1])

    def simulate_path(individual):
        """Simulate the path the individual takes based on its genome."""
        position = list(start)
        for move in individual:
            nx, ny = position[0] + \
                DIRECTIONS[move][0], position[1] + DIRECTIONS[move][1]
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0:
                position = [nx, ny]
            if tuple(position) == goal:
                break
        return tuple(position)

    def create_individual():
        """Generate a random sequence of moves."""
        return [random.randint(0, len(DIRECTIONS) - 1) for _ in range(50)]

    def crossover(parent1, parent2):
        """Perform crossover between two parents."""
        pivot = random.randint(1, len(parent1) - 1)
        return parent1[:pivot] + parent2[pivot:]

    def mutate(individual):
        """Mutate an individual with a given probability."""
        return [
            random.randint(0, len(DIRECTIONS) -
                           1) if random.random() < mutation_rate else move
            for move in individual
        ]

    start_time = time.time()

    population = [create_individual() for _ in range(population_size)]

    best_individual = None
    best_fitness = float('-inf')

    for generation in range(generations):
        fitness_scores = [(fitness(individual), individual)
                          for individual in population]

        fitness_scores.sort(reverse=True)
        population = [individual for _, individual in fitness_scores]

        if fitness_scores[0][0] > best_fitness:
            best_fitness = fitness_scores[0][0]
            best_individual = fitness_scores[0][1]

        if simulate_path(best_individual) == goal:
            break

        parents = population[:population_size // 2]

        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            child = mutate(crossover(parent1, parent2))
            new_population.append(child)

        population = new_population

    best_path = []
    position = list(start)
    for move in best_individual:
        nx, ny = position[0] + \
            DIRECTIONS[move][0], position[1] + DIRECTIONS[move][1]
        if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0:
            position = [nx, ny]
            best_path.append(tuple(position))
        if tuple(position) == goal:
            break

    end_time = time.time()
    return best_path, [], generation + 1, end_time - start_time
