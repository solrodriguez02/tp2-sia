import matplotlib 
matplotlib.use('Agg')  # Use the 'Agg' backend which doesn't require Qt
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

csv_file = 'data.csv'
df = pd.read_csv(csv_file)

if not os.path.exists("graphs"):
    os.makedirs("graphs")

def fitness_vs_generations():
    df['generaciones'] = df['generaciones'].astype(int)
    df['mean_fitness_value'] = df['mean_fitness_value'].astype(float)
    df['std_dev_fitness_value'] = df['std_dev_fitness_value'].astype(float)

    df_gen = df.groupby('generaciones')

    for gen, group in df_gen:
        plt.plot(group['mean_fitness_value'].reset_index(drop=True), label=f'{gen} generaciones')
        plt.fill_between(group.index - group.index.min(), 
                 group['mean_fitness_value'] - group['std_dev_fitness_value'],
                 group['mean_fitness_value'] + group['std_dev_fitness_value'], alpha=0.2)
        
    plt.xlabel('Individuos')
    plt.ylabel('Fitness')
    plt.title('Evolucion del Fitness vs Generaciones')
    plt.xticks(rotation=90)
    plt.grid()

    plt.legend()
    plt.savefig(f"graphs/fitness_vs_generations.png")


# Max fitness vs generations
def max_fitness_vs_generations():
    df['generaciones'] = df['generaciones'].astype(int)
    df['max_fitness_value'] = df['max_fitness_value'].astype(float)

    df_gen = df.groupby('generaciones')
    for gen, group in df_gen:
        plt.plot(group['max_fitness_value'].reset_index(drop=True), label=f'{gen} generaciones')
    
    plt.xlabel('Generaciones')
    plt.ylabel('Fitness')
    plt.title('Fitness Maximo vs Generaciones')
    plt.xticks(rotation=90)
    plt.ylim(0.5, 0.9)
    plt.grid()
    plt.legend()
    plt.savefig(f"graphs/max_fitness_vs_generations.png")


def triangles_variation_graph():

    df = df[df["variation"] == "Triangles_variation"]

    for triangle_count in df["triangulos"].unique():
        subset = df[df["triangulos"] == triangle_count]

        plt.plot(
            subset["generation_number"],
            subset["max_fitness_value"],
            label=f"{triangle_count} triángulos"
        )

        plt.fill_between(
            subset["generation_number"],
            subset["max_fitness_value"] - subset["std_dev_fitness_value"],
            subset["max_fitness_value"] + subset["std_dev_fitness_value"],
            alpha=0.2
        )

    plt.xlabel("Generación")
    plt.ylabel("Fitness máximo")
    plt.title("Evolución del fitness según la cantidad de triángulos")
    plt.legend(title="Cantidad de triángulos")
    plt.grid(True)
    plt.ylim(bottom=0.55)
    plt.tight_layout()
    plt.show()


def crossover_variation():

    df = df[df["variation"] == "Crossover_variation"]

    for crossover_type in df["crossover"].unique():
        subset = df[df["crossover"] == crossover_type]
        label = "Uniform" if crossover_type == "uniform_crossover" else "One Point"
        plt.plot(
            subset["generation_number"],
            subset["max_fitness_value"],
            label = label
        )

        plt.fill_between(
            subset["generation_number"],
            subset["max_fitness_value"] - subset["std_dev_fitness_value"],
            subset["max_fitness_value"] + subset["std_dev_fitness_value"],
            alpha=0.2
        )

    plt.title("Evolución del fitness según el método de Cruza")
    plt.xlabel("Generación")
    plt.ylabel("Fitness Máximo")
    plt.legend(title="Método de Cruza")
    plt.grid(True)
    plt.tight_layout()
    plt.ylim(bottom=0.55)
    plt.show()

def mutation_vs_fitness(mutation):
    # mutation: single / multi
    df_single = df[(df['variation'] == 'MUTATION') & (df['mutation'] == mutation)].copy()

    df_single['generaciones'] = df_single['generaciones'].astype(int)
    df_single['mean_fitness_value'] = df_single['mean_fitness_value'].astype(float)
    df_single['std_dev_fitness_value'] = df_single['std_dev_fitness_value'].astype(float)
    df_single['probability_mutation'] = df_single['probability_mutation'].astype(float)

    df_single = df_single.groupby('probability_mutation')

    plt.figure(figsize=(10, 6))

    for prob, group in df_single:
        plt.plot(group['mean_fitness_value'].reset_index(drop=True), label=f'{prob} mutación')
        plt.fill_between(group.index - group.index.min(), 
                 group['mean_fitness_value'] - group['std_dev_fitness_value'],
                 group['mean_fitness_value'] + group['std_dev_fitness_value'], alpha=0.2)
        
    plt.xlabel('Generaciones')
    plt.ylabel('Fitness')
    if mutation == 'single':
        plt.title('Evolucion del Fitness vs Generaciones variando la probabilidad de mutación (Un solo gen)')
    else:
        plt.title('Evolucion del Fitness vs Generaciones variando la probabilidad de mutación (Multiples genes)')

    plt.xticks(rotation=90)
    plt.grid()
    plt.legend()
    plt.savefig(f"graphs/{mutation}_vs_fitness.png")

