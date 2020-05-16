from random import randint

class move:
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def get_value(self):
        return randint(self.min, self.max)