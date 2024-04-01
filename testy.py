from scipy.integrate import quad
import numpy as np

# Define the function for Gauss-Chebyshev quadrature (since the weighting function is part of the method, we use f(x) = 1)
def f(x):
    return x**2

# Number of nodes for Gauss-Chebyshev quadrature
n = 10

# Gauss-Chebyshev nodes and weights (for Chebyshev polynomials of the first kind)
nodes = np.cos(np.pi * (np.arange(1, n + 1) - 0.5) / n)
weights = np.pi / n * np.ones(n)

# Approximate integral using Gauss-Chebyshev quadrature
approx_integral = sum(weights * f(nodes))

# Exact integral of 1/sqrt(1-x^2) over [-1, 1] is pi
exact_integral = np.pi

# Calculate the error
error = np.abs(approx_integral - exact_integral)

print(approx_integral, exact_integral, error)
