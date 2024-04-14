import sys
import numpy as np
import timeit
import math

from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from sympy import sympify, lambdify, solve
from PyQt5.QtCore import Qt, QCoreApplication, QLocale
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QComboBox, QLineEdit, QSlider, QHBoxLayout,
                             QPushButton, QDialog)
from PyQt5.QtGui import QDoubleValidator, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import PyQt5.QtGui as qtg
import instrukcja
from metody import regula_3_8
from obliczenia import (obliczenia_czeb, oblicz_herm, oblicz_monte, oblicz_monte2D, oblicz_boole,
                        oblicz_metoda_prostokatow, oblicz_nieoznaczone, oblicz_simpson, oblicz_trapez)


def symbols(rownanie):
    rownanie_matematyczne = sympify(rownanie)
    x_sym = rownanie_matematyczne.free_symbols
    x_sym_sorted = sorted(x_sym, key=lambda s: s.name)
    return x_sym_sorted


class ObliczRegula(QDialog):
    def __init__(self):
        super().__init__()
        self.window = None
        self.instrukcja = None
        self.wi = None
        self.w = None
        self.canvas = None
        self.figure = None
        self.wartosc = None
        self.b = None
        self.a = None
        self.rownanie = None
        self.combo = None
        self.font = None
        self.n = None
        self.l6 = None
        self.l7 = None
        self.l8 = None
        self.l9 = None
        self.slider = None
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
        l2 = QLabel("Wpisz równanie: ", self)
        l3 = QLabel("Podaj przedział [a,b]:", self)
        self.rownanie = QLineEdit(self)
        self.instrukcja = QPushButton('Instrukcja', self)
        la = QLabel("a: ", self)
        lb = QLabel("b:", self)
        self.a = QLineEdit(self)
        self.b = QLineEdit(self)
        self.n = 3
        self.l6 = QLabel(self)
        self.l7 = QLabel(self)
        self.l8 = QLabel(self)
        self.l9 = QLabel(self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(3)
        self.slider.setMaximum(50)
        self.slider.setValue(3)
        start = QLabel('3')
        end = QLabel('60')
        oblicz = QPushButton('Oblicz', self)
        self.wartosc = QLabel("Ilość n: 3", self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.slider.valueChanged.connect(self.slider_nodes)
        self.instrukcja.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        oblicz.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        self.slider.setStyleSheet("""
                QSlider::handle:horizontal {
                    background: #333;
                    border: 1px solid #555;
                    width: 8px;
                    height: 8px;
                    margin: -8px 0;  
                    border-radius:4px;  
                }
                """)
        self.l7.setStyleSheet('color: red')
        validator = QDoubleValidator()
        validator.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.a.setPlaceholderText("Wpisz wartość a")
        self.b.setPlaceholderText("Wpisz wartość b")
        self.a.setValidator(validator)
        self.b.setValidator(validator)
        self.rownanie.setPlaceholderText("Wpisz wartość całki")
        l3.setAlignment(Qt.AlignCenter)
        self.wartosc.setAlignment(Qt.AlignCenter)

        self.combo.addItem("Wybierz", "none")
        self.combo.addItem("Metoda prostokątów", "window1")
        self.combo.addItem("Metoda trapezów", "window2")
        self.combo.addItem("Metoda Simpsona", "window3")
        self.combo.addItem("Metoda Boole'a", "window4")
        self.combo.addItem("Kwadratura Gaussa-Czebyszewa", "window5")
        self.combo.addItem("Kwadratura Gaussa-Hermite'a", "window6")
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

        abHorizontal.addWidget(la)
        abHorizontal.addWidget(self.a)

        abHorizontal.addWidget(lb)
        abHorizontal.addWidget(self.b)

        layout.addLayout(abHorizontal, 5, 0, 1, 2)

        layout.addWidget(oblicz, 6, 0, 1, 2)
        oblicz.clicked.connect(self.check_errors)

        layout.addWidget(self.wartosc, 7, 0, 1, 2)

        sliderLayout.addWidget(start)
        sliderLayout.addWidget(self.slider)
        sliderLayout.addWidget(end)

        sliderLayout.setStretch(0, 1)
        sliderLayout.setStretch(1, 50)
        sliderLayout.setStretch(2, 1)

        layout.addLayout(sliderLayout, 8, 0, 1, 2)

        layout.addWidget(self.l6, 9, 0, 1, 2)
        layout.addWidget(self.l7, 10, 0, 1, 2)
        layout.addWidget(self.l8, 11, 0, 1, 2)
        layout.addWidget(self.l9, 12, 0, 1, 2)

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
        self.setFontForLayout(layout, self.font)
        self.setWindowTitle('Obliczenia reguła 3/8')

    def wroc(self):
        self.w = regula_3_8.Regula38()
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
            self.window = oblicz_boole.ObliczBoole()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window5":
            self.window = obliczenia_czeb.ObliczCzeb()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window6":
            self.window = oblicz_herm.ObliczHerm()
            self.pass_data_n(self.window)
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

    def setFontForLayout(self, layout, font):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setFont(font)

    def check_errors(self):
        try:
            self.f(1)
            self.l7.setText("")
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
            return e

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
            self.l7.setText(f"Error: W zakresie [a,b] nie mogą znajdować sie te punkty: {punkty}")
            return punkty

    def regula_3_8(self, n, a, b):
        try:

            if n % 3 == 1:
                self.l8.setText(f"")
                raise ValueError(self.l6.setText("Reguła 3/8 przyjmuje tylko liczbę przedziałów podzielną przez 3."))
            start_time = timeit.default_timer()

            h = (b - a) / n
            wynik = self.f(a) + self.f(b) + 3 * sum(self.f(a + i * h) for i in range(1, n, 3)) + 3 * sum(
                self.f(a + i * h) for i in range(2, n, 3)) + 2 * sum(self.f(a + i * h) for i in range(3, n - 1, 3))

            wynik *= 3 * h / 8

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

    def slider_nodes(self, value):
        if value % 3 == 0:
            self.n = value
        else:
            self.n = value + (3 - value % 3)
        self.wartosc.setText(f"Ilość n: {self.n}")
        self.get_a_b()

    def error(self, a, b, value):
        try:
            accurate_result, _ = quad(self.f, a, b)

            error = abs(accurate_result - value)
            self.l9.setText(f"Błąd dla reguły 3/8:  +-{error}")

        except Exception as e:
            self.l9.setText(f"Error: Problem z obliczeniem błędu.")
            return e

    def get_a_b(self):
        if self.rownanie.text().strip() == "":
            self.l6.setText("Error: Wpisz równanie")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return
        if self.a.text().strip() == "":
            self.l6.setText("Error: a nie może być puste")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return
        if self.b.text().strip() == "":
            self.l6.setText("Error: b nie może być puste")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return
        try:
            a = float(self.a.text())
            b = float(self.b.text())
        except ValueError:
            self.l6.setText("Error: Nieprawidłowe dane wejściowe dla a lub b.")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return
        if a >= b:
            self.l6.setText("Error: a powinno być mniejsze niż b.")
            self.l8.setText(f"")
            self.l9.setText(f"")
            return

        rownanie_matematyczne, x_sym_sorted = self.converter()
        zera = self.dzielenie_przez_zero(rownanie_matematyczne, x_sym_sorted)

        if zera:
            for i in zera:
                if i == a or i == b or a <= i <= b:
                    self.l6.setText("Error: Nieprawidłowe dane wejściowe dla a lub b.")
                    self.l8.setText(f"")
                    self.l9.setText(f"")
                    return

        try:

            result_regula = self.regula_3_8(self.n, a, b)

            if result_regula is None:
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
            self.error(a, b, result_regula)
        except Exception as e:
            self.l6.setText(f"Error: Błąd z errorem")
            self.l8.setText(f"")
            self.l9.setText(f"")

            return e

        self.update_wykres(a, b)

    def update_wykres(self, a, b):
        if a is None or b is None or a >= b:
            return

        if (self.n - 1) % 3 != 0:
            self.n += 3 - ((self.n - 1) % 3)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        x_points = np.linspace(a, b, self.n)
        y_points = [self.f(x) for x in x_points]
        ax.scatter(x_points, y_points, color='red', marker=".")
        ax.grid(True, alpha=0.2)

        for i in range(0, self.n - 1, 3):
            if i + 3 < self.n:
                x_sub = x_points[i:i + 4]
                y_sub = y_points[i:i + 4]

                cs = CubicSpline(x_sub, y_sub)
                x_sub_fine = np.linspace(x_sub[0], x_sub[-1], 100)
                ax.plot(x_sub_fine, cs(x_sub_fine), 'r-', alpha=0.5,
                        label='Reguła 3/8' if i == 0 else "")
                ax.fill_between(x_sub_fine, cs(x_sub_fine), color='orange', alpha=0.3)

        x_fine = np.linspace(a, b, 300)
        y_fine = [self.f(x) for x in x_fine]
        ax.plot(x_fine, y_fine, 'b-', linewidth=1, label=self.rownanie.text())
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend(loc='upper left')

        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    ex = ObliczRegula()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
