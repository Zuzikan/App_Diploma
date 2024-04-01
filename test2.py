import numpy as np


def czebyszew_nodes(n):
    return np.cos(0.5 * np.pi * (2 * np.arange(1, n + 1) - 1) / n)


def chebyshev_solver(f, a, b, n):
    d = (b - a)
    c = 0.5 * np.pi * d / n

    cn = czebyszew_nodes(n)
    v = 0.5 * (cn + 1) * d + a
    return c * np.sum(f(v) * np.sqrt(1 - cn**2))


def efunc(x):
    return np.sqrt(3 * x**2 + 7) / (5 + np.log(2*x))

print(chebyshev_solver(efunc,2 , 3, 3))


def gauss_chebyshev_quadrature(deg):
    # Compute sample points and weights
    x, w = np.polynomial.chebyshev.chebgauss(deg)

    # Example: Integrate f(x) = x^2 over [-1, 1]
    integral_approximation = np.sum(w * (x**2))

    return integral_approximation

# Example usage
degree = 60  # Choose the degree (number of sample points)
result = gauss_chebyshev_quadrature(degree)
print(f"Approximate integral: {result:.6f}")
