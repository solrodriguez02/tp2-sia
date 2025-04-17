from genetic_algorithm.algorithm_definition import GeneticAlgorithm
from genetic_algorithm.utils.generate_canvas import canvas_to_image
from genetic_algorithm.fitness import FitnessFunction
import cv2
import json
import os
from itertools import product
import time

def load_config(config_path="config.json"):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def generate_filename(base_name, params):
    return f"outputs/{base_name}_" + "_".join(f"{k}{v}" for k, v in params.items()) + ".png"

def run_experiment(config):
    timer = time.time()

    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    all_combinations = product(
        config["target_image_path"],
        config["crossover_algorithm"],
        config["selection_algorithm"],
        config["new_generation_bias"],
        config["initial_population_size"],
        config["triangles_per_solution"],
        config["recombination_probability"],
        config["mutations"],
        config["mutation_probability"],
        config["parents_selection_percentage"],
        config["rounds"]
    )

    for (
        image_path, crossover_method, selection_method, new_generation_bias,
        pop_size, triangles, recombination, mutation_gens, mutation_prob,
        parents_pct, round_count
    ) in all_combinations:

        image_name = os.path.splitext(os.path.basename(image_path))[0]
        target_image = cv2.imread(image_path)
        fitness_function = FitnessFunction(target_image).fitness_avg_pixel_difference

        ga = GeneticAlgorithm(
            fitness_function, target_image, pop_size, round_count,
            parents_pct, mutation_gens
        )

        best_individual, fitness_val, generation = ga.run(
            triangles, recombination, mutation_prob,
            new_generation_bias, selection_method, crossover_method
        )

        output_params = {
            "p": pop_size,
            "t": triangles,
            "rec": recombination,
            "probmut": mutation_prob,
            "r": round_count,
            "mut": mutation_gens,
            "sel": selection_method,
            "cross": crossover_method,
            "parents": parents_pct,
            "newgen": new_generation_bias
        }

        output_filename = generate_filename(image_name, output_params)
        canvas_to_image(best_individual).save(output_filename)

        timer = time.time() - timer
        print(f"Execution time: {timer:.2f} seconds")
        print(f"Best result on generation {generation} with fitness: {fitness_val}")
        print(f"Saved to {output_filename}")


if __name__ == "__main__":
    config = load_config()
    run_experiment(config)