def boltzmann_temperature_variation_with_decreasing():

    variations = [
        "BoltzmannTemp_T00.5_variation",
        "BoltzmannTemp_T05_variation",
        "BoltzmannTemp_T01.5_variation"
    ]

    df_filtered = df[df["variation"].isin(variations)]

    plt.figure(figsize=(10, 6))

    for variation in variations:
        subset = df_filtered[df_filtered["variation"] == variation]
        
        if variation == "BoltzmannTemp_T00.5_variation":
            label = "T0 = 0.5"
        elif variation == "BoltzmannTemp_T05_variation":
            label = "T0 = 5"
        elif variation == "BoltzmannTemp_T01.5_variation":
            label = "T0 = 1.5"

        plt.plot(subset["generation_number"], subset["mean_fitness_value"], label=label)

        plt.fill_between(
            subset["generation_number"],
            subset["mean_fitness_value"] - subset["std_dev_fitness_value"],
            subset["mean_fitness_value"] + subset["std_dev_fitness_value"],
            alpha=0.2
        )

    plt.title("Impacto de la Variación de Temperatura en la Selección Boltzmann")
    plt.xlabel("Generación")
    plt.ylabel("Fitness Medio")
    plt.legend(title="Variación de Temperatura")
    plt.ylim(bottom=0.5)
    plt.grid(True)
    plt.tight_layout()

    plt.show()

def boltzmann_temperature_variation():

    variations = [
        "BoltzmannTemp_T0.5_variation",
        "BoltzmannTemp_T10_variation",
        "BoltzmannTemp_T0.01_variation"
    ]

    df_filtered = df[df["variation"].isin(variations)]

    plt.figure(figsize=(10, 6))

    for variation in variations:
        subset = df_filtered[df_filtered["variation"] == variation]
        
        if variation == "BoltzmannTemp_T0.5_variation":
            label = "T = 0.5"
        elif variation == "BoltzmannTemp_T5_variation":
            label = "T = 5"
        elif variation == "BoltzmannTemp_T1.5_variation":
            label = "T = 1.5"
        elif variation == "BoltzmannTemp_T10_variation":
            label = "T = 10"
        elif variation == "BoltzmannTemp_T0.01_variation":
            label = "T = 0.01"

        plt.plot(subset["generation_number"], subset["mean_fitness_value"], label=label)

        plt.fill_between(
            subset["generation_number"],
            subset["mean_fitness_value"] - subset["std_dev_fitness_value"],
            subset["mean_fitness_value"] + subset["std_dev_fitness_value"],
            alpha=0.2
        )

    plt.title("Impacto de la Variación de Temperatura en la Selección Boltzmann")
    plt.xlabel("Generación")
    plt.ylabel("Fitness Medio")
    plt.legend(title="Variación de Temperatura")
    plt.ylim(bottom=0.5)
    plt.grid(True)
    plt.tight_layout()

    plt.show()

def parents_selection_percentage_variation_graph():

    my_df = df[df["variation"] == "padres"]

    for parents_selection_percentage in my_df["padres"].unique():
        subset = my_df[my_df["padres"] == parents_selection_percentage]

        plt.plot(
            subset["generation_number"],
            subset["max_fitness_value"],
            label=f"{parents_selection_percentage * 100} %"
        )

        plt.fill_between(
            subset["generation_number"],
            subset["max_fitness_value"] - subset["std_dev_fitness_value"],
            subset["max_fitness_value"] + subset["std_dev_fitness_value"],
            alpha=0.2
        )

    plt.xlabel("Generación")
    plt.ylabel("Fitness máximo")
    plt.title("Evolución del fitness según el porcentaje de reproducción")
    plt.legend(title="Porcentaje de población que se reproduce")
    plt.grid(True)
    plt.ylim(bottom=0.55)
    plt.tight_layout()
    plt.savefig(f"graphs/parents_selection_percentage_vs_fitness_value.png")


if __name__ == "__main__":
    ## triangles_variation_graph()
    ## fitness_vs_generations()
    #max_fitness_vs_generations()
    #triangles_variation_graph()
    #crossover_variation()
    #boltzmann_temperature_variation()
    parents_selection_percentage_variation_graph()

    mutation_vs_fitness('single')
    mutation_vs_fitness('multi')