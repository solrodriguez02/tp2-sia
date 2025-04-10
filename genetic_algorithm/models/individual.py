import random
from .genes import ColorGene, OpacityGene, PositionGene

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

    def update_from_gene(self, gene):
        if isinstance(gene, ColorGene):
            match gene.name:
                case "Red":
                    self.color = (gene.value, self.color[1], self.color[2], self.color[3])
                case "Green":
                    self.color = (self.color[0], gene.value, self.color[2], self.color[3])
                case "Blue":
                    self.color = (self.color[0], self.color[1], gene.value, self.color[3])
        elif isinstance(gene, OpacityGene):
            self.color = (self.color[0], self.color[1], self.color[2], gene.value)
        elif isinstance(gene, PositionGene):
            match gene.name:
               case "Vertex1": 
                    self.vertexes[0] = gene.value
               case "Vertex2": 
                    self.vertexes[1] = gene.value
               case "Vertex3":  
                    self.vertexes[2] = gene.value

class Canvas:
    def __init__(self):
        self.triangles = []
        self.chromosome = []

    def add_triangle(self, triangle):
        self.triangles.append(triangle)
        self.chromosome.extend(triangle.genes)

    def update_triangle_from_gene(self, gene, gene_position):
        # considering each triangle has 7 genes
        triangle_index = int(gene_position / 7)
        self.triangles[triangle_index].update_from_gene(gene)