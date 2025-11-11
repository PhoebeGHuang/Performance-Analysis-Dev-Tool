class RandomClass:
    def __init__(self, value):
        self.value = value

    def multiply(self, value):
        self.value = self.value * value

    def add(self, value):
        self.value = self.value + value

    def reset_val(self):
        self.value = 0
