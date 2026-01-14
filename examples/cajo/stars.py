import numpy as np

from wzk import mpl2, spatial

import axidraw

directory = "/Users/jote/Documents/code/python/misc/axidraw/data/stars"
# CONSTELLATIONS = ["BigDipper", "Cas", "Gemini", "UrsaMajor", "Bootes", "Cyg", "Hydra", "UrsaMinor",
#                   "SummerTriangle", "Cassiopeia"]

CONSTELLATIONS = ["UrsaMinor", "SummerTriangle", "Cassiopeia", "Swan"]


def read_stars():
    """x, y, z, brightness"""
    stars = []
    names = dict()
    with open(f"{directory}/stars.txt") as f:
        lines = f.readlines()
        for i, s in enumerate(lines):
            s = s.replace("\n", "")
            s = s.split(" ")
            stars.append([float(s[0]), float(s[1]), float(s[2]), float(s[4])])
            if len(s) > 6:
                # print(s)
                n = " ".join(s[6:])
                n = n.split("; ")
                for nn in n:
                    names[nn] = i

    stars = np.array(stars)
    return stars, names


def read_constellation(c, star_names):
    res = []
    with open(f"{directory}/constellations/{c}.txt") as f:
        lines = f.readlines()
        for i, s in enumerate(lines):
            s = s.replace("\n", "")
            s1, s2 = s.split(",")
            res.append([star_names[s1], star_names[s2]])

    return np.array(res, dtype=int)


def read_all_constellations(star_names):
    constellations = {c: read_constellation(c=c, star_names=star_names) for c in CONSTELLATIONS}
    return constellations


def draw_constellation(ax, stars, c, color="blue"):
    x_list = []
    for i in c:
        x = stars[i, :2]
        x_list.append(x)
        ax.plot(*x.T, color=color, alpha=0.5)
    return np.array(x_list)


def draw_all_constellations(ax, constellations, stars, color="blue"):
    x_list = []
    for c in CONSTELLATIONS:
        c = constellations[c]
        x = draw_constellation(ax=ax, stars=stars, c=c, color=color)
        x_list.append(x)
    return x_list


stars, star_names = read_stars()
# stars[:, :3] = spatial.Ax(spatial.trans_euler2frame(euler=np.deg2rad([45, 0, 0])), stars[:, :3])
stars[:, :3] = spatial.Ax(spatial.rotz2frame(np.deg2rad(+140)), stars[:, :3])
stars[:, :3] = spatial.Ax(spatial.rotx2frame(np.deg2rad(+45)), stars[:, :3])
stars[:, :3] = spatial.Ax(spatial.rotz2frame(np.deg2rad(-45)), stars[:, :3])
# stars[:, 1] = -stars[:, 1]
constellations = read_all_constellations(star_names=star_names)


fig, ax = mpl2.new_fig(aspect=1)
c_list = draw_all_constellations(ax=ax, stars=stars, constellations=constellations)
ax.scatter(stars[:, 0], stars[:, 1], s=np.sqrt((1/stars[:, 3]))*5, color="black")
# ax.scatter(stars[:, 0], stars[:, 1], marker="o", ls="", color="black", markersize=2)

path = stars[:, np.newaxis, :2].tolist()
for c in c_list:
    path += c.tolist()
path = axidraw.drawing.scale2(path, size=axidraw.dinA_inch[6], padding=0.5 * axidraw.cm2inch, keep_aspect=True,
                              center=True)

path0 = path[:len(stars)]
path1 = path[len(stars):]

#
# input("change color")
# drawing = axidraw.Drawing(path1)
# axidraw.draw(drawing=drawing)
#
path0 = axidraw.sort_paths(path0)
drawing = axidraw.Drawing(path0)
axidraw.draw(drawing=drawing)