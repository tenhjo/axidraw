# import axidraw
import numpy as np

from wzk import np2, mpl2, perlin, spatial

n = 1024
img_a = perlin.perlin_noise_2d(shape=(n, n), res=4)
img_b = perlin.perlin_noise_2d(shape=(n, n), res=16)

img = (img_a*5 + img_b) / 5

f_camera = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]])


f_camera = f_camera @ spatial.roty2frame(beta=np.deg2rad(135))

camera = dict(f=f_camera, focal_length=1000)


def camera_projection(camera, x):
    focal_length = camera["focal_length"]
    f_world_camera = camera["f"]
    f_camera_world = spatial.invert(f_world_camera)

    x_camera = spatial.Ax(f_camera_world, x)

    u = x_camera[:, :2] * focal_length / x_camera[:, 2:]

    return u

x0 = np.linspace(0, 1, n)
x, y = np.meshgrid(x0, x0, indexing="ij")


x3 = np.concatenate([x[..., np.newaxis],
                     y[..., np.newaxis],
                     img[..., np.newaxis]], axis=-1)
x3 = x3.reshape(-1, 3)

x2 = camera_projection(camera=camera, x=x3)

fig, ax = mpl2.new_fig()

ax.plot(*x2.T,)

# ax.imshow(img)