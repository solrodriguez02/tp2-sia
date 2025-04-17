from genetic_algorithm.selection_algorithms.elite_selection import EliteSelection

class NextGenerationSelection:
    def __init__(self, current_generation, children):
        self.current_generation = current_generation
        self.children = children

    def apply_traditional(self, fitness_function):
        combined_gen = self.current_generation + self.children
        selection_method = EliteSelection(len(self.current_generation))
        new_generation = selection_method.select(combined_gen, fitness_function)
        return new_generation

    def apply_youth_bias(self, fitness_function):
        elite_count = max(0, len(self.current_generation) - len(self.children))
        selection_method = EliteSelection(elite_count)
        selected_parents = selection_method.select(self.current_generation, fitness_function)
        new_generation = selected_parents + self.children
        return new_generation
