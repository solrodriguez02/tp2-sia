import random



class Crossover:

    def one_point_crossover(self,new_generation):
        childs = []
        cross_point = random.randint(0, 7 - 1)
        index = 0
        individuals = len(new_generation)
        while index < individuals - 1:
        
            first_individual = new_generation[index]
            second_individual = new_generation[index + 1]

            if len(first_individual.triangles) != len(second_individual.triangles):
                raise ValueError("individuals must have the same number of triangles")
            
            #while chromosome_index < len(first_individual.chromosome):
                #first_parent = first_individual.chromosome[chromosome_index]
                #second_parent = second_individual.chromosome[chromosome_index]

            first_child = first_individual.chromosome[0:cross_point] + second_individual.chromosome[cross_point:]
            second_child = second_individual.chromosome[0:cross_point] + first_individual.chromosome[cross_point:]

            childs.append(first_child)
            childs.append(second_child)
        
            index += 2

        return childs
            
    
    def uniform_crossover(self,new_generation):
        childs = []
        index = 0
        individuals = len(new_generation)
        while index < individuals - 1:
        
            first_individual = new_generation[index]
            second_individual = new_generation[index + 1]

            if len(first_individual.triangles) != len(second_individual.triangles):
                raise ValueError("individuals must have the same number of triangles")
            
            chromosome_index = 0
            
            while chromosome_index < len(first_individual.chromosome):
                first_parent = first_individual.chromosome[chromosome_index]
                second_parent = second_individual.chromosome[chromosome_index]

                first_child = []
                second_child = []

                change_genes_probability = 0.5

                for i in range(len(first_parent)):
                    if random.random() > change_genes_probability:
                        first_child.append(first_parent[i])
                        second_child.append(second_parent[i])
                    else:
                        first_child.append(second_parent[i])
                        second_child.append(first_parent[i])

                childs.append(first_child)
                childs.append(second_child)

                chromosome_index += 1
        
            index += 2

        return childs
    