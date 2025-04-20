import heapq as hp

class EliteSelection:
    def __init__(self, size):
      self.size = size

    def select(self, population, fitness_values_dict):
        #best_individuals = hp.nlargest(
        #     self.size,
        #     population,
        #     key=lambda ind: fitness_values_dict[hash(str(ind))]
        # )

        fitness_priority_queue = []
        counter = 0
        for individual in population:
            counter += 1
            individual_hash = hash(str(individual))
            hp.heappush(fitness_priority_queue, (-fitness_values_dict[individual_hash], counter, individual))
        
        original_queue = fitness_priority_queue.copy()
        best_individuals = []
        
        while len(best_individuals) < self.size:
            if not fitness_priority_queue:
                fitness_priority_queue = original_queue.copy()
                
            # Get the next best individual
            value,_, individual = hp.heappop(fitness_priority_queue)
            best_individuals.append(individual)
        
        return best_individuals

