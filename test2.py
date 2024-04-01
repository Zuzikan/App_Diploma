import numpy as np


def chebyshev_nodes(n):
    return np.cos(0.5 * np.pi * (2 * np.arange(1, n + 1) - 1) / n)


def chebyshev_solver(f, a, b, n):
    d = (b - a)
    c = 0.5 * np.pi * d / n

    cn = chebyshev_nodes(n)
    v = 0.5 * (cn + 1) * d + a
    return c * np.sum(f(v) * np.sqrt(1 - cn**2))


def efunc(x):
    return (x**2-1)**3*np.cos(x)

print(chebyshev_solver(efunc,0 , 2, 3))



