import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Edit me first! Ends with .exe on Windows.
ffmpeg_path = '/usr/bin/ffmpeg'


def main():

    zoom_levels = [0.8, 1, 1.2, 1.5, 2, 4, 8, 15, 30, 100, 500,
                   1500, 3500, 8000, 15000, 17000, 18800, 20000]
    set_1 = Mandelbrot(x=-0.60885, y=-0.62032, iters=100, zoom=zoom_levels)

    # More detailed animation (can take several minutes to render!)
    # zoom_levels = [x / 4 for x in range(1, 13)] + [x for x in range(3, 16)] + \
    #               [x**2 for x in range(4, 65)] + [x**3 for x in range(16, 26)] + \
    #               [x**4 for x in range(12, 20)] + \
    #               [160000, 200000, 220000, 230000, 235000, 238000, 239000, 240000]
    # set_1 = Mandelbrot(x=-0.65, y=-0.375, iters=200, zoom=zoom_levels)

    set_1.calculate()
    set_1.draw()


class Mandelbrot():
    _img = None

    def __init__(self, x=0, y=0, zoom=1, iters=80, density=200):
        if isinstance(zoom, int):
            self._zoom = [(1 / zoom, zoom)]
        else:
            self._zoom = [(1 / z, z) for z in zoom]
        self._coords = (x, y)
        self._iter = iters
        self._pixels = (density * 5, density * 3)
        self._radius = 2.5

    def _calculate(self, zoom):
        off_x = self._coords[0] * zoom[1]
        off_y = self._coords[1] * zoom[1]

        x_axis = np.linspace((-2.5 + off_x) * zoom[0],
                             (2.5 + off_x) * zoom[0], self._pixels[0])
        y_axis = np.linspace((-1.5 + off_y) * zoom[0],
                             (1.5 + off_y) * zoom[0], self._pixels[1])
        grid_a, grid_b = np.meshgrid(x_axis, y_axis)
        grid = grid_a + grid_b * 1j
        grid_2 = np.zeros_like(grid)
        img = np.zeros(grid.shape)

        for i in range(self._iter):
            j = abs(grid_2) < self._radius
            grid_2[j] = grid_2[j] ** 2 + grid[j]
            img[j] = i

        return img

    def calculate(self):
        print(f'Calculating Mandelbrot for {self._iter} iterations')
        self._img = []
        for i, zoom_level in enumerate(self._zoom):
            bar_len = int(i / len(self._zoom) * 20) + 1
            prg_bar = f'[{bar_len * "#"}{(20 - bar_len) * " "}]'
            percentage = int(i / len(self._zoom) * 100)
            print(f'{prg_bar} {percentage} %', end='\r')
            self._img.append(self._calculate(zoom_level))
        print(f'[{"#" * 20}] 100 %')

    def draw(self, cmap=plt.cm.gnuplot2):
        plt.style.use('dark_background')
        fig = plt.figure(num='Mandelbrot set', figsize=(10, 6))
        plt.axis('off')

        print('Preparing animation... ')
        images = []
        for img in self._img:
            plt_img = plt.imshow(img, cmap=cmap, animated=True)
            images.append([plt_img])
        plt.savefig('mandelbrot.png', dpi=400)
        images += [[plt_img]] * 20

        anim = animation.ArtistAnimation(fig, images, interval=50, blit=True,
                                         repeat_delay=1000)

        plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path
        writer = animation.FFMpegWriter(fps=15, bitrate=4000)
        print('Saving to file... ')
        anim.save('mandelbrot_zoom.mp4', writer=writer)
        print('Done!')

        plt.show()


if __name__ == '__main__':
    main()
