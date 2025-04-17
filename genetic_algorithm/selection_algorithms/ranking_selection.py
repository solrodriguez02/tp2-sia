from genetic_algorithm.utils.create_individuals import random_generator
import numpy as np

class RankingSelection:
    def __init__(self, size):
        self.size = size

    def select(self, population, fitness_function):
        ranked_population = sorted(population, key=fitness_function, reverse=True)
        n = len(ranked_population)
        probabilities = np.arange(n, 0, -1) / np.sum(np.arange(n, 0, -1))

        cumulative_prob = np.cumsum(probabilities)

        selected_individuals = []

        for _ in range(self.size):
            r = random_generator.random()
            index = np.searchsorted(cumulative_prob, r)
            selected_individuals.append(population[index])

        return selected_individuals