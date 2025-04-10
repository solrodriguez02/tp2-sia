import heapq as hp

class EliteSelection:
    def __init__(self, size):
      self.size = size

    def select(self, population, fitness_function):
        fitness_priority_queue = []
        for individual in population:
            hp.heappush(fitness_priority_queue, (fitness_function(individual), individual))
        
        original_queue = fitness_priority_queue.copy()
        best_individuals = []
        
        while len(best_individuals) < self.size:
            if not fitness_priority_queue:
                fitness_priority_queue = original_queue.copy()
                
            # Get the next best individual
            value, individual = hp.heappop(fitness_priority_queue)
            best_individuals.append(individual)
        
        return best_individuals

