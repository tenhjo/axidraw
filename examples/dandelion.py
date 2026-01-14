# idea: draw dandelion and project into 2D

import numpy as np

from wzk import random2, geometry, mpl2

import axidraw

n = 512
x = geometry.sample_points_on_sphere_3d(shape=n)

paths = []
fig, ax = mpl2.new_fig(aspect=1)
for xx in x:
    if xx[0] < -0.1 and xx[1] > 0.2:
        a = np.random.uniform(0.1, 1.4, size=2)
        b = a + np.random.uniform(0.4, 0.6, size=2)

        # ax.plot([a[0] * xx[0] - 0.2, b[0] * xx[0]],
        #         [a[1] * xx[1], b[1] * xx[1]],
        #         color='black', linewidth=0.5)
        paths.append(np.array([[a[0] * xx[0] - 0.2, b[0] * xx[0]],
                               [a[1] * xx[1], b[1] * xx[1]]]).T)

        xx = np.array([b[0] * xx[0], b[1] * xx[1]])

    else:
        r0 = np.random.uniform(0.2, 0.5)
        # ax.plot([r0 * xx[0], xx[0]],
        #         [r0 * xx[1], xx[1]],
        #         color='black', linewidth=0.5)

        paths.append(np.array([[r0 * xx[0], xx[0]],
                               [r0 * xx[1], xx[1]]]).T)

    x1 = geometry.sample_points_on_sphere_3d(shape=3)
    for xx1 in x1:
        r0 = np.random.uniform(0.05, 0.05)
        # ax.plot([xx[0], xx[0] + xx1[0]*r0],
        #         [xx[1], xx[1] + xx1[1]*r0],
        #         color='black', linewidth=0.7)
        paths.append(np.array([[xx[0], xx[0] + xx1[0]*r0],
                               [xx[1], xx[1] + xx1[1]*r0]]).T)


x = axidraw.drawing.scale2(paths, size=axidraw.dinA_inch[6], padding=1*axidraw.cm2inch, center=True,
                           keep_aspect=True)
# x = [geometry.box(axidraw.limits_dinA[6])]

# x = axidraw.sort_paths(x)
drawing = axidraw.Drawing(x)
# drawing.render()

axidraw.draw(drawing)

# now add the stängel

# from scipy import interpolate
#
#
# nodes = np.array( [ [0, 0], [+0.3, -0.7], [-0.3, -4]])
#
# x = nodes[:, 0]
# y = nodes[:, 1]
#
# tck, u = interpolate.splprep([x, y], k=2)
# xnew, ynew = interpolate.splev( np.linspace( 0, 1, 100), tck, der=0)
#
# for i in np.linspace(-0.05, +0.05, 13):
#     ax.plot(xnew+i, ynew, color="black", zorder=-10, alpha=0.1)
