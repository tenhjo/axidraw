import numpy as np
from wzk import spatial
import axidraw

n = 1000
seed = 2
np.random.seed(2)
n_body = 30
line1 = axidraw.plotting.get_wobbly_line(n=n, m=20, meet_ends="linear-shift", mi=-0.2, ma=+0.2, x0=0)
line2 = axidraw.plotting.get_wobbly_line(n=n, m=4, meet_ends="linear-shift", mi=0, ma=+10, x0=0)
rr = axidraw.plotting.line_transition(lines=[line1, line2], n=n_body)
x = [np.array([np.linspace(0, 1, n), rrr+i*0.4]) for (i, rrr) in enumerate(rr)]
x = np.array(x).transpose((0, 2, 1))
x_body = x[:, :, ::-1]

x_body[..., 0] = x_body[..., 0]/5 - 12
x_body[..., 1] = x_body[..., 1]*40 - 18
x_body = x_body.tolist()
for i in range(n_body-1):
    x_body[i] = x_body[i][10*i:n-10*i:5]


n_eyes = 10
line1 = axidraw.plotting.get_wobbly_line(n=n, m=4, meet_ends="linear-shift", mi=-0.5, ma=+0.5, x0=0)
line2 = axidraw.plotting.get_wobbly_line(n=n, m=4, meet_ends="linear-shift", mi=-0.5, ma=+0.5, x0=0)
rr = axidraw.plotting.line_transition(lines=[line1, line2], n=n_eyes)
x = [np.array([np.linspace(0, 1, n), rrr+i*0.0]) for (i, rrr) in enumerate(rr)]
x = np.array(x).transpose((0, 2, 1))
x[..., 0] *= 6
x[..., 1] *= 1
dcm = spatial.transform_2d.theta2dcm(np.deg2rad(+30))
x = (dcm @ x[..., np.newaxis])[..., 0]

x[..., 0] += 13
x[..., 1] -= 9
x_eye_1 = x[:, ::10, ::-1]

x_eye_1 = x_eye_1.tolist()


x_house = axidraw.plotting.theodorus_spiral(n=135, alpha=1.1)
rr = axidraw.plotting.line_transition(lines=[line1, line2], n=n_body)


# TODO general line trafo betetween (0, 0) (0, 1) to go between a and b

x = x_body + x_house + x_eye_1
x = axidraw.drawing.scale2(x, size=axidraw.dinA_inch[6], padding=0.5*axidraw.cm2inch, center=True,
                           keep_aspect=True)

# drawing = axidraw.Drawing(x)
# drawing.render(title=str(seed))

x_body = x[:len(x_body)]
x_house = x[len(x_body):-len(x_eye_1)]
x_eye = x[-len(x_eye_1):]



input("change color - body")
x_body = axidraw.sort_paths(x_body)
drawing = axidraw.Drawing(x_body)
drawing.render(title=str(seed))
axidraw.draw(drawing)

input("change color - eye")
# x_eye = axidraw.sort_paths(x_eye)
drawing = axidraw.Drawing(x_eye)
drawing.render(title=str(seed))
axidraw.draw(drawing)


input("change color - house")
# x_house = axidraw.sort_paths(x_house)
drawing = axidraw.Drawing(x_house)
drawing.render(title=str(seed))
axidraw.draw(drawing)
#
