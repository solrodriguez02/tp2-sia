

class Triangle:
    def __init__(self, vertices, color):
        # vertices: lista de 3 tuplas (x, y)
        # color: tupla (R, G, B, A)
        self.vertices = vertices
        self.color = color
        self.gens = []
        self.set_gens()

    def set_gens(self):
        # Esta implementada la versión 2: hay un gen por cada componente del RGBA y un gen por cada vertice
        for vertice in self.vertices:
            self.gens.append(vertice)
        for rgbi in self.color:
            self.gens.append(rgbi)



class Canvas:
    def __init__(self):
        self.triangles = []
        self.cromosoma = []

    def add_triangle(self, triangle):
        self.triangles.append(triangle)
        self.cromosoma.append(triangle.gens)
