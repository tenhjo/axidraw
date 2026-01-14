import numpy as np
from wzk import mpl2
import axidraw

size = axidraw.dinA_inch[4]
pad = 0.03
line_height = 0.1
n_address_lines = 4
point_size = 12


directory = '/Users/jote/Documents/code/python/misc/axidraw/data/svg'
file = 'one-piece/gum-gum-fruit.svg'
file = 'Obelix-and-Asterix-Crying.svg'
file = 'Obelix-with-Dogmatix.svg'
# file = 'birds/bird_0.svg'

drawing = axidraw.drawing.Drawing.load(f"{directory}/{file}")

drawing = axidraw.drawing.scale2(x=drawing.paths, size=size, padding=1.0, mi=0, ma=1, keep_aspect=False,
                                 center=False)
drawing = axidraw.Drawing(drawing)
drawing.render()



# A
from xml.dom import minidom

doc = minidom.parse(f"{directory}/{file}")  # parseString also exists
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()


# B
from svg.path import parse_path
from svg.path.path import Line
from xml.dom import minidom

# read the SVG file
doc = minidom.parse(f"{directory}/{file}")
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()

# print the line draw commands
for path_string in path_strings:
    path = parse_path(path_string)
    for e in path:
        if isinstance(e, Line):
            x0 = e.start.real
            y0 = e.start.imag
            x1 = e.end.real
            y1 = e.end.imag
            print("(%.2f, %.2f) - (%.2f, %.2f)" % (x0, y0, x1, y1))



from svgpathtools import svg2paths


def svg_to_coordinates(svg_file):
    num_points = 500  # Number of points to sample

    paths, attributes = svg2paths(svg_file)

    xy_paths = []

    for path in paths:
        xy_path = []
        for segment in path:

            points = np.array([segment.point(t) for t in np.linspace(0, 1, num_points)])
            xy_paths.extend([[point.real, point.imag] for point in points])

    return np.array(xy_paths)


xy = svg_to_coordinates(svg_file=f"{directory}/{file}")
d_xy = np.linalg.norm(xy[1:, :] - xy[:-1, :], axis=-1)
i = np.array(np.nonzero(d_xy > 10)[0] + 1, dtype=int)
paths = np.split(xy, i, axis=0)


# ax.plot(*np.array(paths[0]).T, color="black")
# ax.plot(*np.array(paths[1]).T, color="black")
# ax.plot(*np.array(paths[2]).T, color="black")
# ax.plot(*np.array(paths[3]).T, color="black")

fig, ax = mpl2.new_fig()
for i, xy in enumerate(paths):
    ax.plot(*np.array(xy).T, color="black", lw=1)
