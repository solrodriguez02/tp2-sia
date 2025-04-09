import random
from genes import ColorGene, OpacityGene, PositionGene

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
