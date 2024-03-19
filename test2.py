import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

x = sp.symbols('x')

# Define the function and its indefinite integral
f = sp.sin(x)
F = sp.integrate(f, x)

# Convert symbolic expressions to numpy functions
f_lambdified = sp.lambdify(x, f, 'numpy')
F_lambdified = sp.lambdify(x, F, 'numpy')

# Generate x values
x_vals = np.linspace(-2*np.pi, 2*np.pi, 1000)

# Generate y values for both the function and its integral
f_vals = f_lambdified(x_vals)
F_vals = F_lambdified(x_vals)

# Plotting
plt.figure(figsize=(10, 5))

# Plot the original function
plt.plot(x_vals, f_vals, label=r'$f(x) = \sin(x)$')

# Plot the indefinite integral of the function
plt.plot(x_vals, F_vals, label=r'$F(x) = -\cos(x) + C$', linestyle='--')

plt.title('Function and its Indefinite Integral')
plt.xlabel('x')
plt.ylabel('y')
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()

plt.show()