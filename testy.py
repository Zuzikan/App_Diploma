import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def f(x, y):
    return x ** 2 + y ** 2


def monte_carlo_2D_integration(f, a, b, n):
    x_random = np.random.uniform(a, b, n)
    y_random = np.random.uniform(a, b, n)
    f_values = f(x_random, y_random)
    area = (b - a) * (b - a)
    integral_estimate = area * np.mean(f_values)
    return x_random, y_random, f_values, integral_estimate


# Domain boundaries
a, b, = -1, 1
n = 10000  # Number of points

# Monte Carlo Integration
x_random, y_random, f_values, integral_estimate = monte_carlo_2D_integration(f, a, b, n)

# Plotting
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Generate grid for plotting
x = np.linspace(a, b, 100)
y = np.linspace(a, b, 100)
x, y = np.meshgrid(x, y)
z = f(x, y)

# Plot the surface
ax.plot_surface(x, y, z, cmap='viridis', alpha=0.7)

# Plot the points
ax.scatter(x_random, y_random, f_values, color='r', marker='o')

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('f(x, y)')
ax.set_title(f'Monte Carlo 2D Integration Estimate: {integral_estimate:.4f}')

plt.show()
