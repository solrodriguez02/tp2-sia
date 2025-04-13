import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

def triangles_variation_graph():
    df = pd.read_csv("data.csv")

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
    df = pd.read_csv("data.csv")

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


def boltzmann_temperature_variation_with_decreasing():

    df = pd.read_csv("data.csv")

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
    df = pd.read_csv("data.csv")

    variations = [
        "BoltzmannTemp_T0.5_variation",
        "BoltzmannTemp_T5_variation",
        "BoltzmannTemp_T1.5_variation"
    ]

    df_filtered = df[df["variation"].isin(variations)]

    plt.figure(figsize=(10, 6))

    for variation in variations:
        subset = df_filtered[df_filtered["variation"] == variation]
        
        if variation == "BoltzmannTemp_T0.5_variation":
            label = "T0 = 0.5"
        elif variation == "BoltzmannTemp_T5_variation":
            label = "T0 = 5"
        elif variation == "BoltzmannTemp_T1.5_variation":
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


if __name__ == "__main__":
    #triangles_variation_graph()
    #crossover_variation()
    boltzmann_temperature_variation()
 