from random import uniform as rand
import numpy as np
import matplotlib.pyplot as plt
from perceptron import Perceptron


POINTS = [(rand(-1, 1), rand(-1, 1)) for x in range(0, 100)]
EPOCHS = 1000
LEARNING_RATE = 0.1


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def d_sigmoid(x):
    return x * (1 - x)


p1 = Perceptron(LEARNING_RATE, sigmoid)
p2 = Perceptron(LEARNING_RATE, sigmoid)
p3 = Perceptron(LEARNING_RATE, d_sigmoid)

expected_outputs = (0, 1, 1, 0)
training_inputs = (
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1)
)

# Run the neural network
for e in range(0, EPOCHS):
    for i, input in enumerate(training_inputs):
        expected = expected_outputs[i]
        output_h1 = p1.run(input, bias=1)
        output_h2 = p2.run(input, bias=1)
        output_h = output_h1 + output_h2

        output_o = p3.run((output_h1, output_h2), bias=1)
        error_o = (expected - output_o)
        d_output_o = error_o * d_sigmoid(output_o)

        error_h = d_output_o * p3.weights[0] + d_output_o * p3.weights[1]
        d_hidden = error_h * d_sigmoid(output_h)

        # print(input[0], p1.weights[0], p1.learning_rate)
        p1.weights[0] += input[0] * d_hidden * p1.learning_rate
        p1.weights[1] += input[1] * d_hidden * p1.learning_rate
        p2.weights[0] += input[0] * d_hidden * p2.learning_rate
        p2.weights[1] += input[1] * d_hidden * p2.learning_rate
        p3.weights[0] += output_h1 * d_output_o * p3.learning_rate
        p3.weights[1] += output_h2 * d_output_o * p3.learning_rate

print(p1.weights[0], p1.weights[1], p2.weights[0], p2.weights[1])
