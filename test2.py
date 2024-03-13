import sympy as sp


def estimate_rectangular_method_error(a, b, n, f_expr):
    """
    Estimate the error of the Rectangular (Midpoint) Method for numerical integration.

    Parameters:
    - a: The lower limit of integration.
    - b: The upper limit of integration.
    - n: The number of subintervals (rectangles).
    - f_expr: A sympy expression representing the function f(x).

    Returns:
    - The estimated error of the Rectangular Method.
    """
    # Define the symbol
    x = sp.symbols('x')

    # Calculate the second derivative of the function
    f_second_derivative = sp.diff(f_expr, x, 2)

    # Find the maximum value of the second derivative in the interval [a, b]
    # Note: For simplicity, this example just evaluates the second derivative at the endpoints
    # and the midpoint. For a more accurate estimate, you could use optimization methods.
    f_second_derivative_max = max(f_second_derivative.subs(x, a),
                                  f_second_derivative.subs(x, b),
                                  f_second_derivative.subs(x, (a + b) / 2))

    # Calculate the error estimate
    error_estimate = ((b - a) ** 3 / (24 * n ** 2)) * f_second_derivative_max

    return error_estimate


# Example usage
if __name__ == "__main__":
    # Define the function to integrate as a sympy expression
    f_expr = sp.sympify('x**2 + 2*x + 1')

    # Define the integration interval and number of subintervals
    a, b, n = 0, 10, 100

    # Estimate the error
    error_estimate = estimate_rectangular_method_error(a, b, n, f_expr)
    print(f"Estimated error: {error_estimate}")
