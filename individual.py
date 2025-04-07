import random

class Triangle:
    def __init__(self, vertexes, color):
        # vertices: lista de 3 tuplas (x, y)
        # color: tupla (R, G, B, A)
        self.vertexes = vertexes
        self.color = color
        self.genes = []
        self.set_genes()

    def set_genes(self):
        # Esta implementada la versión 2: hay un gen por cada componente del RGBA y un gen por cada vertice
        colors = ["Red", "Green", "Blue"]
        for rgb_index in range(len(self.color)-1):
            self.genes.append(ColorGene(colors[rgb_index], self.color[rgb_index]))
        
        self.genes.append(OpacityGene(0.8))

        vertex_names = ["Vertex1", "Vertex2", "Vertex3"]
        
        for vertex_index in range(3):
            #change last parameter if image dimensions' restrictions are changed
            self.genes.append(PositionGene(vertex_names[vertex_index], self.vertexes[vertex_index], (499,499)))

class Canvas:
    def __init__(self):
        self.triangles = []
        self.chromosome = []

    def add_triangle(self, triangle):
        self.triangles.append(triangle)
        self.chromosome.append(triangle.genes)

class Gene:
    def __init__(self, name, value, min, max, is_float = False):
        if isinstance(value, int):
            if value < min or value > max:
                raise ValueError("invalid value for integer value")
        if isinstance(value, tuple):
            if value[0] < min[0] or value[0] > max[0] or value[1] < min[1] or value[1] > max[1]:
                raise ValueError("invalid value for tuple")

        self.name = name
        self.value = value
        self.min = min
        self.max = max
        self.is_float = is_float

    def mutate(self):
        self.value = random.randint(min, max)

class ColorGene(Gene):
    def __init__(self, name, value):
        super().__init__(name, value, 0, 255)

class OpacityGene(Gene):
    def __init__(self, value):
        super().__init__("opacity", value, 0, 1, True)

    def mutate(self):
        self.value = random.random()

class PositionGene(Gene):
    def __init__(self, name, value, max):
        super().__init__(name, value, (0,0), max)

    def mutate(self):
        self.value = (random.randint(min[0], max[0]), random.randint(min[0], max[0]))