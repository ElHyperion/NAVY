from random import uniform as rand
from math import copysign as sgn
import matplotlib.pyplot as plt


points = [(rand(-10, 10), rand(-10, 10)) for x in range(0, 100)]
learning_rate = 1000
epochs = 100


class Perceptron:
    weights = [0, 0]
    slope, intercept = 0.0, 0.0
    bias = rand(-1, 1)

    def __init__(self, slope, intercept):
        self.slope = slope
        self.intercept = intercept
        self.weights = [rand(-1, 1), rand(-1, 1)]

    def above_line(self, x, y):
        if y < self.slope * x + self.intercept:
            return -1  # Under the line
        elif y > self.slope * x + self.intercept:
            return 1   # Above the line
        else:
            return 0   # On the line

    def train(self, x, y):
        result = sgn(1, x * self.weights[0] + y * self.weights[1] + self.bias)
        expected = self.above_line(x, y)
        error = expected - result
        self.weights[0] += error * x * learning_rate
        self.weights[1] += error * y * learning_rate
        self.bias += error * learning_rate
        return result

    def run(self, x, y):
        return sgn(1, x * self.weights[0] + y * self.weights[1] + self.bias)


p1 = Perceptron(4, -5)

plt.style.use('dark_background')


# 1 Training phase
for e in range(0, epochs):
    for point in points:
        p1.train(point[0], point[1])


point_colours = []
new_points = []
sc = plt.scatter([], [], color='g')


plt.ylim(-10, 10)
plt.xlim(-10, 10)
plt.grid(which='major', color='darkblue')
plt.plot([-100, 100], [-4 * 100 - 5, 4 * 100 - 5], '-r', color='yellow')
plt.show(block=False)


def update_graph():
    sc.set_offsets(new_points)
    sc.set_color(point_colours)
    plt.draw()
    plt.pause(1e-17)


# 2 Testing phase
for i in range(0, len(points)):
    point = points[i]
    new_points.append(point)
    if p1.run(point[0], point[1]) == 1:
        point_colours.append('g')
    else:
        point_colours.append('r')
    update_graph()


# Graph drawing

plt.draw()
plt.pause(1e-17)

points_unzip = list(zip(*points))
plt.scatter(list(points_unzip)[0], list(points_unzip)[1], color=point_colours)
plt.plot([-100, 100], [-4 * 100 - 5, 4 * 100 - 5], '-r', color='yellow')

plt.show()
