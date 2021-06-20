import numpy as np
import matplotlib.pyplot as plt


def main():
    # 13 iterations per 8 terrain levels
    land = Landscape(13, 8)
    land.draw()


class Landscape():
    def __init__(self, iterations, levels):
        self._iter = iterations
        self._levels = levels

    def draw(self):
        perturb = 0.3  # Initial perturbation

        points_all = [[np.random.rand() / (level + 1.5),
                       np.random.rand() / (level + 1.5)]
                      for level in range(self._levels)]

        for _ in range(self._iter):
            perturb /= 2
            for level, points in enumerate(points_all):
                cur_point = 1
                while cur_point < len(points):
                    random = (np.random.rand() - 0.5) * perturb * (level + 1)
                    point = (points[cur_point] +
                             points[cur_point - 1]) / 2 + random

                    points_all[level].insert(cur_point, point)
                    cur_point += 2

        plt.style.use('dark_background')
        fig, ax1 = plt.subplots(figsize=(18, 8))
        fig.tight_layout()
        plt.ylim(bottom=0)

        clr_hills = (1, 1.35, 1.75)  # blues
        clr_background = (0.75, 0.85, 1)
        # clr_hills = (1.75, 0.9, 1.1)  # sunset
        # clr_background = (1, 0.7, 0.55)
        levels = len(points_all)

        # Colour fading with the distance
        colors = [(clr_hills[0] * (0.75 / (lvl + 2)),
                   clr_hills[1] * (1 / (lvl + 2)),
                   clr_hills[2] * (1.1 / (lvl + 2)))
                  for lvl in range(levels)]

        points_x = np.arange(len(points_all[0]))
        ax1.fill_between(points_x, 0, 1, color=clr_background)
        for level, points in enumerate(points_all):
            ax1.fill_between(points_x, 0, points, color=colors[level])
        plt.axis('off')
        plt.savefig('landscape.png', dpi=600,
                    bbox_inches='tight', pad_inches=0)
        plt.show()


if __name__ == '__main__':
    main()
