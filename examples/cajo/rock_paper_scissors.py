import numpy as np

from wzk import mpl2, geometry


def plot(ax, paths):
    for p in paths:
        ax.plot(*np.array(p).T, color="black")


# Rock
rock_outline = [
    (50, 60), (55, 50), (65, 45), (75, 47),
    (85, 55), (88, 65), (85, 75), (75, 80),
    (65, 78), (60, 72), (55, 70), (52, 65),
    (50, 60)
]

rock_cracks = [
    [(60, 60), (65, 55)],
    [(70, 65), (75, 60), (78, 65)],
    [(68, 72), (66, 68), (62, 70)],
    [(70, 55), (68, 50), (75, 47)],
    [(55, 58), (58, 62)]
]

rock = [rock_outline] + rock_cracks


# Paper
paper_outline = [
    (100, 40), (140, 38), (142, 45), (140, 80),
    (100, 82), (98, 75), (100, 65), (98, 50), (100, 40)
]

paper_lines = [
    [(105, 46), (135, 47)],
    [(105, 56), (135, 57)],
    [(105, 65), (135, 66)],
    [(105, 74), (135, 74)],

]

paper = [paper_outline] + paper_lines


# Scissor
scissors = [
            # [[4, 8.5], [8, 0.8], [7.5, 1], [3, 7.5]],
            [[4, 8.5], [5, 6.575], [4.417, 5.45], [3, 7.5]],
            [[5.585, 5.45], [8, 0.8], [7.5, 1], [5, 4.611]],
            [[6, 8.5], [2, 0.8], [2.5, 1], [7, 7.5]],
            geometry.get_points_on_circle(x=[3, 8.5], r=1, n=100)[0],
            geometry.get_points_on_circle(x=[3, 8.5], r=0.7, n=100)[0],
            geometry.get_points_on_circle(x=[7, 8.5], r=1, n=100)[0],
            geometry.get_points_on_circle(x=[7, 8.5], r=0.7, n=100)[0],
            geometry.get_points_on_circle(x=[5, 5.5], r=0.3, n=100)[0],
            ]

fig, ax3 = mpl2.new_fig(n_cols=3, aspect=1)

plot(ax3[0], rock)
plot(ax3[1], paper)
plot(ax3[2], scissors)

fig.show()



import numpy as np

from wzk import mpl2, ltd

import axidraw
from axidraw.paths import (simplify_paths, sort_paths, join_paths, crop_paths,
                           convex_hull, expand_quadratics, paths_length)

from axidraw import units


x = axidraw.drawing.scale2(x=rock, size=axidraw.dinA_inch[6][::-1], padding=1, keep_aspect=True, center=True)
drawing = axidraw.Drawing(x)
# drawing.render()
axidraw.draw(drawing=drawing)
