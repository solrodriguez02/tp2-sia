from genetic_algorithm.algorithm_definition import GeneticAlgorithm
from genetic_algorithm.utils.generate_canvas import canvas_to_image
from genetic_algorithm.fitness import FitnessFunction
import cv2
import json

if __name__ == "__main__":

    with open("config.json", 'r') as config_file:
        config = json.load(config_file)
        target_image_path = config.get("target_image_path")
        initial_population_size = config.get("initial_population_size")
        triangles_per_solution = config.get("triangles_per_solution")
        recombination_probability = config.get("recombination_probability")
        mutation_probability = config.get("mutation_probability")
        rounds = config.get("rounds")

    for image in target_image_path:
        for pop_size in initial_population_size:
            for triangles in triangles_per_solution:
                for recombination in recombination_probability:
                    for mutation in mutation_probability:
                        for r in rounds:
                            target_image = cv2.imread(image)
                            fitness_function = FitnessFunction(target_image).fitness_avg_pixel_difference
                            genetic_algorithm = GeneticAlgorithm(fitness_function, target_image, pop_size, r)
                            best_individual, fitness_value, generation = genetic_algorithm.run(triangles, recombination, mutation)
                            answer_image = canvas_to_image(best_individual)
                            answer_image.save(f"output_image_r{r}.png")
                            print(f"The best result was found on generation {generation} with a fitness value of: {fitness_value}")
