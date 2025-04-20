from genetic_algorithm.utils.create_individuals import random_generator

class TournamentSelection:
    #providing the fitness fuction gives a higher value if the individual is similar to the target image
    # rounds = K
    def __init__(self, rounds, M, threshold=1.0):
        self.rounds = rounds
        self.M = M
        self.threshold = threshold

    def runDeterministicTournament(self, population, fitness_values):
        best_individuals = []
        for round in range(self.rounds):
            best_individual = population[0]
            best_score = -1
            for i in range(self.M):
                random_individual = population[random_generator.randint(0,len(population)-1)]
                random_individual_hash = hash(str(random_individual))
                current_score = fitness_values[random_individual_hash]
                if current_score > best_score:
                    best_score = current_score
                    best_individual = random_individual
            best_individuals.append(best_individual)
        
        return best_individuals

    def runProbabilisticTournament(self, population, fitness_values):
        best_individuals = []
        for round in range(self.rounds):
            best_individual = population[0]
            worse_individual = population[0]

            first_individual = population[random_generator.randint(0, len(population)-1)]
            second_individual = population[random_generator.randint(0, len(population)-1)]

            first_individual_hash = hash(str(first_individual))
            second_individual_hash = hash(str(second_individual))

            if (fitness_values[first_individual_hash] > fitness_values[second_individual_hash]):
                best_individual = first_individual
                worse_individual = second_individual
            else:
                best_individual = second_individual
                worse_individual = first_individual
            r = random_generator.random()
            if (r < self.threshold):
                best_individuals.append(best_individual)
            else:
                best_individuals.append(worse_individual)
        return best_individuals