import numpy as np
from wzk import np2, mpl2

import axidraw

pi = np.pi
pi2 = 2*np.pi

def get_phis(n):
    x = np.arange(1,n+1)
    phi = np.arctan(1 / np.sqrt(x))
    return np.cumsum(np.hstack([np.zeros(1), phi]))


n = 150
phi = get_phis(n)
sn = np.sqrt(np.arange(1, n+1))
sn = np.hstack([np.ones(1), sn])

x = np.array([np.cos(phi)*sn,
              np.sin(phi)*sn]).T


x_center = np.zeros((len(x), 2, 2))
x_center[:, 1, :] = x


for i in range(len(x_center)):
    if phi[i] / pi2 < 1:
        continue

    phi1 = phi[:i] - (phi[i] - pi2)
    s = np.sign(phi1)
    s = s[:-1] + s[1:]

    try:
        j = np.nonzero(s == 0)[0][0]
        x_center[i, 0, :] = [np.cos(phi[i])*(sn[j]*1.1),
                             np.sin(phi[i])*(sn[j]*1.1)]
    except IndexError:
        pass

x = [x.tolist()] + x_center.tolist()
# fig, ax = mpl2.new_fig()
# ax.plot(*x.T)

x = axidraw.drawing.scale2(x, size=axidraw.dinA_inch[6], padding=2*axidraw.cm2inch, center=True,
                           keep_aspect=False)

drawing = axidraw.Drawing(x)
drawing.render()
# drawing = drawing.sort_paths()

# axidraw.draw(drawing)


# np.nonzero(phi[-1]%(2*np.pi) - phi%(2*np.pi) < 0)[0][-1]