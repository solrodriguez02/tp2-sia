from genetic_algorithm.utils.create_individuals import random_generator

class RankingSelection:
    def __init__(self, size):
        self.size = size

    def select(self, population, fitness_values_dict):
        fitness_values = []
        sum_aptitudes = 0
        for individual in population:
            individual_hash = hash(str(individual))
            current_aptitude = fitness_values_dict[individual_hash]
            sum_aptitudes += current_aptitude
            fitness_values.append(current_aptitude)

        accum_aptitude_values = []
        for i in range(len(population)):
            if i == 0:
                accum_aptitude_values.append(fitness_values[i]/sum_aptitudes)
            else:
                accum_aptitude_values.append(accum_aptitude_values[i-1] + fitness_values[i] / sum_aptitudes)

        selected_individuals = []

        for _ in range(self.size):
            r = random_generator.random()
            selected = False
            for i in range(len(population)):
                if accum_aptitude_values[i] > r:
                    if i > 0:
                        selected_individuals.append(population[i-1])
                    else:
                        selected_individuals.append(population[0])
                    selected = True
                    break
            if not selected:
                selected_individuals.append(population[len(population)-1])

        return selected_individuals