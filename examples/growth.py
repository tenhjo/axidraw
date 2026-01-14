import random
import numpy as np
from wzk import mpl2

from collections import defaultdict
from math import pi, sin, cos, hypot, floor
from shapely.geometry import LineString
import axidraw


class Grid(object):
    def __init__(self, r):
        self.r = r
        self.size = r / 2 ** 0.5
        self.points = {}
        self.lines = {}

    def normalize(self, x, y):
        i = int(floor(x / self.size))
        j = int(floor(y / self.size))
        return i, j

    def nearby(self, x, y):
        points = []
        lines = []
        i, j = self.normalize(x, y)
        for p in range(i - 2, i + 3):
            for q in range(j - 2, j + 3):
                if (p, q) in self.points:
                    points.append(self.points[(p, q)])
                if (p, q) in self.lines:
                    lines.append(self.lines[(p, q)])
        return points, lines

    def insert(self, x, y, line=None):
        points, lines = self.nearby(x, y)
        for bx, by in points:
            if hypot(x - bx, y - by) < self.r:
                return False
        i, j = self.normalize(x, y)
        if line:
            for other in lines:
                if line.crosses(other):
                    return False
            self.lines[(i, j)] = line
        self.points[(i, j)] = (x, y)
        return True

    def remove(self, x, y):
        i, j = self.normalize(x, y)
        self.points.pop((i, j))
        self.lines.pop((i, j))


def max_angle(i, d):
    if d < 0.1:
        return pi
    return pi / 4


def new_angle(a, d):
    # return random.gauss(a, pi / 20)

    if d < 0.1:
        return random.random() * 2 * pi
    else:
        return random.gauss(a, pi / 10)


def choice(items):
    p = random.random() ** 0.5
    return items[int(p * len(items))]


def poisson_disc(x1, y1, x2, y2, r, n):
    grid = Grid(r)
    active = []
    x = (x1 + x2) / 2.0
    y = (y1 + y2) / 2.0
    a = random.random() * 2 * pi
    b = random.random() * 2 * pi
    grid.insert(x, y-1)
    active.append((x, y-1, a, 0, 0, 0))

    grid.insert(x, y+1)
    active.append((x, y+1, b, 0, 0, 1))
    # fig, axx = mpl2.new_fig()
    eps = 1e-6
    pairs = [((a[0], a[1]), (a[0]+eps, a[1]+eps)) for a in active]

    ii = 0
    while active:
        # ax, ay, aa, ai, ad, ag = record = choice(active)
        npactive = np.array(active)
        try:
            iii = np.arange(len(active))[npactive[:, -1] == ii][-1]
        except IndexError:
            iii = -1
        ax, ay, aa, ai, ad, ag = record = active[iii]
        for i in range(n):
            a = new_angle(aa, ad)
            d = random.random() * r + r
            x = ax + cos(a) * d
            y = ay + sin(a) * d
            if x < x1 or y < y1 or x > x2 or y > y2:
                ii = (ii + 1) % 2
                continue
            if ad + d > 3.25:
                ii = (ii + 1) % 2
                continue
            pair = ((ax, ay), (x, y))
            line = LineString(pair)
            if not grid.insert(x, y, line):
                continue
            pairs.append(pair)
            # axx.plot(*np.array(pair).T, color=)
            # mpl2.plt.pause(0.01)
            active.append((x, y, a, ai + 1, ad + d, ag))
            # active.sort(key=lambda x: -x[4])
            break
        else:
            active.remove(record)
    return grid.points.values(), pairs


def make_path(pairs, i=0):
    lookup = defaultdict(list)
    for parent, child in pairs:
        lookup[parent].append(child)
    path = []
    root = pairs[i][0]
    stack = []
    stack.append(root)
    while stack:
        point = stack[-1]
        path.append(point)
        if not lookup[point]:
            stack.pop()
            continue
        child = lookup[point].pop()
        stack.append(child)

    return path


def main():
    # random.seed(68)
    # for seed in range(125, 35):
    seed = 129
    random.seed(seed)
        # points, pairs = poisson_disc(x1=0, y1=0, x2=11, y2=8.5, r=0.035, n=32)
    points, pairs = poisson_disc(x1=0, y1=0, x2=axidraw.dinA_inch[6][0], y2=axidraw.dinA_inch[6][1], r=0.04, n=32)
    path0 = make_path(pairs, i=0)
    path1 = make_path(pairs, i=1)

    path = path0 + path1

    path = np.array(path)
    pp = np.unique(path, axis=0)
    print(pp.shape)
    print(path.shape)
    # from wzk import mpl2
    # fig, ax = mpl2.new_fig(aspect=1)
    # for i in range(len(path)-1):
    #     ax.plot(*path[i:i+2, :].T, color='black', lw=0.5)
    #     mpl2.plt.pause(0.001)

    path = axidraw.drawing.scale2(path, size=axidraw.dinA_inch[6], padding=0.5*axidraw.cm2inch, keep_aspect=True,
                                  center=True)

    path00 = [path[0][:len(path0)]]
    path11 = [path[0][len(path0):]]
    drawing = axidraw.Drawing(path00)
    ax = drawing.render(dinA=6, color="blue")
    axidraw.draw(drawing=drawing)
    input("change color")

    drawing = axidraw.Drawing(path11)
    # drawing.render(dinA=6, ax=ax, color="red", title=f"{seed}")
    axidraw.draw(drawing=drawing)
    a = 1

if __name__ == '__main__':
    # points, pairs = poisson_disc(0, 0, 11, 8.5, 0.035, 32)
    # path = make_path(pairs)
    main()
#