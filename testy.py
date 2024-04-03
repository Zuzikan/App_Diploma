import numpy as np


n=1000
a=0
b=10
def f(x):
    return x**2

def punkty( n, a, b):

    random_points_x = np.random.uniform(a, b, n)
    random_points_y = np.random.uniform(f(a), f(b), n)
    return random_points_x, random_points_y


ar_x, ar_y = punkty(n, a, b)
f_values_at_ar_x = np.array([f(x) for x in ar_x])

points_under_or_on_curve = ar_y <= f_values_at_ar_x
points_above_curve = ~points_under_or_on_curve
num_points_under_or_on_curve = np.sum(points_under_or_on_curve)
num_points_above_curve = np.sum(points_above_curve)


print(num_points_under_or_on_curve, num_points_above_curve)