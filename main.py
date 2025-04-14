from genetic_algorithm.algorithm_definition import GeneticAlgorithm
from genetic_algorithm.utils.generate_canvas import canvas_to_image
from genetic_algorithm.fitness import FitnessFunction
import cv2
import json
import os

if __name__ == "__main__":

    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    with open("config.json", 'r') as config_file:
        config = json.load(config_file)
        target_image_path = config.get("target_image_path")
        initial_population_size = config.get("initial_population_size")
        triangles_per_solution = config.get("triangles_per_solution")
        recombination_probability = config.get("recombination_probability")
        mutation_probability = config.get("mutation_probability")
        rounds = config.get("rounds")
        parents_selection_percentages = config.get("parents_selection_percentage")

    for image in target_image_path:
        img_name = image.split('.')[1]
        img_name = img_name.split('/')[2]

        for pop_size in initial_population_size:
            for triangles in triangles_per_solution:
                for recombination in recombination_probability:
                    for mutation in mutation_probability:
                        for parents_selection_percentage in parents_selection_percentages:
                            for r in rounds:
                                target_image = cv2.imread(image)
                                fitness_function = FitnessFunction(target_image).fitness_avg_pixel_difference
                                genetic_algorithm = GeneticAlgorithm(fitness_function, target_image, pop_size, r)
                                best_individual, fitness_value, generation = genetic_algorithm.run(triangles, recombination, mutation)
                                answer_image = canvas_to_image(best_individual)
                                answer_image.save(f"outputs/{img_name}_p{pop_size}_t{triangles}_rec{recombination}_mut{mutation}_r{r}.png")
                                print(f"The best result was found on generation {generation} with a fitness value of: {fitness_value}")

