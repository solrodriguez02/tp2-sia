import pandas as pd

# Read from CSV
df = pd.read_csv('./data.csv')

# Params to group by
params = ['padres', 'poblacion_inicial']
total_generations = df['generation_number'].max()
penalization = 0.2  # Ajustable según cuán importante es la velocidad

# Group by params combination
groups = df.groupby(params)

data = {}

for (pd, P), group in groups:
    group = group.sort_values('generation_number')
    idx_max = group['max_fitness_value'].idxmax()
    max_fitness = group.loc[idx_max, 'max_fitness_value']
    gen_max = group.loc[idx_max, 'generation_number']

    if pd not in data:
        data[pd] = []
    data[pd].append((P, max_fitness, gen_max))

results = []

for pd, list in data.items():
    total_score = 0
    for P, max_fit, gen in list:
        penality = (gen / total_generations) * penalization
        score = max_fit - penality
        total_score += score
    mean_score = total_score / len(list)
    results.append((pd, round(mean_score, 5)))

results.sort(key=lambda x: x[1], reverse=True)

print("Score promedio por valor de 'pd':\n")
for pd, score in results:
    print(f"pd = {pd:.2f} --> score = {score}")
