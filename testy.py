import numpy as np


def min_max_fxy(f, x_range, y_range):
    min_val = float('inf')
    max_val = float('-inf')
    min_point = (None, None)
    max_point = (None, None)

    # Iterate over both x and y ranges
    for x in np.arange(x_range[0], x_range[1], 0.01):
        for y in np.arange(y_range[0], y_range[1], 0.01):
            val = f(x, y)
            if val < min_val:
                min_val = val
                min_point = (x, y)
            if val > max_val:
                max_val = val
                max_point = (x, y)

    return {"max": {"value": max_val, "point": max_point}, "min": {"value": min_val, "point": min_point}}


# Example usage
def f(x, y):
    return x +y # Example function


x_range = (0, 5)
y_range = (0, 5)

min_max_results = min_max_fxy(f, x_range, y_range)
print(min_max_results)