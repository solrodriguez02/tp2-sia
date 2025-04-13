from .utils.create_individuals import random_generator
from genetic_algorithm.models.individual import Canvas, Triangle


class Crossover():

    def __init__(self, triangles_amount):
        self.triangles_amount = triangles_amount

    def one_point_crossover(self, new_generation):
        childs = []
        #cross_point = random.randint(1, self.triangles_amount - 1) * 7
        cross_point = random_generator.randint(0, len(new_generation[0].chromosome) - 1)
        index = 0
        generation_shuffled = new_generation.copy()
        random_generator.shuffle(generation_shuffled)
        while index < len(new_generation) - 1:
            p1 = generation_shuffled[index]
            p2 = generation_shuffled[index + 1]

            if len(p1.chromosome) != len(p2.chromosome):
                raise ValueError("Los individuos deben tener la misma cantidad de genes")

            child1_genes = p1.chromosome[:cross_point] + p2.chromosome[cross_point:]
            child2_genes = p2.chromosome[:cross_point] + p1.chromosome[cross_point:]

            childs.append(build_canvas_from_genes(child1_genes))
            childs.append(build_canvas_from_genes(child2_genes))

            index += 2

        return childs

    def uniform_crossover(self,new_generation):
        childs = []
        index = 0
        individuals = len(new_generation)
        change_genes_probability = 0.5

        while index < individuals - 1:
        
            first_individual = new_generation[index]
            second_individual = new_generation[index + 1]

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
        
            index += 2

        return childs
    

    
def build_canvas_from_genes(chromosoma):
    canvas = Canvas()
    index = 0
    while index < len(chromosoma):
        r = chromosoma[index].value
        g = chromosoma[index+1].value
        b = chromosoma[index+2].value
        a = chromosoma[index+3].value
        vertex1 = chromosoma[index+4].value
        vertex2 = chromosoma[index+5].value
        vertex3 = chromosoma[index+6].value
        triangle = Triangle([vertex1, vertex2, vertex3], (r, g, b, a))
        canvas.add_triangle(triangle)
        index += 7
    return canvas