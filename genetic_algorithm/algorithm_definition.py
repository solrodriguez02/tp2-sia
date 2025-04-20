from genetic_algorithm.utils.create_individuals import create_individuals
from genetic_algorithm.selection_algorithms.elite_selection import EliteSelection
from genetic_algorithm.selection_algorithms.boltzmann_selection import BoltzmannSelection
from genetic_algorithm.selection_algorithms.ranking_selection import RankingSelection
from genetic_algorithm.selection_algorithms.roulette_wheel_selection import RouletteWheelSelection
from genetic_algorithm.selection_algorithms.tournaments_selection import TournamentSelection
from genetic_algorithm.selection_algorithms.universal_selection import UniversalSelection

from genetic_algorithm.crossover import Crossover
from genetic_algorithm.mutation import Mutation
from genetic_algorithm.next_generation import NextGenerationSelection
from genetic_algorithm.utils.create_individuals import random_generator
import numpy as np
import time
from .utils.write_data import create_csv
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count

def _calculate_fitness(args):
    individual, fitness_function = args
    return fitness_function(individual)
class GeneticAlgorithm:
    def __init__(self, fitness_function, target_image, initial_population_size=50, rounds=200, parents_selection_percentage=0.25, mutation_gens="multiple", max_workers=100):
        self.current_generation = [] 
        self.initial_population_size = initial_population_size
        self.best_individual = None
        self.fitness_function = fitness_function
        self.rounds = rounds
        self.max_fitness = 0
        self.generation_number = 0
        self.target_image = target_image
        self.parents_selection_percentage = parents_selection_percentage
        self.mutation_gens = mutation_gens
        self.fitness_cache = {}
        self.max_workers = max_workers  

    #as threads
    #def calculate_population_fitness(self, population):
    #    fitness_values = []
    #    

    #    with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
    #        fitness_values = list(executor.map(
    #            self.calculate_fitness_for_individual, 
    #            population
    #        ))
    #        
    #    return fitness_values


    #def calculate_fitness_for_individual(self, individual):
    #    individual_hash = hash(str(individual))
    #    if individual_hash in self.fitness_cache:
    #        return self.fitness_cache[individual_hash]

    #    fitness = self.fitness_function(individual)

    #    self.fitness_cache[individual_hash] = fitness
    #    return fitness

    # as processes
    def calculate_population_fitness(self, population):
        fitness_values = []
        uncached_individuals = []
        uncached_indices = []

        for i, individual in enumerate(population):
            individual_hash = hash(str(individual))
            if individual_hash in self.fitness_cache:
                fitness_values.append(self.fitness_cache[individual_hash])
            else:
                uncached_individuals.append(individual)
                uncached_indices.append(i)

        if uncached_individuals:
            args = [(ind, self.fitness_function) for ind in uncached_individuals]

            with Pool(processes=cpu_count()) as pool:
                uncached_fitness_values = pool.map(_calculate_fitness, args)

            for i, individual in enumerate(uncached_individuals):
                individual_hash = hash(str(individual))
                self.fitness_cache[individual_hash] = uncached_fitness_values[i]

            for original_idx, fitness in zip(uncached_indices, uncached_fitness_values):
                while len(fitness_values) <= original_idx:
                    fitness_values.append(None)
                fitness_values[original_idx] = fitness

        return fitness_values

    def run(self, initial_population, triangles_per_solution = 50, recombination_probability=1.0, mutation_probability=0.0,new_generation_bias="traditional",selection_algorithm="elite",crossover_method="uniform_crossover"):

        # CAMBIAR CRITERIA_VALUE SEGUN CORRESPONDA Y EL NOMBRE DE LOS ALGORITMOS QUE VARIAN
        parameters_string = f"next_generation_bias,{triangles_per_solution},{self.rounds},{self.initial_population_size},{self.parents_selection_percentage},{selection_algorithm},{crossover_method},{recombination_probability},{self.mutation_gens},{mutation_probability},{new_generation_bias}"
        data_filename = create_csv()

        # generate initial population
        #self.current_generation = create_individuals(self.initial_population_size, triangles_per_solution)
        self.current_generation = initial_population

        size = int(self.parents_selection_percentage*self.initial_population_size)
        
        if selection_algorithm == "elite":
            selection_method = EliteSelection(size)
        elif selection_algorithm == "roulette":
            selection_method = RouletteWheelSelection(size)
        elif selection_algorithm == "ranking":
            selection_method = RankingSelection(size)
        elif selection_algorithm == "deterministic_tournament" or selection_method == "probabilistic_tournament":
            m = random_generator.randint(0, self.initial_population_size-1)
            treshold = random_generator.random()
            selection_method = TournamentSelection(self.rounds, m, treshold)
        elif selection_algorithm == "universal":
            selection_method = UniversalSelection(size)
        elif selection_algorithm == "boltzmann":
            selection_method = BoltzmannSelection(size, self.rounds)

        
        # set number of parents based on a percentage 
        #selection_method = EliteSelection(Math.floor(0.1 * self.initial_population_size)) 
        #or
        #selection_method = EliteSelection(Math.floor(0.1 * len(self.current_generation)))         
        crossover_method = Crossover(triangles_per_solution)
        #asumming a mutation probability of 1.0
        mutation_method = Mutation(mutation_probability, triangles_per_solution)

        data_file = open(data_filename, mode='a', newline='')
        results = []

        #pass as parameter 
        start_time = time.time()
        while self.generation_number < self.rounds and self.max_fitness < 1.0:

            fitness_values = self.calculate_population_fitness(self.current_generation)
            current_max_fitness = max(fitness_values)

            if current_max_fitness > self.max_fitness:
                self.max_fitness = current_max_fitness
                max_index = fitness_values.index(current_max_fitness)
                self.best_individual = self.current_generation[max_index]

            result_string = f"{parameters_string},{self.generation_number},{self.max_fitness},{np.mean(fitness_values)},{np.std(fitness_values)}\n"
            results.append(result_string)
            # write results every 100 generations
            if self.generation_number % 10 == 0:
                elapsed = time.time() - start_time
                mins, secs = divmod(int(elapsed), 60)
                print(f"Generation: {self.generation_number}, Max fitness: {self.max_fitness}, Time: {mins:02d}:{secs:02d}")
                data_file.writelines(results)
                results = []
            
            # select all parents for this generation
            if selection_algorithm == "deterministic_tournament":
                new_parents = selection_method.runDeterministicTournament(self.current_generation, self.fitness_cache)
            elif selection_algorithm == "probabilistic_tournament":
                new_parents = selection_method.runProbabilisticTournament(self.current_generation, self.fitness_cache)
            else:
                new_parents = selection_method.select(self.current_generation, self.fitness_cache)


            # code for stochasticity
            children = []
            new_parents_shuffled = new_parents.copy()
            random_generator.shuffle(new_parents_shuffled)
            for i in range(int(len(new_parents)/2)):
                first_parent = i * 2 
                second_parent = i * 2 + 1
                random_value = random_generator.random()
                if random_value < recombination_probability:
                    current_parents = [new_parents_shuffled[first_parent], new_parents_shuffled[second_parent]]
                    if crossover_method == "uniform":
                        new_children = crossover_method.uniform_crossover(current_parents)
                    else:
                        new_children = crossover_method.one_point_crossover(current_parents)
                    for child in new_children:
                        children.append(child)
                else:
                    children.append(new_parents[first_parent])
                    children.append(new_parents[second_parent])

            if self.mutation_gens == "single":
                mutation_method.mutateSingleGen(children)
            elif self.mutation_gens == "multiple":
                mutation_method.mutateMultipleGenes(children)
       
            next_generation_selection_method = NextGenerationSelection(self.current_generation, children) 
            if new_generation_bias == "traditional":
                children_fitness = self.calculate_population_fitness(children)
                self.current_generation = next_generation_selection_method.apply_traditional(self.fitness_cache)
            elif new_generation_bias == "youth_bias":
                self.current_generation = next_generation_selection_method.apply_youth_bias(self.fitness_cache)
            self.generation_number += 1

        # Write the resting results to the file
        if len(results) > 0:
            data_file.writelines(results)
        data_file.close()

        print(self.max_fitness)
        print(self.fitness_function(self.best_individual))
        return self.best_individual, self.max_fitness, self.generation_number