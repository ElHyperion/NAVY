from random import uniform as rand
from math import copysign as sgn


class Perceptron:
    weights = []
    bias = rand(-1, 1)
    learning_rate = 0.0

    def __init__(self, learning_rate, function):
        self.function = function
        self.weights = [rand(-1, 1)] * 2
        self.learning_rate = learning_rate

    def train(self, inputs, expected, bias=None):
        input_sum = inputs[0] * self.weights[0] + inputs[1] * self.weights[1]
        result = self.function(input_sum + self.bias)
        error = expected - result
        for i in range(0, len(inputs)):
            self.weights[i] += error * inputs[i] * self.learning_rate
        if bias is not None:
            self.bias = bias
        else:
            self.bias += error * self.learning_rate
        return result

    def run(self, inputs, bias=None):
        input_sum = inputs[0] * self.weights[0] + inputs[1] * self.weights[1]
        if bias is not None:
            self.bias = bias
        return self.function(input_sum + self.bias)
