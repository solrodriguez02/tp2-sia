import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read from CSV
df = pd.read_csv('./data.csv')

# Detect the varying parameter
varying_param = df['variation'].iloc[0]

# Define the relevant parameters and their abbreviations
# (excluding the varying parameter)
relevant_params = {
    'triangulos': 'T=',
    'generaciones': 'G=',
    'poblacion_inicial': 'PI=',
    'padres': 'Pd=',
    'selection_algorithms': 'SA=',
    'crossover': 'C=',
    'crossover_probability': 'Cp=',
    'mutation': 'M=',
    'probability_mutation': 'Mp=',
    #'next_generation_bias': 'NG=',
}

# Detect fixed parameter combinations
fixed_combinations = df.drop(columns=['variation']).drop_duplicates(
    subset=list(relevant_params.keys()) + [varying_param]
)

# Group by the fixed parameters (excluding the varying one)
config_groups = df.groupby([
    df[k] for k in relevant_params.keys() if k != varying_param
])

# Iterate over each distinct configuration
for _, config_df in config_groups:
    plt.figure(figsize=(12, 7))

    # Group by the varying parameter within this config
    subgroups = config_df.groupby(varying_param)

    #Choose between mean and max fitness value
    fitness_value = 'max_fitness_value'
    #fitness_value = 'mean_fitness_value'

    for (value, group), in zip(subgroups):
        group = group.sort_values('generation_number')
        group = group[group['generation_number'] > 0]

        x = group['generation_number']
        y = group[fitness_value]
        y_std = group['std_dev_fitness_value']

        # Find the maximum fitness value and the generation it occurred in
        idx_max = group['max_fitness_value'].idxmax()
        max_fitness = group.loc[idx_max, 'max_fitness_value']
        gen_max = group.loc[idx_max, 'generation_number']

        label = f'{varying_param} = {value} (max = {max_fitness:.4f} gen {gen_max})'

        plt.plot(x, y, label=label, linewidth=2)
        if fitness_value == 'mean_fitness_value':
            plt.fill_between(x, y - y_std, y + y_std, alpha=0.2)

    param_values = config_df.iloc[0]
    simplified_name = "_".join(
        f"{abbr}{param_values[key]}"
        for key, abbr in relevant_params.items()
    )

    title = f"Fitness maximo vs {varying_param}"
    filename = f"plot_{varying_param}_{simplified_name}.png"

    plt.title(title)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend(loc='center right')
    plt.grid(True)
    plt.tight_layout()  # Deja espacio a la derecha
    plt.savefig(filename)
    #plt.show()
