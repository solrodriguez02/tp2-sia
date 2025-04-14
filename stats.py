from matplotlib import pyplot as plt
import pandas as pd
import os

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

# main
if __name__ == "__main__":
    # triangles_variation_graph()
    # fitness_vs_generations()
    # max_fitness_vs_generations()
    mutation_vs_fitness('single')
    mutation_vs_fitness('multi')