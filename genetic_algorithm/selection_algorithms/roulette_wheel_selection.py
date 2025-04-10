from random import uniform, random

class RouletteWheelSelection:

    def __init__(self, size):
        self.size = size

    def select(self, population, fitness_function):

        rel_fitness = []
        for individual in population:
            rel_fitness.append(fitness_function(individual))
        
        sum_fitness = sum(rel_fitness)
        rel_fitness = [x / sum_fitness for x in rel_fitness]

        q = []
        cumulative_sum = 0
        for fitness in rel_fitness:
            cumulative_sum += fitness
            q.append(cumulative_sum) 

        selected_individuals = []

        for _ in range(self.size):
            r = uniform(0, 1)
            for i, qi in enumerate(q):
                q_prev = q[i - 1] if i > 0 else 0
                if q_prev <= r < qi:
                    selected_individuals.append(population[i])
                    break        
        
        return selected_individuals
        
            