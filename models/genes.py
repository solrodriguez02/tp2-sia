import random
class Gene:
    def __init__(self, name, value, min, max, is_float = False):
        if isinstance(value, int):
            if value < min or value > max:
                raise ValueError("invalid value for integer value")
        if isinstance(value, tuple):
            if value[0] < min[0] or value[0] > max[0] or value[1] < min[1] or value[1] > max[1]:
                raise ValueError("invalid value for tuple")

        self.name = name
        self.value = value
        self.min = min
        self.max = max
        self.is_float = is_float
    
    def __lt__(self, other):
        other.value < self.value

    def mutate(self):
        self.value = random.randint(min, max)

class ColorGene(Gene):
    def __init__(self, name, value):
        super().__init__(name, value, 0, 255)

class OpacityGene(Gene):
    def __init__(self, value):
        super().__init__("opacity", value, 0, 1, True)

    def mutate(self):
        self.value = random.random()

class PositionGene(Gene):
    def __init__(self, name, value, max):
        super().__init__(name, value, (0,0), max)

    def mutate(self):
        self.value = (random.randint(min[0], max[0]), random.randint(min[0], max[0]))