import sys
import numpy as np
import timeit
import math
import PyQt5.QtGui as qtg
from numpy.polynomial.hermite import hermgauss
from scipy.integrate import quad
from sympy import sympify, lambdify, solve
from PyQt5.QtCore import Qt, QCoreApplication, QLocale
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QComboBox, QLineEdit, QHBoxLayout,
                             QPushButton, QDialog)
from PyQt5.QtGui import QDoubleValidator, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import instrukcja
from metody import metoda_herm
from obliczenia import (oblicz_boole, obliczenia_czeb, oblicz_monte, oblicz_monte2D, oblicz_regula_3_8,
                        oblicz_metoda_prostokatow, oblicz_nieoznaczone, oblicz_simpson, oblicz_trapez)


def setFontForLayout(layout, font):
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.setFont(font)


def symbols(rownanie):
    rownanie_matematyczne = sympify(rownanie)
    x_sym = rownanie_matematyczne.free_symbols
    x_sym_sorted = sorted(x_sym, key=lambda s: s.name)
    return x_sym_sorted


class ObliczHerm(QDialog):
    def __init__(self):
        super().__init__()
        self.window = None
        self.w = None
        self.instrukcja = None
        self.figure = None
        self.canvas = None
        self.wartosc = None
        self.rownanie = None
        self.font = None
        self.wi = None
        self.combo = None
        self.n = None
        self.l6 = None
        self.l7 = None
        self.l8 = None
        self.l9 = None
        self.initUI()

    def initUI(self):
        self.setWindowIcon(qtg.QIcon('zdjecia/icon.png'))

        # self.setStyleSheet("background-color: white;")
        self.font = QFont()
        self.font.setPointSize(9)

        layout = QGridLayout()
        abHorizontal = QHBoxLayout()
        layout_for_buttons = QHBoxLayout()

        self.combo = QComboBox(self)
        l1 = QLabel("Porównaj z: ", self)

        l2 = QLabel("Wpisz równanie: ", self)
        l3 = QLabel("Przedział [a,b] to [-∞,∞]", self)
        self.rownanie = QLineEdit(self)
        self.instrukcja = QPushButton('Instrukcja', self)
        self.n = QLineEdit(self)
        self.l6 = QLabel(self)
        self.l7 = QLabel(self)
        self.l8 = QLabel(self)
        self.l9 = QLabel(self)
        oblicz = QPushButton('Oblicz', self)
        self.wartosc = QLabel("Ilość n: ", self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.instrukcja.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        oblicz.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        self.l7.setStyleSheet('color: red')

        validator = QDoubleValidator()
        validator.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

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
        self.combo.addItem("Metoda Monte Carlo 1D", "window7")
        self.combo.addItem("Metoda Monte Carlo 2D", "window8")
        self.combo.addItem("Całki nieoznaczone", "window9")

        self.combo.activated.connect(self.porownaj)
        layout.addWidget(l1, 1, 0)
        layout.addWidget(self.combo, 1, 1)

        layout.addWidget(l2, 2, 0)
        layout.addWidget(self.rownanie, 2, 1)
        layout.addWidget(self.instrukcja, 3, 0, 1, 2)
        self.instrukcja.clicked.connect(self.open_inst)
        layout.addWidget(l3, 4, 0, 1, 2)

        layout.addWidget(oblicz, 6, 0, 1, 2)
        oblicz.clicked.connect(self.check_errors)

        abHorizontal.addWidget(self.wartosc)
        abHorizontal.addWidget(self.n)
        layout.addLayout(abHorizontal, 5, 0, 1, 2)

        layout.addWidget(self.l6, 7, 0, 1, 2)
        layout.addWidget(self.l7, 8, 0, 1, 2)
        layout.addWidget(self.l8, 9, 0, 1, 2)
        layout.addWidget(self.l9, 10, 0, 1, 2)

        layout.addWidget(self.canvas, 0, 3, 15, 1)

        zamknij = QPushButton('Zamknij program')
        zamknij_okno = QPushButton("Zamknij okno")
        powrot = QPushButton("Powrót")

        zamknij_okno.clicked.connect(self.close)
        zamknij.clicked.connect(QCoreApplication.instance().quit)
        powrot.clicked.connect(self.wroc)

        powrot.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        zamknij.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")
        zamknij_okno.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")

        layout_for_buttons.addWidget(zamknij)
        layout_for_buttons.addWidget(zamknij_okno)
        layout_for_buttons.addWidget(powrot)

        layout.addLayout(layout_for_buttons, 18, 0, 1, 2)

        self.setLayout(layout)
        setFontForLayout(layout, self.font)
        self.setWindowTitle("Obliczenia kwadratura Gaussa-Hermite'a")

    def wroc(self):
        self.w = metoda_herm.MetodaHerm()
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
            self.window = oblicz_monte.ObliczMonte()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window8":
            self.window = oblicz_monte2D.ObliczMonte2()
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

    def check_errors(self):
        try:
            self.l7.setText("")
            self.f(1)
        except Exception as e:
            self.l6.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return
        try:
            self.get_a_b()
        except Exception as e:
            self.l6.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return

    def converter(self):
        try:
            rownanie_string = self.rownanie.text()
            rownanie_matematyczne = sympify(rownanie_string)
            x_sym_sorted = symbols(rownanie_string)
            if len(x_sym_sorted) != 1:
                self.l6.setText("Error: Funkcja powinna zawierać tylko jedną zmienną.")
                self.l8.setText(f"")
                self.l9.setText(f"")
                return None
            return rownanie_matematyczne, x_sym_sorted

        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji.")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return

    def f(self, x):
        try:
            rownanie_matematyczne, x_sym_sorted = self.converter()
        except Exception as e:
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.")
            self.l8.setText(f"")
            self.l9.setText(f"")

            return None
        try:
            funkcja = lambdify(x_sym_sorted, rownanie_matematyczne, 'numpy')
            return funkcja(x)
        except ValueError:
            self.l6.setText("Error: Wartość nieprawidłowa.")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return
        except Exception as e:
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.")
            self.l8.setText(f"")
            self.l9.setText(f"")

            return

    def dzielenie_przez_zero(self, funkcja, x):
        denominator = funkcja.as_numer_denom()[1]
        punkty = solve(denominator, x)
        if punkty:
            self.l7.setText(f"Error: W zakresie nie mogą znajdować sie te punkty: {punkty}")
            return punkty

    def hermit(self, n):
        try:

            start_time = timeit.default_timer()

            x, w = np.polynomial.hermite.hermgauss(n)

            wynik = np.sum(w * self.f(x))

            end_time = timeit.default_timer()
            time = end_time - start_time

            if math.isnan(wynik):
                self.l6.setText("Error: Podana została zła funkcja lub jej przedziały.")
                self.l8.setText(f"")
                self.l9.setText(f"")
                return None
            else:
                self.l6.setText(f"Wynik: {wynik}")
                self.l8.setText(f"Czas potrzebny do obliczenia: {time}")
                return wynik

        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji.")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return e

    @staticmethod
    def do_errora(x):
        return np.exp(-x ** 2)

    def razem(self, x):
        return self.do_errora(x) * self.f(x)

    def error(self, value):
        try:
            accurate_result, _ = quad(self.razem, -np.inf, np.inf)

            error = abs(accurate_result - value)
            self.l9.setText(f"Błąd dla kwadratury Gaussa-Hermite'a:  +-{error}")

        except Exception as e:
            self.l9.setText(f"Error: Problem z obliczeniem błędu.")
            return e

    def get_a_b(self):
        if self.rownanie.text().strip() == "":
            self.l6.setText("Error: Wpisz równanie")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return
        if self.n.text().strip() == "":
            self.l6.setText("Error: Wpisz wartość n")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return
        try:
            n = int(self.n.text())
        except ValueError:
            self.l6.setText("Error: Nieprawidłowe dane wejściowe dla n.")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return

        rownanie_matematyczne, x_sym_sorted = self.converter()
        zera = self.dzielenie_przez_zero(rownanie_matematyczne, x_sym_sorted)

        if zera:
            self.l6.setText("Error: Funkcja nie jest ciągła.")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return
        try:

            result_herm = self.hermit(n)
            if result_herm is None:
                self.l6.setText("Error: Problem z obliczeniem wartości.")
                self.l8.setText(f"")
                self.l9.setText(f"")
                return
        except Exception as e:
            self.l6.setText(f"Error: Wystąpił problem podczas obliczeń.")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return
        try:
            self.error(result_herm)
        except Exception as e:
            self.l6.setText(f"Error: Błąd z errorem")
            self.l8.setText(f"")
            self.l9.setText(f"")

            return e
        self.update_wykres(n)

    def update_wykres(self, n):

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        nodes, weights = hermgauss(n)
        y_points = [self.f(x) * np.exp(-x ** 2) for x in nodes]
        x_fine = np.linspace(-4, 4, 3000)
        y_fine = [self.f(x) for x in x_fine]

        ax.scatter(nodes, y_points, color='red', marker=".", label="Węzły Gaussa-Hermite'a")
        ax.grid(True, alpha=0.2)

        ax.plot(x_fine, y_fine, 'b-', linewidth=1, label=self.rownanie.text())

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend(loc='upper left')

        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    ex = ObliczHerm()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
