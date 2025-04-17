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
from .utils.write_data import create_csv

SELECTION_METHODS = {
    "elite": EliteSelection,
    "roulette": RouletteWheelSelection,
    "ranking": RankingSelection,
    "deterministic_tournament": TournamentSelection,
    "probabilistic_tournament": TournamentSelection,
    "universal": UniversalSelection,
    "boltzmann": BoltzmannSelection
}

class GeneticAlgorithm:
    def __init__(self, fitness_function, target_image, initial_population_size=50, rounds=200, parents_selection_percentage=0.25, mutation_gens="multiple"):
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
    
    def run(self, triangles_per_solution = 50, recombination_probability=1.0, mutation_probability=0.0,new_generation_bias="traditional",selection_algorithm="elite",crossover_method="uniform_crossover"):

        # CAMBIAR CRITERIA_VALUE SEGUN CORRESPONDA Y EL NOMBRE DE LOS ALGORITMOS QUE VARIAN
        parameters_string = f"next_generation_bias,{triangles_per_solution},{self.rounds},{self.initial_population_size},{self.parents_selection_percentage},{selection_algorithm},{crossover_method},{recombination_probability},{self.mutation_gens},{mutation_probability},{new_generation_bias}"
        data_filename = create_csv()

        # generate initial population
        self.current_generation = create_individuals(self.initial_population_size, triangles_per_solution)

        size = int(self.parents_selection_percentage*self.initial_population_size)
        
        selection_method_class = SELECTION_METHODS.get(selection_algorithm)
        if selection_method_class:
            if selection_algorithm in ["deterministic_tournament", "probabilistic_tournament"]:
                m = random_generator.randint(0, self.initial_population_size-1)
                treshold = random_generator.random()
                selection_method = selection_method_class(self.rounds, m, treshold)
            else:
                selection_method = selection_method_class(size)
        else:
            raise ValueError(f"Unknown selection algorithm: {selection_algorithm}")

        
        # set number of parents based on a percentage 
        #selection_method = EliteSelection(Math.floor(0.1 * self.initial_population_size)) 
        #or
        #selection_method = EliteSelection(Math.floor(0.1 * len(self.current_generation)))         
        crossover_obj = Crossover(triangles_per_solution)
        #asumming a mutation probability of 1.0
        mutation_method = Mutation(mutation_probability, triangles_per_solution)

        data_file = open(data_filename, mode='a', newline='')

        #pass as parameter 
        while self.generation_number < self.rounds:
            print(f"Generation: {self.generation_number}, Max fitness: {self.max_fitness}")
            fitness_values = []
            for individual in self.current_generation:
                fitness_values.append(self.fitness_function(individual))
            data_string = f"{self.generation_number},{self.max_fitness},{np.mean(fitness_values)},{np.std(fitness_values)}"
            data_file.write(f"{parameters_string},{data_string}\n")

            # select all parents for this generation
            if selection_algorithm == "deterministic_tournament":
                new_parents = selection_method.runDeterministicTournament(self.current_generation, self.fitness_function)
            elif selection_algorithm == "probabilistic_tournament":
                new_parents = selection_method.runProbabilisticTournament(self.current_generation, self.fitness_function)
            else:
                new_parents = selection_method.select(self.current_generation, self.fitness_function)


            # asumme a recombination probability of 1.0
            #children = crossover_method.uniform_crossover(new_parents)

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
                    if crossover_method == "uniform_crossover":
                        new_children = crossover_obj.uniform_crossover(current_parents)
                    else:
                        new_children = crossover_obj.one_point_crossover(current_parents)
                    for child in new_children:
                        children.append(child)
                else:
                    children.append(new_parents[first_parent])
                    children.append(new_parents[second_parent])

            mutation_method.mutateSingleGen(children) if self.mutation_gens == "single" else mutation_method.mutateMultipleGenes(children)
       
            # calculate max fitness value
            for child in children:
                current_fitness = self.fitness_function(child)
                if current_fitness > self.max_fitness:
                    self.max_fitness = current_fitness
                    self.best_individual = child
            
            next_generation_selection_method = NextGenerationSelection(self.current_generation, children) 
            if new_generation_bias == "traditional":
                self.current_generation = next_generation_selection_method.apply_traditional(self.fitness_function)
            else:
                self.current_generation = next_generation_selection_method.apply_youth_bias(self.fitness_function)

            self.generation_number += 1

        print(self.max_fitness)
        print(self.fitness_function(self.best_individual))
        return self.best_individual, self.max_fitness, self.generation_number