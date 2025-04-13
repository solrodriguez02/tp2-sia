import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read from CSV
df = pd.read_csv('./data.csv')


# Detect variable parameter
parametro_variable = df['variation'].iloc[0]

parametros_relevantes = {
    'triangulos': 'T',
    'generaciones': 'G',
    'padres': 'Pd'
}

# Detect fixed parameters combinations
param_combinaciones = df.drop(columns=['variation']).drop_duplicates(
    subset=list(parametros_relevantes.keys()) + [parametro_variable]
)

# Group by the fixed parameter combination (without the variable one)
grupos_config = df.groupby([
    df[k] for k in parametros_relevantes.keys() if k != parametro_variable
])

# Iterate over each distinct configuration
for _, df_config in grupos_config:
    plt.figure(figsize=(12, 7))

    # Group by the varying parameter within this config
    subgroups = df_config.groupby(parametro_variable)

    for (valor, group), in zip(subgroups):
        group = group.sort_values('generation_number')
        group = group[group['generation_number'] > 0]

        x = group['generation_number']
        y_mean = group['mean_fitness_value']
        y_std = group['std_dev_fitness_value']

        # Find the maximum fitness_value and the generation it occurred in
        idx_max = group['max_fitness_value'].idxmax()
        max_fitness = group.loc[idx_max, 'max_fitness_value']
        gen_max = group.loc[idx_max, 'generation_number']

        label = f'{parametro_variable} = {valor} (max = {max_fitness:.4f} gen {gen_max})'

        plt.plot(x, y_mean, label=label, linewidth=2)
        plt.fill_between(x, y_mean - y_std, y_mean + y_std, alpha=0.2)

    
    valores_param = df_config.iloc[0]
    nombre_simplificado = "_".join(
        f"{abreviacion}{valores_param[clave]}"
        for clave, abreviacion in parametros_relevantes.items()
    )

    titulo = f"Evolución de Fitness Promedio - {nombre_simplificado}"
    archivo = f"grafico_{parametro_variable}_{nombre_simplificado}.png"

    plt.title(titulo)
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(archivo)
    plt.show()
