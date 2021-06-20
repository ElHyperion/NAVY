import json
import os
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3


def main():
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(cwd + '/ifs.json', 'r') as file:
        systems = json.load(file)

    ifs_fern = IFS(systems[0])
    ifs_tree = IFS(systems[1])

    # Calculate both systems for the specified number of points
    # The tree needs fewer points to look nice
    # Adding more points makes the drawing significantly less responsive!
    ifs_fern.calculate(40000)
    ifs_tree.calculate(10000)
    ifs_fern.draw()
    ifs_tree.draw(True)


class IFS():
    x_points = None
    y_points = None
    z_points = None

    def __init__(self, system):
        self.name = system['name']
        self.a_i = np.array(system['A_I'])
        self.j_l = np.array(system['J_L'])

    def calculate(self, points):
        print('Calculating', self.name, end='\r')

        x_z = np.array([0, 0, 0])
        self.x_points = np.array(x_z[0])
        self.y_points = np.array(x_z[1])
        self.z_points = np.array(x_z[2])

        trans_1 = self.a_i[0].reshape(3, 3)
        trans_2 = self.a_i[1].reshape(3, 3)
        trans_3 = self.a_i[2].reshape(3, 3)
        trans_4 = self.a_i[3].reshape(3, 3)

        for i in range(points):
            prg = int(i / points * 20) + 1
            prg_bar = f'[{prg * "#"}{(20 - prg) * " "}]'
            print(f'Calculating {self.name} {prg_bar} {prg * 5} %', end='\r')

            rnd = np.random.random_sample()
            if rnd < 0.25:
                x_z = np.dot(trans_1, x_z) + self.j_l[0]
            elif rnd < 0.5:
                x_z = np.dot(trans_2, x_z) + self.j_l[1]
            elif rnd < 0.75:
                x_z = np.dot(trans_3, x_z) + self.j_l[2]
            else:
                x_z = np.dot(trans_4, x_z) + self.j_l[3]

            self.x_points = np.append(self.x_points, x_z[0])
            self.y_points = np.append(self.y_points, x_z[1])
            self.z_points = np.append(self.z_points, x_z[2])

        print('')

    def draw(self, islast=False):
        print('Drawing', self.name)

        fig = plt.figure(num='IFS fractal ' + self.name, figsize=(10, 10))
        ax_1 = p3.Axes3D(fig)
        ax_1.grid(False)
        ax_1.scatter3D(self.x_points.flatten(), self.y_points.flatten(),
                       self.z_points.flatten(), c='g', s=1)
        ax_1.set_title(self.name)
        plt.show(block=islast)


if __name__ == '__main__':
    main()
