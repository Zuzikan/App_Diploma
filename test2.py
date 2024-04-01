import matplotlib.pyplot as plt
from numpy import linspace, sqrt, log
from scipy.special import roots_chebyt

# Definicja funkcji
def f(x):
    return sqrt(3 * x**2 + 7) / (5 + log(2*x))

# Przedział
a, b = 2, 3

# Liczba węzłów
n = 3

# Zmiana zmiennych dla węzłów Czebyszewa
t_nodes, _ = roots_chebyt(n)
x_nodes = (b - a) / 2 * t_nodes + (b + a) / 2
y_nodes = f(x_nodes)

# Rysowanie funkcji
x = linspace(a, b, 400)
y = f(x)
plt.plot(x, y, label='Funkcja $\\sqrt{3x^2 + 7} / (5 + \\log(2x))$', color='blue')

# Zaznaczenie węzłów kwadratury Gaussa-Czebyszewa
plt.scatter(x_nodes, y_nodes, color='red', label='Węzły Gaussa-Czebyszewa')

plt.fill_between(x, y, color='skyblue', alpha=0.3)
plt.title('Wykres funkcji i węzły kwadratury Gaussa-Czebyszewa')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()

# Wyświetlenie wykresu
plt.show()
