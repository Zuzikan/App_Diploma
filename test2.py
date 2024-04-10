import numpy as np
import matplotlib.pyplot as plt

# Define the function f(x) = 2x + 1
def f(x):
    return x

# Generate 20 random x values between -10 and 10
x_random = np.random.uniform(-10, 10, 20)

# Generate 20 random y values; this method generates points that may or may not lie on the function
y_random = np.random.uniform(-20, 30, 20) # Adjusted range to cover possible y values of f(x)

# Plotting the function and the random points
x_plot = np.linspace(-10, 10, 400)
y_plot = f(x_plot)

plt.figure(figsize=(10, 6))
plt.plot(x_plot, y_plot, label='f(x) = 2x + 1', color='blue')
plt.scatter(x_random, y_random, color='red', label='Random Points')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Function and Random Points')
plt.grid(True)


# Check if the points lie on the function with a threshold
threshold = 0.001
points_on_function = np.abs(f(x_random) - y_random) < threshold
points_under_function = y_random < f(x_random)
points_above_function = y_random > f(x_random)

# Counting how many points are under the function
num_points_under_function = np.sum(points_under_function)
num_points_above_function = np.sum(points_above_function)
num_points_on_function = np.sum(points_on_function)
print("under:")
print(num_points_under_function, points_under_function)
print("on:")
print(num_points_on_function, points_on_function)
print("above:")
print(num_points_above_function, points_above_function)
plt.show()