from cmath import acos

import sympy
from sympy import symbols, S, sqrt, log, solveset, Interval, acos

x = symbols('x')

# Dla funkcji z pierwiastkiem kwadratowym
expr1_domain = solveset(sqrt(x - 2) > 0, x, domain=S.Reals)

# Dla funkcji logarytmicznej
expr2_domain = solveset(2/(x-3) > 0, x, domain=S.Reals)

# Przygotowanie formatowania na przedziały (a, b)
def format_interval(interval):
    if isinstance(interval, Interval):
        return f"({interval.start}; {interval.end})"
    else:
        # Jeśli rozwiązanie nie jest przedziałem, zwróć oryginalny format
        return str(interval)

# Formatowanie i wyświetlanie wyników
expr1_domain_formatted = format_interval(expr1_domain)
expr2_domain_formatted = format_interval(expr2_domain)

print(expr1_domain_formatted, expr2_domain_formatted)
