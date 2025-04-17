from genetic_algorithm.utils.create_individuals import random_generator
import numpy as np
class UniversalSelection:

    def __init__(self, size):
        self.size = size

    def select(self, population, fitness_function):

        fitness_values = [fitness_function(individual) for individual in population]
        total_fitness = sum(fitness_values)
        rel_fitness = [f / total_fitness for f in fitness_values]

        q = np.cumsum(rel_fitness)

        selected_individuals = []

        for j in range(self.size):
            r = random_generator.uniform(0, 1)
            r_j = (r + j) / self.size
            index = np.searchsorted(q, r_j)
            selected_individuals.append(population[index])
      
        return selected_individuals