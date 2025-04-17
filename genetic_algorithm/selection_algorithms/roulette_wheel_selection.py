from genetic_algorithm.utils.create_individuals import random_generator
import numpy as np

class RouletteWheelSelection:

    def __init__(self, size):
        self.size = size

    def select(self, population, fitness_function):

        rel_fitness = [fitness_function(ind) for ind in population]
        sum_fitness = sum(rel_fitness)
        rel_fitness = [x / sum_fitness for x in rel_fitness]

        q = np.cumsum(rel_fitness) 

        selected_individuals = []
        for _ in range(self.size):
            r = random_generator.uniform(0, 1)
            index = np.searchsorted(q, r, side='right')
            selected_individuals.append(population[index - 1])
                    
        return selected_individuals
        
            