from random import uniform
from itertools import accumulate

class UniversalSelection:

    def __init__(self, size):
        self.size = size

    def select(self, population, fitness_function):

        rel_fitness = []
        for individual in population:
            rel_fitness.append(fitness_function(individual))
        
        sum_fitness = sum(rel_fitness)
        rel_fitness = [x / sum_fitness for x in rel_fitness]

        q = list(accumulate(rel_fitness))

        selected_individuals = []

        for j in range(self.size):
            r = uniform(0, 1)
            r_j = (r + j) / self.size
            for i, qi in enumerate(q):
                q_prev = q[i - 1] if i > 0 else 0
                if q_prev <= r_j < qi:
                    selected_individuals.append(population[i])
                    break        
        
        return selected_individuals