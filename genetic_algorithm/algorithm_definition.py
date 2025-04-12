from genetic_algorithm.utils.create_individuals import create_individuals
from genetic_algorithm.selection_algorithms.elite_selection import EliteSelection
from genetic_algorithm.crossover import Crossover
from genetic_algorithm.mutation import Mutation
from genetic_algorithm.next_generation import NextGenerationSelection
import random
import numpy as np
from .utils.write_data import create_csv
class GeneticAlgorithm:
    def __init__(self, fitness_function, target_image, initial_population_size=50, rounds=200, parents_selection_percentage=0.25):
        self.current_generation = [] 
        self.initial_population_size = initial_population_size
        self.best_individual = None
        self.fitness_function = fitness_function
        self.rounds = rounds
        self.max_fitness = 0
        self.generation_number = 0
        self.target_image = target_image
        self.parents_selection_percentage = parents_selection_percentage
    
    def run(self, triangles_per_solution = 50, recombination_probability=1.0, mutation_probability=0.0):

        # CAMBIAR CRITERIA_VALUE SEGUN CORRESPONDA Y EL NOMBRE DE LOS ALGORITMOS QUE VARIAN
        parameters_string = f"CRITERIA_VALUE,{triangles_per_solution},{self.rounds},{self.initial_population_size},{self.parents_selection_percentage},elite_selection,uniform_crossover,{recombination_probability},Multi,{mutation_probability},Youth_bias"
        data_filename = create_csv()

        # generate initial population
        self.current_generation = create_individuals(self.initial_population_size, triangles_per_solution)
        
        selection_method = EliteSelection(self.parents_selection_percentage*self.initial_population_size)
        # set number of parents based on a percentage 
        #selection_method = EliteSelection(Math.floor(0.1 * self.initial_population_size)) 
        #or
        #selection_method = EliteSelection(Math.floor(0.1 * len(self.current_generation)))         
        crossover_method = Crossover(triangles_per_solution)
        #asumming a mutation probability of 1.0
        mutation_method = Mutation(mutation_probability, triangles_per_solution)

        data_file = open(data_filename, mode='a', newline='')

        #pass as parameter 
        while self.max_fitness < 0.9 and self.generation_number < self.rounds:
            print(f"Generation: {self.generation_number}, Max fitness: {self.max_fitness}")
            fitness_values = []
            for individual in self.current_generation:
                fitness_values.append(self.fitness_function(individual))
            data_string = f"{self.generation_number},{self.max_fitness},{np.mean(fitness_values)},{np.std(fitness_values)}"
            data_file.write(f"{parameters_string},{data_string}\n")

            # select all parents for this generation
            new_parents = selection_method.select(self.current_generation, self.fitness_function)


            # asumme a recombination probability of 1.0
            children = crossover_method.uniform_crossover(new_parents)

            # code for stochasticity
            #children = []
            #for i in range(len(new_parents)/2):
            #    first_parent = i * 2 
            #    second_parent = i * 2 + 1
            #    random_value = random_generator.random()
            #    if random_value < recombination_probability:
            #        current_parents = [new_parents[first_parent], new_parents[second_parent]]
            #        new_children = crossover_method.one_point_crossover(current_parents)
            #        for child in new_children:
            #            children.append(child)
            #    else:
            #        children.append(new_parents[first_parent])
            #        children.append(new_parents[second_parent])

            mutation_method.mutateSingleGen(children)

            # calculate max fitness value
            for child in children:
                current_fitness = self.fitness_function(child)
                if current_fitness > self.max_fitness:
                    self.max_fitness = current_fitness
                    self.best_individual = child
            
            next_generation_selection_method = NextGenerationSelection(self.current_generation, children) 
            self.current_generation = next_generation_selection_method.apply_youth_bias(self.fitness_function)
            self.generation_number += 1

        print(self.max_fitness)
        print(self.fitness_function(self.best_individual))
        return self.best_individual, self.max_fitness, self.generation_number