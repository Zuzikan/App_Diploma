import sys
import numpy as np
import timeit
import math
from scipy.optimize import minimize
from scipy.special import roots_chebyt
from scipy.integrate import quad, nquad
from scipy.interpolate import CubicSpline
from sympy import sympify, lambdify, solve
from PyQt5.QtCore import Qt, QCoreApplication, QLocale
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QComboBox, QLineEdit, QSlider, QHBoxLayout,
                             QPushButton, QDialog, QTabWidget, QVBoxLayout, QWidget)
from PyQt5.QtGui import QDoubleValidator, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from sympy.core.sympify import SympifyError

import instrukcja
from metody import metoda_monte
from obliczenia import (oblicz_boole, oblicz_herm, obliczenia_czeb, oblicz_monte, oblicz_regula_3_8,
                        oblicz_metoda_prostokatow, oblicz_nieoznaczone, oblicz_simpson, oblicz_trapez)
import PyQt5.QtGui as qtg


class ObliczMonte2(QDialog):
    def __init__(self):
        super().__init__()
        self.maximum = None
        self.minimum = None
        self.ar_x = None
        self.ar_y = None
        self.ar_z = None
        self.initUI()

    def initUI(self):

        # self.setStyleSheet("background-color: white;")
        self.setWindowIcon(qtg.QIcon('zdjecia/icon.png'))

        self.font = QFont()
        self.font.setPointSize(9)

        layout = QGridLayout()
        sliderLayout = QHBoxLayout()
        abHorizontal = QHBoxLayout()
        layout_for_buttons = QHBoxLayout()

        self.combo = QComboBox(self)
        l1 = QLabel("Porównaj z: ", self)
        self.error_ocurred = False
        l2 = QLabel("Wpisz równanie: ", self)
        l3 = QLabel("Podaj przedział [a,b]:", self)
        self.rownanie = QLineEdit(self)
        instrukcja = QPushButton('Instrukcja', self)
        la = QLabel("a: ", self)
        lb = QLabel("b:", self)
        self.a = QLineEdit(self)
        self.b = QLineEdit(self)
        self.n = QLineEdit(self)
        self.l6 = QLabel(self)
        self.l6l = QLabel(self)
        self.l7 = QLabel(self)
        self.l8 = QLabel(self)
        self.l8l = QLabel(self)
        self.l8r = QLabel(self)
        self.l9 = QLabel(self)
        self.l9l = QLabel(self)
        self.l9r = QLabel(self)
        oblicz = QPushButton('Oblicz', self)
        self.wartosc = QLabel("Liczba punktów:", self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.toolbar = NavigationToolbar(self.canvas2, self)
        self.toolbar2 = NavigationToolbar(self.canvas, self)

        instrukcja.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        oblicz.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        self.l7.setStyleSheet('color: red')

        validator = QDoubleValidator()
        validator.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.a.setPlaceholderText("Wpisz wartość a")
        self.b.setPlaceholderText("Wpisz wartość b")
        self.a.setValidator(validator)
        self.b.setValidator(validator)
        self.rownanie.setPlaceholderText("Wpisz wartość całki")
        self.n.setPlaceholderText("Wpisz ilość punktów")
        l3.setAlignment(Qt.AlignCenter)
        self.wartosc.setAlignment(Qt.AlignCenter)

        self.combo.addItem("Wybierz", "none")
        self.combo.addItem("Metoda prostokątów", "window1")
        self.combo.addItem("Metoda trapezów", "window2")
        self.combo.addItem("Metoda Simpsona", "window3")
        self.combo.addItem("Reguła 3/8", "window4")
        self.combo.addItem("Metoda Boole'a", "window5")
        self.combo.addItem("Kwadratura Gaussa-Czebyszewa", "window6")
        self.combo.addItem("Kwadratura Gaussa-Hermite'a", "window7")
        self.combo.addItem("Metoda Monte Carlo 1D", "window8")
        self.combo.addItem("Całki nieoznaczone", "window9")

        self.combo.activated.connect(self.porownaj)
        layout.addWidget(l1, 1, 0)
        layout.addWidget(self.combo, 1, 1)

        layout.addWidget(l2, 2, 0)
        layout.addWidget(self.rownanie, 2, 1)
        layout.addWidget(instrukcja, 3, 0, 1, 2)
        instrukcja.clicked.connect(self.open_inst)
        layout.addWidget(l3, 4, 0, 1, 2)

        abHorizontal.addWidget(la)
        abHorizontal.addWidget(self.a)

        abHorizontal.addWidget(lb)
        abHorizontal.addWidget(self.b)

        layout.addLayout(abHorizontal, 5, 0, 1, 2)

        sliderLayout.addWidget(self.wartosc)
        sliderLayout.addWidget(self.n)
        layout.addLayout(sliderLayout, 6, 0, 1, 2)

        layout.addWidget(oblicz, 7, 0, 1, 2)
        oblicz.clicked.connect(self.check_errors)

        layout.addWidget(self.l6, 9, 0, 1, 2)
        layout.addWidget(self.l6l, 10, 0, 1, 2)
        layout.addWidget(self.l7, 11, 0, 1, 2)

        self.tabTimeErrors = QTabWidget(self)

        self.tabt = QWidget()
        self.tabt.layout = QVBoxLayout(self.tabt)
        self.tabt.layout.addWidget(self.l8)
        self.tabt.layout.addWidget(self.l8l)

        self.tabe = QWidget()
        self.tabe.layout = QVBoxLayout(self.tabe)
        self.tabe.layout.addWidget(self.l9)
        self.tabe.layout.addWidget(self.l9l)

        self.tabTimeErrors.addTab(self.tabt, "Czas")
        self.tabTimeErrors.addTab(self.tabe, "Błędy")

        layout.addWidget(self.tabTimeErrors, 13, 0, 4, 2)

        # canvas tab
        self.tabWidget = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab1.layout = QVBoxLayout(self.tab1)
        self.tab1.layout.addWidget(self.canvas2)
        self.tab1.layout.addWidget(self.toolbar)

        self.tab2 = QWidget()
        self.tab2.layout = QVBoxLayout(self.tab2)
        self.tab2.layout.addWidget(self.canvas)
        self.tab2.layout.addWidget(self.toolbar2)

        self.tabWidget.addTab(self.tab1, "Hit or miss")
        self.tabWidget.addTab(self.tab2, "Średniej wartości")
        layout.addWidget(self.tabWidget, 0, 3, 18, 1)

        zamknij = QPushButton('Zamknij program')
        zamknij_okno = QPushButton("Zamknij okno")
        powrot = QPushButton("Powrót")

        zamknij_okno.clicked.connect(self.close)
        zamknij.clicked.connect(QCoreApplication.instance().quit)
        powrot.clicked.connect(self.wroc)

        powrot.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        zamknij.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")
        zamknij_okno.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")

        layout_for_buttons.addWidget(powrot)
        layout_for_buttons.addWidget(zamknij)
        layout_for_buttons.addWidget(zamknij_okno)

        layout.addLayout(layout_for_buttons, 18, 0, 1, 2)

        self.setLayout(layout)
        self.setFontForLayout(layout, self.font)
        self.setFontForLayout(sliderLayout, self.font)
        self.setFontForLayout(abHorizontal, self.font)
        self.setFontForLayout(layout_for_buttons, self.font)
        self.setWindowTitle('Obliczenia metoda Monte Carlo 2D')

    def wroc(self):
        self.w = metoda_monte.MetodaMonte()
        self.w.show()
        self.close()

    def open_inst(self):
        self.wi = instrukcja.Instrukcja()
        self.wi.show()

    def porownaj(self, index):
        if self.combo.itemData(index) == "window1":
            self.window = oblicz_metoda_prostokatow.Oblicz()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window2":
            self.window = oblicz_trapez.ObliczTrapezy()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window3":
            self.window = oblicz_simpson.ObliczSimpson()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window4":
            self.window = oblicz_regula_3_8.ObliczRegula()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window5":
            self.window = oblicz_boole.ObliczBoole()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window6":
            self.window = obliczenia_czeb.ObliczCzeb()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window7":
            self.window = oblicz_herm.ObliczHerm()
            self.pass_data_n(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window8":
            self.window = oblicz_monte.ObliczMonte()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window9":
            self.window = oblicz_nieoznaczone.ObliczNieoznaczona()
            self.pass_data_n(self.window)
            self.window.show()

    def pass_data(self, window):
        try:
            a = self.a.text()
            b = self.b.text()
            rownanie = self.rownanie.text()

            window.a.setText(a)
            window.b.setText(b)
            window.rownanie.setText(rownanie)
            window.check_errors()
        except Exception as e:
            return

    def pass_data_n(self, window):
        try:
            rownanie = self.rownanie.text()
            window.rownanie.setText(rownanie)
            window.check_errors()
        except Exception as e:
            return

    def setFontForLayout(self, layout, font):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setFont(font)

    def check_errors(self):
        try:
            self.fxy(1, 1)
            self.l7.setText("")
        except Exception as e:
            self.l6.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.1")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return
        try:
            self.get_a_b()
        except Exception as e:
            self.l6.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.2")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return

    def symbols(self, rownanie):
        rownanie_matematyczne = sympify(rownanie)
        x_sym = rownanie_matematyczne.free_symbols
        x_sym_sorted = sorted(x_sym, key=lambda s: s.name)
        return x_sym_sorted

    def converter(self):
        try:
            rownanie_string = self.rownanie.text()
            rownanie_matematyczne = sympify(rownanie_string)
            x_sym_sorted = self.symbols(rownanie_string)
            if len(x_sym_sorted) != 2:
                self.l6.setText("Error: Funkcja powinna zawierać tylko jedną zmienną.")
                self.l6l.setText(f"")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l9.setText(f"")
                self.l8l.setText(f"")
                return None
            return rownanie_matematyczne, x_sym_sorted

        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji. 1")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return e

    def fxy(self, x, y):
        rownanie_string = self.rownanie.text()
        try:
            rownanie_matematyczne = sympify(rownanie_string)
            x_sym = rownanie_matematyczne.free_symbols
            x_sym_sorted = sorted(x_sym, key=lambda s: s.name)
            if len(x_sym_sorted) != 2:
                self.l6.setText("Error: Funkcja powinna zawierać dwie zmienne.")
                self.l6l.setText(f"")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l9.setText(f"")
                self.l8l.setText(f"")
                return None
        except Exception as e:
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")

            return None
        try:
            funkcja = lambdify(x_sym_sorted, rownanie_matematyczne, 'numpy')
            return funkcja(x, y)
        except ValueError:
            self.l6.setText("Error: Wartość nieprawidłowa.")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return
        except Exception as e:
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.4")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")

            return

    def dzielenie_przez_zero(self, funkcja, x):
        denominator = funkcja.as_numer_denom()[1]
        punkty = solve(denominator, x)
        if punkty:
            self.l7.setText(f"Error: W zakresie [a,b] nie mogą znajdować sie te punkty: {punkty}")
            return punkty

    def min_max(self, a, b):
        min_z = float('inf')
        max_z = float('-inf')
        for x in np.arange(a, b, 0.1):
            for y in np.arange(a, b, 0.1):
                z = self.fxy(x, y)
                if z < min_z:
                    min_z = z
                if z > max_z:
                    max_z = z
        return max_z, min_z

    def punkty(self, n, a, b):
        random_points_x = np.round(np.random.uniform(a, b, n), 1)
        random_points_y = np.round(np.random.uniform(a, b, n), 1)
        random_points_z = np.round(np.random.uniform(self.minimum, self.maximum, n), 1)

        return random_points_x, random_points_y, random_points_z

    def monte_carlo_3(self, a, b, ar_x, ar_y):
        try:

            f = self.fxy(ar_x, ar_y)
            start_time = timeit.default_timer()

            pole = (b - a) * (b - a)
            wynik = pole * np.mean(f)

            end_time = timeit.default_timer()
            time = end_time - start_time

            if math.isnan(wynik):
                self.l6.setText("Error: Podana została zła funkcja lub jej przedziały.")
                self.l6l.setText(f"")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l9.setText(f"")
                self.l8l.setText(f"")
                return None
            else:
                self.l6l.setText(f"Wynik dla wartości średniej: {wynik}")
                self.l8l.setText(f"Czas potrzebny do w.ś: {time}")
                return wynik
        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji.2")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return e

    def monte_carlo_4(self, a, b, n):
        try:
            num_on, num_above = self.ilosc_punktow()
            start_time = timeit.default_timer()
            h = self.maximum - self.minimum
            pole = h * (b - a) ** 2

            wynik = (num_on / n) * pole

            end_time = timeit.default_timer()
            time = end_time - start_time

            if math.isnan(wynik):
                self.l6.setText("Error: Podana została zła funkcja lub jej przedziały.")
                self.l6l.setText(f"")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l9.setText(f"")
                self.l8l.setText(f"")
                return None
            else:
                self.l6.setText(f"Wynik dla hit or miss: {wynik}")
                self.l8.setText(f"Czas potrzebny do obliczenia h.o.m.: {time}")
                return wynik
        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji.2")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return e

    def error(self, a, b, value, value2):
        try:
            accurate_result, _ = nquad(self.fxy, [(a, b), (a, b)])

            error = abs(accurate_result - value)
            error2 = abs(accurate_result - value2)

            self.l9.setText(f"Błąd dla Metody Monte Carlo 2D h.o.m.:  +-{error2}")
            self.l9l.setText(f"Błąd dla Metody Monte Carlo 2D w.ś.:  +-{error}")
        except Exception as e:
            self.l9.setText(f"Error: Problem z obliczeniem błędu.")
            self.l9l.setText(f"")
            return e

    def get_a_b(self):
        if self.rownanie.text().strip() == "":
            self.l6.setText("Error: Wpisz równanie")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return
        if self.a.text().strip() == "":
            self.l6.setText("Error: a nie może być puste")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return
        if self.b.text().strip() == "":
            self.l6.setText("Error: b nie może być puste")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return
        if self.n.text().strip() == "":
            self.l6.setText("Error: Wpisz wartość n")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return
        try:
            a = float(self.a.text())
            b = float(self.b.text())
            n = int(self.n.text())
        except ValueError:
            self.l6.setText("Error: Nieprawidłowe dane wejściowe dla a, b lub n")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return
        try:
            self.maximum, self.minimum = self.min_max(a, b)
            self.ar_x, self.ar_y, self.ar_z = self.punkty(n, a, b)
        except Exception as e:
            self.l6.setText("Error: Nieprawidłowe dane wejściowe.")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return
        if a >= b:
            self.l6.setText("Error: a powinno być mniejsze niż b.")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")
            return

        rownanie_matematyczne, x_sym_sorted = self.converter()
        zera = self.dzielenie_przez_zero(rownanie_matematyczne, x_sym_sorted)

        if zera:
            for i in zera:
                if i == a or i == b or a <= i <= b:
                    self.l6.setText("Error: Nieprawidłowe dane wejściowe dla a lub b. 1")
                    self.l6l.setText(f"")
                    self.l8.setText(f"")
                    self.l8l.setText(f"")
                    self.l9.setText(f"")
                    self.l8l.setText(f"")
                    return

        try:

            result_monte3 = self.monte_carlo_3(a, b, self.ar_x, self.ar_y)
            if result_monte3 is None:
                self.l6.setText("Error: Problem z obliczeniem wartości.")
                return
            result_monte4 = self.monte_carlo_4(a, b, n)
            if result_monte4 is None:
                self.l6.setText("Error: Problem z obliczeniem wartości.")
                return

        except Exception as e:
            self.l6.setText(f"Error: Wystąpił problem podczas obliczeń.")
            return
        try:
            self.error(a, b, result_monte3, result_monte4)
        except Exception as e:
            self.l6.setText(f"Error: Błąd z errorem")
            self.l6l.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l9.setText(f"")
            self.l8l.setText(f"")

            return e
        try:
            self.update_wykres3(a, b, self.ar_x, self.ar_y)
            self.update_wykres4(a, b, self.ar_x, self.ar_y, self.ar_z)
        except Exception as e:
            return None

    def ilosc_punktow(self):
        f_values = np.array([self.fxy(x, y) for x, y in zip(self.ar_x, self.ar_y)])
        threshold = 0.1
        points_on_curve = np.abs(f_values - self.ar_z) < threshold
        points_under_curve = self.ar_z < f_values
        points_above_curve = self.ar_z > f_values
        num_on = np.sum(points_on_curve) + np.sum(points_under_curve)
        num_above = np.sum(points_above_curve)
        return num_on, num_above

    def update_wykres3(self, a, b, ar_x, ar_y):
        if a is None or b is None or a >= b:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')

        f_values = self.fxy(ar_x, ar_y)
        x = np.linspace(a, b, 100)
        y = np.linspace(a, b, 100)
        x, y = np.meshgrid(x, y)
        z = self.fxy(x, y)

        ax.scatter(ar_x, ar_y, f_values, color='red', marker=".", label="Punkty Monte Carlo")

        surf = ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5, linewidth=0, antialiased=False,
                               label=self.rownanie.text())

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('f(x, y)')

        surf._facecolors2d = surf._facecolor3d
        surf._edgecolors2d = surf._edgecolor3d
        ax.legend(loc='upper left')

        ax.grid(True, alpha=0.2)
        self.canvas.draw()

    def update_wykres4(self, a, b, ar_x, ar_y, ar_z):
        if a is None or b is None or a >= b:
            return

        self.figure2.clear()
        ax = self.figure2.add_subplot(111, projection='3d')

        f_values = np.array([self.fxy(x, y) for x, y in zip(ar_x, ar_y)])
        threshold = 0.1
        points_on_curve = np.abs(f_values - ar_z) < threshold
        points_under_curve = ar_z < f_values
        points_above_curve = self.ar_z > f_values

        x = np.linspace(a, b, 100)
        y = np.linspace(a, b, 100)
        x, y = np.meshgrid(x, y)
        z = self.fxy(x, y)

        ax.scatter(ar_x[points_on_curve], ar_y[points_on_curve], ar_z[points_on_curve], color='green', marker=".",
                   label="Punkty w obszarze")
        ax.scatter(ar_x[points_under_curve], ar_y[points_under_curve], ar_z[points_under_curve], color='green',
                   marker=".")
        ax.scatter(ar_x[points_above_curve], ar_y[points_above_curve], ar_z[points_above_curve], color='red', marker=".",
                   label="Punkty poza obszarem")
        surf = ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5, linewidth=0, antialiased=False,
                               label=self.rownanie.text())

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('f(x, y)')

        surf._facecolors2d = surf._facecolor3d
        surf._edgecolors2d = surf._edgecolor3d
        ax.legend(loc='upper left')

        ax.grid(True, alpha=0.2)
        self.canvas2.draw()


def main():
    app = QApplication(sys.argv)
    ex = ObliczMonte2()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
