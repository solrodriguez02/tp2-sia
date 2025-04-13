import pandas as pd

# Leer tu archivo real
df = pd.read_csv('./data.csv')

# Parámetros clave para agrupar
parametros = ['padres', 'poblacion_inicial']
generaciones_totales = df['generation_number'].max()
penalizacion = 0.2  # Ajustable según cuán importante es la velocidad

# Agrupar por combinación
grupos = df.groupby(parametros)

# Guardar datos max_fitness y generación por grupo
datos_por_pd = {}

for (pd, P), group in grupos:
    group = group.sort_values('generation_number')
    idx_max = group['max_fitness_value'].idxmax()
    max_fitness = group.loc[idx_max, 'max_fitness_value']
    gen_max = group.loc[idx_max, 'generation_number']

    if pd not in datos_por_pd:
        datos_por_pd[pd] = []
    datos_por_pd[pd].append((P, max_fitness, gen_max))

# Calcular el score por pd
resultados = []

for pd, lista in datos_por_pd.items():
    score_total = 0
    for P, max_fit, gen in lista:
        penalidad = (gen / generaciones_totales) * penalizacion
        score = max_fit - penalidad
        score_total += score
    score_promedio = score_total / len(lista)
    resultados.append((pd, round(score_promedio, 5)))

# Mostrar ordenado
resultados.sort(key=lambda x: x[1], reverse=True)

print("Score promedio por valor de 'pd':\n")
for pd, score in resultados:
    print(f"pd = {pd:.2f} --> score = {score}")
