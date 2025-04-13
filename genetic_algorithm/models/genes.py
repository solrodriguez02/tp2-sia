import random

random_generator = random.Random()
random_generator.seed(43)

class Gene:
    def __init__(self, name, value, min_val, max_val, is_float = False):
        if isinstance(value, int):
            if value < min_val or value > max_val:
                raise ValueError("invalid value for integer value")
        if isinstance(value, tuple):
            if value[0] < min_val[0] or value[0] > max_val[0] or value[1] < min_val[1] or value[1] > max_val[1]:
                raise ValueError("invalid value for tuple")

        self.name = name
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.is_float = is_float

    def mutate(self):
        self.value = random_generator.randint(self.min_val, self.max_val)

class ColorGene(Gene):
    def __init__(self, name, value):
        super().__init__(name, value, 0, 255)

class OpacityGene(Gene):
    def __init__(self, value):
        super().__init__("opacity", value, 0, 1, True)

    def mutate(self):
        self.value = random_generator.random()

class PositionGene(Gene):
    def __init__(self, name, value, max_val):
        super().__init__(name, value, (0,0), max_val)

    def mutate(self):
        self.value = (random_generator.randint(self.min_val[0], self.max_val[0]), random_generator.randint(self.min_val[0], self.max_val[1]))