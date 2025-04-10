import random
from models.individual import Triangle, Canvas

def create_individuals(num_individuals, num_triangles, width=500, height=500):
    
    individuals = []
    
    for _ in range(num_individuals):
        individual = Canvas()

        for _ in range(num_triangles):
            # Genero el triángulo con 3 vértices random y un color random
            vertexes = generate_vertexes(width, height)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.uniform(0, 1))

            triangle = Triangle(vertexes, color)
            individual.add_triangle(triangle)
                    
        individuals.append(individual)

    return individuals


def generate_vertexes(width, height):
   # Genero el primer vértice random
    cx = random.randint(0, width - 1)
    cy = random.randint(0, height - 1)

    vertexes = [(cx, cy)]

    # Para los dos vertices restantes, elijo un desplazamiento aleatorio (a partir del primer vértice) 
    for _ in range(2):
        x = cx + random.randint(-width, width)
        y = cy + random.randint(-height, height)

        # Si el vértice se sale del canvas, lo ajusto a los límites
        x = max(0, min(width - 1, x))
        y = max(0, min(height - 1, y))

        vertexes.append((x, y))

    return vertexes