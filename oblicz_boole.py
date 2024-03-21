import sys
import numpy as np
import timeit
import math

from scipy.integrate import quad
from sympy import sympify, lambdify, solve
from PyQt5.QtCore import Qt, QCoreApplication, QLocale
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QComboBox, QLineEdit, QSlider, QHBoxLayout,
                             QPushButton, QDialog)
from PyQt5.QtGui import QDoubleValidator, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy.core.sympify import SympifyError

import instrukcja
import metoda_tr
import oblicz_metoda_prostokatow
import oblicz_nieoznaczone
import oblicz_regula_3_8
import oblicz_simpson
import oblicz_trapez


class ObliczBoole(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # self.setStyleSheet("background-color: white;")
        self.font = QFont()
        self.font.setPointSize(10)

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
        self.n = 4
        self.l6 = QLabel(self)
        self.l6p = QLabel(self)
        self.l7 = QLabel(self)
        self.l8 = QLabel(self)
        self.l8p = QLabel(self)
        self.l9 = QLabel(self)
        self.l9p = QLabel(self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(4)
        self.slider.setMaximum(80)
        self.slider.setValue(4)
        start = QLabel('4')
        end = QLabel('80')
        oblicz = QPushButton('Oblicz', self)
        self.wartosc = QLabel("Liczba node'ów: 4", self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.slider.valueChanged.connect(self.slider_nodes)
        instrukcja.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
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
        self.combo.addItem("Reguła 3/8", "window4")
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
        layout.addWidget(self.l6p, 10, 0, 1, 2)
        layout.addWidget(self.l7, 11, 0, 1, 2)
        layout.addWidget(self.l8, 12, 0, 1, 2)
        layout.addWidget(self.l8p, 13, 0, 1, 2)
        layout.addWidget(self.l9, 14, 0, 1, 2)
        layout.addWidget(self.l9p, 15, 0, 1, 2)

        layout.addWidget(self.canvas, 0, 3, 18, 1)

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

        layout.addLayout(layout_for_buttons, 20, 0, 1, 2)

        self.setLayout(layout)
        self.setFontForLayout(layout_for_buttons, self.font)
        self.setFontForLayout(layout, self.font)
        self.setWindowTitle("Obliczenia metoda Boole'a")

    def wroc(self):
        self.w = metoda_tr.MetodaTr()
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
        elif self.combo.itemData(index) == "window9":
            self.window = oblicz_nieoznaczone.ObliczNieoznaczona()
            self.pass_data_n(self.window)
            self.window.show()

    def pass_data(self, window):
        try:
            a = self.a.text()
            b = self.b.text()
            rownanie = self.rownanie.text()

            self.window.a.setText(a)
            self.window.b.setText(b)
            self.window.rownanie.setText(rownanie)
            self.window.check_errors()
        except Exception as e:
            return

    def pass_data_n(self, window):
        try:
            rownanie = self.rownanie.text()
            self.window.rownanie.setText(rownanie)
            self.window.check_errors()
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
        except Exception as e:
            self.l6.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.1")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")
            return
        try:
            self.get_a_b()
        except Exception as e:
            self.l6.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.2")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")
            return

    def f(self, x):
        rownanie_string = self.rownanie.text()
        try:
            rownanie_matematyczne = sympify(rownanie_string)
            x_sym = rownanie_matematyczne.free_symbols
            x_sym_sorted = sorted(x_sym, key=lambda s: s.name)
            if len(x_sym_sorted) != 1:
                self.l6.setText("Error: Funkcja powinna zawierać tylko jedną zmienną.")
                self.l6p.setText(f"")
                self.l8.setText(f"")
                self.l8p.setText(f"")
                self.l9.setText(f"")
                self.l9p.setText(f"")

                return None
        except Exception as e:
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.3")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")

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
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.4")
            self.l8.setText(f"")
            self.l9.setText(f"")

            return

    def dzielenie_przez_zero(self, funkcja, x):
        denominator = funkcja.as_numer_denom()[1]
        punkty = solve(denominator, x)
        if punkty:
            self.l7.setText(f"Error: W zakresie [a,b] nie mogą znajdować sie te punkty: {punkty}")
            return punkty


    def metoda_zlozona_boole(self, n, a, b):
        try:
            if n % 4 != 0:
                raise ValueError("Liczba podprzedziałów (n) musi być podzielna przez.")

            h = (b - a) / n
            wynik = 0
            for i in range(0, n, 4):
                x0 = a + i * h
                x1 = x0 + h
                x2 = x1 + h
                x3 = x2 + h
                x4 = x3 + h

                wynik += (2 * h / 45) * (
                        7 * self.f(x0) + 32 * self.f(x1) + 12 * self.f(x2) + 32 * self.f(x3) + 7 * self.f(x4))

            if math.isnan(wynik):
                self.l6.setText("Error: Podana została zła funkcja lub jej przedziały.")
                self.l6p.setText(f"")
                self.l8.setText(f"")
                self.l8p.setText(f"")
                self.l9.setText(f"")
                self.l9p.setText(f"")
                return None
            else:
                self.l6.setText(f"Wynik dla złożonej metody: {wynik}")
                return wynik

        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji.9")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")
            return e

    def metoda_prosta_boole(self, a, b):
        try:
            h = (b - a) / 4
            wynik = 0
            x0 = a
            x1 = a + h
            x2 = a + 2 * h
            x3 = a + 3 * h
            x4 = b

            wynik += (2 * h / 45) * (
                    7 * self.f(x0) + 32 * self.f(x1) + 12 * self.f(x2) + 32 * self.f(x3) + 7 * self.f(x4))

            if math.isnan(wynik):
                self.l6.setText("Error: Podana została zła funkcja lub jej przedziały.")
                self.l6p.setText(f"")
                self.l8.setText(f"")
                self.l8p.setText(f"")
                self.l9.setText(f"")
                self.l9p.setText(f"")
                return None
            else:
                self.l6p.setText(f"Wynik dla prostej metody: {wynik}")
                return wynik

        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji. 0")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")
            return e

    def slider_nodes(self, value):
        if value % 4 == 0:
            self.n = value
        else:
            self.n = value + (4 - value % 4)
        self.wartosc.setText(f"Liczba node'ów: {self.n}")
        self.get_a_b()

    def error(self, a, b, zl, pr):
        try:
            accurate_result, _ = quad(self.f, a, b)

            error_z = abs(accurate_result - zl)
            error_p = abs(accurate_result - pr)
            self.l9.setText(f"Błąd dla metody Boole'a złożonej: {error_z}")
            self.l9p.setText(f"Błąd dla metody Boole'a prostej: {error_p}")
        except Exception as e:
            self.l9.setText(f"Error: Problem z obliczeniem błędu.")
            return e

    def get_a_b(self):
        if self.rownanie.text().strip() == "":
            self.l6.setText("Error: Wpisz równanie")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")
            return
        if self.a.text().strip() == "":
            self.l6.setText("Error: a nie może być puste")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")
            return
        if self.b.text().strip() == "":
            self.l6.setText("Error: b nie może być puste")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")
            return
        try:
            a = float(self.a.text())
            b = float(self.b.text())
        except ValueError:
            self.l6.setText("Error: Nieprawidłowe dane wejściowe dla a lub b.")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")
            return
        if a >= b:
            self.l6.setText("Error: a powinno być mniejsze niż b.")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")
            return

        rownanie_string = self.rownanie.text()
        try:
            rownanie_matematyczne = sympify(rownanie_string)
            x_sym = rownanie_matematyczne.free_symbols
            if not x_sym:
                self.l6.setText("Error: Brak zmiennej w równaniu.")
                return
            x_sym_sorted = sorted(x_sym, key=lambda s: s.name)
        except SympifyError:
            self.l6.setText("Error: Nie można przekształcić wprowadzonego równania.")
            return
        zera = self.dzielenie_przez_zero(rownanie_matematyczne, x_sym_sorted)

        if zera:
            for i in zera:
                if i == a or i == b or a <= i <= b:
                    self.l6.setText("Error: Nieprawidłowe dane wejściowe dla a lub b. 1")
                    return

        try:
            start_time = timeit.default_timer()
            result_zlozona = self.metoda_zlozona_boole(self.n, a, b)
            end_time = timeit.default_timer()
            if result_zlozona is None:
                self.l6.setText("Error: Problem z obliczeniem wartości.")
                return
            time = end_time - start_time
            self.l8.setText(f"Czas potrzebny do obliczenia złożona: {time}")

            start_timep = timeit.default_timer()
            result_prosta = self.metoda_prosta_boole(a, b)
            end_timep = timeit.default_timer()
            if result_prosta is None:
                self.l6.setText("Error: Problem z obliczeniem wartości.")
                return
            timep = end_timep - start_timep
            self.l8p.setText(f"Czas potrzebny do obliczenia prosta: {timep}")

        except Exception as e:
            self.l6.setText(f"Error: Wystąpił problem podczas obliczeń.")
            return
        try:
            self.error(a, b, result_zlozona, result_prosta)
        except Exception as e:
            self.l6.setText(f"Error: Błąd z errorem")
            self.l6p.setText(f"")
            self.l8.setText(f"")
            self.l8p.setText(f"")
            self.l9.setText(f"")
            self.l9p.setText(f"")

            return e
        self.update_wykres(a, b)

    def update_wykres(self, a, b):
        if a is None or b is None or a >= b:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if self.n % 4 != 0:
            self.n += 4 - self.n % 4

        x_points = np.linspace(a, b, self.n + 1)
        y_points = self.f(x_points)

        x_fine = np.linspace(a, b, 300)
        y_fine = self.f(x_fine)
        ax.plot(x_fine, y_fine, 'b-', linewidth=1)
        h = (b - a) / 4
        x0 = a
        x1 = a + h
        x2 = a + 2 * h
        x3 = a + 3 * h
        x4 = b
        punkty = x0, x1, x2, x3, x4
        for punkt in punkty:
            ax.scatter(punkt, self.f(punkt), color='purple', s=50)

        for i in range(0, self.n, 4):
            xs = x_points[i:i + 5]
            ys = y_points[i:i + 5]
            ax.fill_between(xs, 0, ys, color='red', alpha=0.3, step='pre', linewidth=0.5, edgecolor='r')
            ax.scatter(xs, ys, color='red', marker=".")

        ax.grid(True, alpha=0.2)
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    ex = ObliczBoole()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
