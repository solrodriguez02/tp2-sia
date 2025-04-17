from .utils.create_individuals import random_generator
class Mutation:
    def __init__(self, mutation_probability, triangles_per_solution):
        self.mutation_probability = mutation_probability
        self.triangles_per_solution = triangles_per_solution

    def mutateSingleGen(self, new_generation):
        for individual in new_generation:
            if random_generator.random() < self.mutation_probability:
                gene_index = random_generator.randint(0, len(individual.chromosome) - 1)
                self._mutate_gene(individual, gene_index)

    def mutateMultipleGenes(self, new_generation):
        M = self.triangles_per_solution*7

        for individual in new_generation:
            if random_generator.random() < self.mutation_probability:
                genes_to_mutate = random_generator.randint(1, M)
                indices = random_generator.sample(range(len(individual.chromosome)), min(genes_to_mutate, len(individual.chromosome)))
                for gene_index in indices:
                    self._mutate_gene(individual, gene_index)

    def _mutate_gene(self, individual, gene_index):
        gene = individual.chromosome[gene_index]
        gene.mutate()
        individual.update_triangle_from_gene(gene, gene_index)
