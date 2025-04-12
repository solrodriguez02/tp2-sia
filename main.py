from genetic_algorithm.algorithm_definition import GeneticAlgorithm
from genetic_algorithm.utils.generate_canvas import canvas_to_image
from genetic_algorithm.fitness import FitnessFunction
import cv2

if __name__ == "__main__":
    # change to use parameters
    target_image_path = "./images/bandera.jpg"
    target_image = cv2.imread(target_image_path)

    #read from config file (now all have a default value anyway)
    initial_population_size = 50
    triangles_per_solution = 10
    recombination_probability = 1.0
    mutation_probability = 1.0

    fitness_function = FitnessFunction(target_image).fitness_avg_pixel_difference
    genetic_algorithm = GeneticAlgorithm(fitness_function, target_image, initial_population_size)
    best_individual, fitness_value, generation = genetic_algorithm.run(triangles_per_solution, recombination_probability, mutation_probability)

    answer_image = canvas_to_image(best_individual)
    answer_image.save("output_image.png")
    print(f"The best result was found on generation {generation} with a fitness value of: {fitness_value}")

