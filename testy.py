from sympy import sympify, simplify

# Example expression
expr_string = "x**2 + 3*x - 1/2 + acos(x)"

# Parsing the string to a sympy expression
expr = sympify(expr_string)

# Display the parsed expression
print(f"Parsed Expression: {expr}")

# Evaluate the expression for a specific value of x
x_value =0.23
evaluated_expr = expr.subs('x', x_value)
numeric_value = evaluated_expr.evalf()
print(f"Evaluated at x={x_value}: {evaluated_expr}")
print(f" x={x_value}: {numeric_value}")

