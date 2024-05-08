#!/usr/bin/env python3

# Packages
from functools import partial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import least_squares

# Registers
EARTH_GRAVITY_MS2 = 9.80665

# Functions
def err(data, p0):
    x, y, z = data.T
    x0, y0, z0, r = p0
    return np.abs(np.sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2) - r)

# Read actual data here
data = np.genfromtxt("2024-01-24-295.02K.csv", delimiter=',', skip_header=1, usecols=(8,10,12)) # np.random.random((15, 3))

error = partial(err, data)
x0, y0, z0, r = least_squares(error, (0, 0, 0, EARTH_GRAVITY_MS2)).x

print(f"x0 = {x0}, y0 = {y0}, z0 = {z0}")

# Plotting solution
fig = plt.figure()
ax = fig.add_subplot(projection = "3d")

ax.scatter(data[:, 0], data[:, 1], data[:, 2])

u, v = np.mgrid[0 : 2 * np.pi : 20j, 0 : np.pi : 10j]
x = r * np.cos(u) * np.sin(v) + x0
y = r * np.sin(u) * np.sin(v) + y0
z = r * np.cos(v) + z0
ax.plot_wireframe(x, y, z, color = "r")
ax.set_aspect("equal")
plt.savefig("offset.png")