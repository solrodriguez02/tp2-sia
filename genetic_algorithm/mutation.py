import random

class Mutation:
    def __init__(self, mutation_probability):
        self.mutation_probability = mutation_probability

    def mutateSingleGen(self, new_generation):
        for individual in new_generation:
            change_probability = random.random()
            if change_probability < self.mutation_probability:
                random_gene_index = random.randint(0, len(individual.chromesome)-1)
                selected_gene = individual.chromesome[random_gene_index]
                selected_gene.mutate()
                individual.update_triangle_from_gene(selected_gene, random_gene_index)

    def mutateMultiplenGenes(self, new_generation, M):
        if M > 7 or M < 1:
            raise ValueError("invalid M")

        for individual in new_generation:
            genes_mutated = random.randint(1, M)
            change_probability = random.random()
            if change_probability < self.mutation_probability:
                for i in genes_mutated:
                    random_gene_index = random.randint(0, len(individual.chromesome)-1)
                    selected_gene = individual.chromesome[random_gene_index]
                    selected_gene.mutate()
                    individual.update_triangle_from_gene(selected_gene, random_gene_index)