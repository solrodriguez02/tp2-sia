from .utils.create_individuals import random_generator
from genetic_algorithm.models.individual import Canvas, Triangle


class Crossover():

    def __init__(self, triangles_amount):
        self.triangles_amount = triangles_amount

    def one_point_crossover(self, parents):
        childs = []
        cross_point = random_generator.randint(0, len(parents[0].chromosome) - 1)
        index = 0

        p1,p2 = parents[index], parents[index + 1]

        if len(p1.chromosome) != len(p2.chromosome):
            raise ValueError("Los individuos deben tener la misma cantidad de genes")
        
        child1_genes = p1.chromosome[:cross_point] + p2.chromosome[cross_point:]
        child2_genes = p2.chromosome[:cross_point] + p1.chromosome[cross_point:]

        childs.append(build_canvas_from_genes(child1_genes))
        childs.append(build_canvas_from_genes(child2_genes))

        return childs

    def uniform_crossover(self,parents):
        childs = []
        index = 0
        change_genes_probability = 0.5

        first_individual = parents[index]
        second_individual = parents[index + 1]
        
        if len(first_individual.triangles) != len(second_individual.triangles):
            raise ValueError("individuals must have the same number of triangles")
        
        chromosome_index = 0
        
        first_child = []
        second_child = []
        
        while chromosome_index < len(first_individual.chromosome):
            first_parent = first_individual.chromosome[chromosome_index]
            second_parent = second_individual.chromosome[chromosome_index]
            if random_generator.random() > change_genes_probability:
                first_child.append(first_parent)
                second_child.append(second_parent)
            else:
                first_child.append(second_parent)
                second_child.append(first_parent)
            chromosome_index += 1
        childs.append(build_canvas_from_genes(first_child))
        childs.append(build_canvas_from_genes(second_child))

        return childs
    

    
def build_canvas_from_genes(chromosoma):
    canvas = Canvas()
    index = 0
    while index < len(chromosoma):
        r = chromosoma[index].value
        g = chromosoma[index+1].value
        b = chromosoma[index+2].value
        vertex1 = chromosoma[index+3].value
        vertex2 = chromosoma[index+4].value
        vertex3 = chromosoma[index+5].value
        triangle = Triangle([vertex1, vertex2, vertex3], (r, g, b))
        canvas.add_triangle(triangle)
        index += 6
    return canvas