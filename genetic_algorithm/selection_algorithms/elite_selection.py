import heapq as hp

class EliteSelection:
    def __init__(self, size):
      self.size = size

    def select(self, population, fitness_function):
        best_individuals = hp.nlargest(
            self.size,
            population,
            key=lambda ind: fitness_function(ind)
        )
        return best_individuals

