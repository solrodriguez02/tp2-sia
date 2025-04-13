import os

def create_csv():
    filename = "data.csv"
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            header_keys = f"variation,triangulos,generaciones,poblacion_inicial,padres,selection_algorithms,crossover,crossover_probability,mutation,probability_mutation,next_generation_bais,generation_number,max_fitness_value,mean_fitness_value,std_dev_fitness_value\n"
            file.write(header_keys)

    return filename

