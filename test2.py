import scipy.integrate as spi

def my_function(x, y):
    return x**2 + y

a, b = 0, 5  # Integration limits for x
c, d = 0, 5  # Integration limits for y

result, error = spi.nquad(my_function, [(a, b), (c, d)])
print(f"Integral result: {result:.4f}, Estimated error: {error:.4e}")