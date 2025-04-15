# Compresor de Imagenes con Triangulos utilizando Algoritmos Geneticos

## Configuracion del Algoritmo

Los parametros iniciales del algoritmo se definen en el archivo `config.json`.

- `image_target_path`: Ubicacion de la imagen a comprimir
- `initial_population_size`: Tamaño inicial de la poblacion
- `triangles_per_solution`: Cantidad de triangulos en el estado inicial
- `recombination_probability`: Probabilidad de que los genes se combinen
- `mutations`: Si muta un solo gen o varios. Puede ser "single" o "multi"
- `mutation_probability`: Probabilidad de mutacion
- `rounds`: Cantidad de generaciones a ejecutar
- `parents_selection_percentage`: Porcentaje de padres que se reproducen 

Se pueden definir varios valores para cada parametro

Ejemplo de archivo de configuracion

```json
{
    "target_image_path": [ "./images/bandera.jpg" ],
    "initial_population_size": [ 50 ],
    "triangles_per_solution": [ 10 ],
    "recombination_probability": [ 1.0 ],
    "mutations": [ "multi" ],
    "mutation_probability": [ 0.2, 0.4, 0.6, 0.8, 1.0 ],
    "rounds": [ 100 ],
    "parents_selection_percentage": [ 0.25, 0.5, 0.75, 1.0]
}
```

El algoritmo termina si alcanza un fitness maximo mayor a 0.9 o si se alcanzo el numero de generaciones definido, lo que ocurra primero.
