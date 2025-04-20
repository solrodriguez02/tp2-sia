from genetic_algorithm.utils.create_individuals import random_generator
from itertools import accumulate

class RouletteWheelSelection:

    def __init__(self, size):
        self.size = size

    def select(self, population, fitness_values):

        rel_fitness = []
        for individual in population:
            individual_hash = hash(str(individual))
            rel_fitness.append(fitness_values[individual_hash])
        
        sum_fitness = sum(rel_fitness)
        rel_fitness = [x / sum_fitness for x in rel_fitness]

        q = list(accumulate(rel_fitness)) 

        selected_individuals = []

        for _ in range(self.size):
            r = random_generator.uniform(0, 1)
            for i, qi in enumerate(q):
                q_prev = q[i - 1] if i > 0 else 0
                if q_prev <= r < qi:
                    selected_individuals.append(population[i])
                    break        
        
        return selected_individuals
        
            