import random
import time
from src.utilities.constants import DIRECTIONS, MAZE_WIDTH, MAZE_HEIGHT


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
