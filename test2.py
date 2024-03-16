from scipy.integrate import quad
from numpy import arccos, linspace


# Define the function to integrate
def f(x):
    return x ** 2


# Approximate the integral using the midpoint rectangular method
def midpoint_rectangular_method(f, a, b, n):
    h = (b - a) / n
    result = 0
    for i in range(n):
        xi = a + (i + 0.5) * h
        result += f(xi) * h
    return result


# Accurate integration using scipy.integrate.quad
accurate_result, _ = quad(f, 0, 10)

# Number of subintervals
n = 25

# Midpoint rectangular method approximation
approximation = midpoint_rectangular_method(f, 0, 10, n)

# Error estimation
error = abs(accurate_result - approximation)

accurate_result, approximation, error

print(f"Error estimate: {accurate_result}, {approximation}, {error}")
