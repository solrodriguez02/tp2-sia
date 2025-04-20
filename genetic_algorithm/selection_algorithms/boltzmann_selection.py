from math import exp
from genetic_algorithm.utils.create_individuals import random_generator
from itertools import accumulate
import math

class BoltzmannSelection:

    def __init__(self, size, total_generations, T0=1.0, with_decreasing_function=False):
        self.size = size
        self.total_generations = total_generations
        self.with_decreasing_function = with_decreasing_function
        self.T0 = T0
        self.Tc = 0.01

    def select(self, population, fitness_values_dict, generation_number):
        
        if self.with_decreasing_function:
            temperature = self.temperature_schedule(generation_number)
        else:
            temperature = self.T0

        # Pseudo fitness aptitude
        exp_values = [exp(fitness_values_dict[hash(str(individual))] / temperature) for individual in population]
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
    
    def temperature_schedule(self, generation_number):
        epsilon = 0.001
        k = -math.log(epsilon / (self.T0 - self.Tc)) / self.total_generations
        return self.Tc + (self.T0 - self.Tc) * math.exp(-k * generation_number)
