from math import exp
from genetic_algorithm.utils.create_individuals import random_generator
from itertools import accumulate

class BoltzmannSelection:

    def __init__(self, size):
        self.size = size

    def select(self, population, fitness_function, temperature):
        
        # Pseudo fitness aptitude
        exp_values = [exp(fitness_function(individual) / temperature) for individual in population]
        avg_exp = sum(exp_values) / len(exp_values)
        pseudo_fitnesses = [x / avg_exp for x in exp_values]

        q = list(accumulate(pseudo_fitnesses))

        selected_individuals = []

        for _ in range(self.size):
            r = random_generator.uniform(0, 1)
            for i, qi in enumerate(q):
                q_prev = q[i - 1] if i > 0 else 0
                if q_prev <= r < qi:
                    selected_individuals.append(population[i])
                    break        
        
        return selected_individuals