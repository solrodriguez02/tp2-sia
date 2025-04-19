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

    COLOR_SENSITIVITY = {
        'Red': 1.0,
        'Green': 0.8,
        'Blue': 1.2
    }
        
    def __init__(self, name, value):
        super().__init__(name, value, 0, 255)

    def mutate(self,percent):
        delta = round((self.max_val - self.min_val) * percent * self.COLOR_SENSITIVITY[self.name])
        self.value = random_generator.randint(self.value - delta, self.value + delta)
        if self.value < self.min_val:
            self.value = self.min_val
        elif self.value > self.max_val:
            self.value = self.max_val

class OpacityGene(Gene):
    def __init__(self, value):
        super().__init__("opacity", value, 0, 1, True)

    def mutate(self, percent):
        delta = (self.max_val - self.min_val) * percent
        self.value = random_generator.uniform(self.value - delta, self.value + delta)
        if self.value < self.min_val:
            self.value = self.min_val
        elif self.value > self.max_val:
            self.value = self.max_val

class PositionGene(Gene):
    def __init__(self, name, value, max_val):
        super().__init__(name, value, (0,0), max_val)

    def mutate(self, percent):
        probability = random_generator.random()
        if probability < 0.5:
            self.mutate_x(percent)
        else:
            self.mutate_y(percent)

    def mutate_x(self, percent):
        delta = (self.max_val[0] - self.min_val[0]) * percent
        self.value = (random_generator.uniform(self.value[0] - delta, self.value[0] + delta), self.value[1])
        if self.value[0] < self.min_val[0]:
            self.value = (self.min_val[0], self.value[1])
        elif self.value[0] > self.max_val[0]:
            self.value = (self.max_val[0], self.value[1])

    def mutate_y(self, percent):
        delta = (self.max_val[1] - self.min_val[1]) * percent
        self.value = (self.value[0], random_generator.uniform(self.value[1] - delta, self.value[1] + delta))
        if self.value[1] < self.min_val[1]:
            self.value = (self.value[0], self.min_val[1])
        elif self.value[1] > self.max_val[1]:
            self.value = (self.value[0], self.max_val[1])