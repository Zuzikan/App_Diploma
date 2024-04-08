import numpy as np

# Define the function
def f(x):
    return x**2

# Define the range and step size
start = 0
end = 5
step = 0.01

# Initialize minimum and maximum values
min_val = float('inf')
max_val = float('-inf')
min_x = None
max_x = None

# Loop over the range and compute function values
for x in np.arange(start, end, step):
    y = f(x)
    if y < min_val:
        min_val = y
        min_x = x
    if y > max_val:
        max_val = y
        max_x = x

# Print results
print("Minimum value:", min_val, "at x =", min_x)
print("Maximum value:", max_val, "at x =", max_x)