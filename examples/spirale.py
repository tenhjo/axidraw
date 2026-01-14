import numpy as np
from wzk.mpl2 import new_fig

import axidraw

pi = np.pi
n = 7000
t_end = 2*np.pi * 20

phi = np.linspace(0, t_end, n)
r = np.linspace(1, 0.1, n) **3

x = np.array((np.cos(phi), np.sin(phi))).T * r[:, np.newaxis]


x = axidraw.drawing.scale2(x=x, size=axidraw.dinA_inch[6], padding=0.5, keep_aspect=True, center=True)

drawing = axidraw.Drawing(x)
# drawing.render()
# input()
axidraw.draw(drawing=drawing)
#