import pandas as pd
import matplotlib.pyplot as plt

def triangles_variation_graph():
    df = pd.read_csv("data.csv")

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


# main
if __name__ == "__main__":
    triangles_variation_graph()