import numpy as np
import timeit
import math
from scipy.integrate import quad
from sympy import sympify, lambdify, solve
from PyQt5.QtCore import Qt, QCoreApplication, QLocale
from PyQt5.QtWidgets import (QGridLayout, QLabel, QComboBox, QLineEdit, QSlider, QHBoxLayout,
                             QPushButton, QDialog, QTabWidget, QVBoxLayout, QWidget)
from PyQt5.QtGui import QDoubleValidator, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import PyQt5.QtGui as qtg
import instrukcja
from metody import metoda_pr
from obliczenia import (oblicz_boole, obliczenia_czeb, oblicz_herm, oblicz_simpson, oblicz_regula_3_8,
                        oblicz_nieoznaczone, oblicz_monte, oblicz_monte2D, oblicz_trapez)


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


class Oblicz(QDialog):
    def __init__(self):
        super().__init__()
        self.instrukcja = None
        self.window = None
        self.wi = None
        self.w = None
        self.tab3 = None
        self.tab2 = None
        self.tab1 = None
        self.tabWidget = None
        self.tabe = None
        self.tabt = None
        self.tabTimeErrors = None
        self.slider = None
        self.errory = None
        self.l9 = None
        self.l8r = None
        self.l8l = None
        self.l8 = None
        self.l6r = None
        self.l7 = None
        self.l6l = None
        self.l6 = None
        self.l9l = None
        self.l9r = None
        self.n = None
        self.b = None
        self.a = None
        self.wartosc = None
        self.figure1 = None
        self.canvas1 = None
        self.figure2 = None
        self.canvas2 = None
        self.figure3 = None
        self.canvas3 = None
        self.rownanie = None
        self.combo = None
        self.font = None
        self.initUI()

    def initUI(self):

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
        self.n = 1
        self.l6 = QLabel(self)
        self.l6l = QLabel(self)
        self.l6r = QLabel(self)
        self.l7 = QLabel(self)
        self.l8 = QLabel(self)
        self.l8l = QLabel(self)
        self.l8r = QLabel(self)
        self.l9 = QLabel(self)
        self.l9l = QLabel(self)
        self.l9r = QLabel(self)
        self.errory = QLabel(self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(1)
        start = QLabel('1')
        end = QLabel('50')
        oblicz = QPushButton('Oblicz', self)
        self.wartosc = QLabel("Ilość n: 1", self)
        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.figure3 = Figure()
        self.canvas3 = FigureCanvas(self.figure3)

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
        validator = QDoubleValidator()
        validator.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.a.setPlaceholderText("Wpisz wartość a")
        self.b.setPlaceholderText("Wpisz wartość b")
        self.a.setValidator(validator)
        self.b.setValidator(validator)
        self.rownanie.setPlaceholderText("Wpisz wartość całki")
        l3.setAlignment(Qt.AlignCenter)
        self.wartosc.setAlignment(Qt.AlignCenter)
        self.l7.setStyleSheet('color: red')

        self.combo.addItem("Wybierz", "none")
        self.combo.addItem("Metoda trapezów", "window1")
        self.combo.addItem("Metoda Simpsona", "window2")
        self.combo.addItem("Reguła 3/8", "window3")
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

        layout.addWidget(self.errory, 9, 0, 1, 2)
        layout.addWidget(self.l6, 10, 0, 1, 2)
        layout.addWidget(self.l6l, 11, 0, 1, 2)
        layout.addWidget(self.l6r, 12, 0, 1, 2)
        layout.addWidget(self.l7, 13, 0, 1, 2)

        # tab for errors and time

        self.tabTimeErrors = QTabWidget(self)

        self.tabt = QWidget()
        self.tabt.layout = QVBoxLayout(self.tabt)
        self.tabt.layout.addWidget(self.l8)
        self.tabt.layout.addWidget(self.l8l)
        self.tabt.layout.addWidget(self.l8r)

        self.tabe = QWidget()
        self.tabe.layout = QVBoxLayout(self.tabe)
        self.tabe.layout.addWidget(self.l9)
        self.tabe.layout.addWidget(self.l9l)
        self.tabe.layout.addWidget(self.l9r)

        self.tabTimeErrors.addTab(self.tabt, "Czas")
        self.tabTimeErrors.addTab(self.tabe, "Błędy")

        layout.addWidget(self.tabTimeErrors, 14, 0, 4, 2)

        # tab for canvas
        self.tabWidget = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab1.layout = QVBoxLayout(self.tab1)
        self.tab1.layout.addWidget(self.canvas1)

        self.tab2 = QWidget()
        self.tab2.layout = QVBoxLayout(self.tab2)
        self.tab2.layout.addWidget(self.canvas2)

        self.tab3 = QWidget()
        self.tab3.layout = QVBoxLayout(self.tab3)
        self.tab3.layout.addWidget(self.canvas3)

        self.tabWidget.addTab(self.tab1, "Midpoint")
        self.tabWidget.addTab(self.tab2, "Left side")
        self.tabWidget.addTab(self.tab3, "Right side")

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

        layout_for_buttons.addWidget(zamknij)
        layout_for_buttons.addWidget(zamknij_okno)
        layout_for_buttons.addWidget(powrot)

        layout.addLayout(layout_for_buttons, 25, 0, 1, 2)

        self.setLayout(layout)
        setFontForLayout(layout, self.font)
        self.setWindowTitle('Obliczenia metoda prostokątów')

    def wroc(self):
        self.w = metoda_pr.MetodaPr()
        self.w.show()
        self.close()

    def open_inst(self):
        self.wi = instrukcja.Instrukcja()
        self.wi.show()

    def porownaj(self, index):
        if self.combo.itemData(index) == "window1":
            self.window = oblicz_trapez.ObliczTrapezy()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window2":
            self.window = oblicz_simpson.ObliczSimpson()
            self.pass_data(self.window)
            self.window.show()
        elif self.combo.itemData(index) == "window3":
            self.window = oblicz_regula_3_8.ObliczRegula()
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

    def check_errors(self):
        try:
            self.errory.setText("")
            self.l7.setText("")
            self.f(1)
        except Exception as e:
            self.errory.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.")
            self.l6.setText(f"")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return
        try:
            self.get_a_b()
        except Exception as e:
            self.errory.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.2")
            self.l6.setText(f"")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return

    def converter(self):
        try:
            rownanie_string = self.rownanie.text()
            rownanie_matematyczne = sympify(rownanie_string)
            x_sym_sorted = symbols(rownanie_string)
            if len(x_sym_sorted) != 1:
                self.l6.setText("Error: Funkcja powinna zawierać tylko jedną zmienną.")
                self.l6.setText(f"")
                self.l6l.setText(f"")
                self.l6r.setText(f" ")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l8r.setText(f"")
                self.l9.setText(f"")
                self.l9l.setText(f"")
                self.l9r.setText(f"")
                return None
            return rownanie_matematyczne, x_sym_sorted

        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji. 1")
            self.l6.setText(f"")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return e

    def f(self, x):
        try:
            rownanie_matematyczne, x_sym_sorted = self.converter()
        except Exception as e:
            self.errory.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.3")
            self.l6.setText(f"")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")

            return None
        try:
            funkcja = lambdify(x_sym_sorted, rownanie_matematyczne, 'numpy')
            return funkcja(x)
        except ValueError:
            self.errory.setText("Error: Wartość nieprawidłowa.")
            self.l6.setText(f"")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return
        except Exception as e:
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.4")
            self.errory.setText("")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")

            return

    def dzielenie_przez_zero(self, funkcja, x):
        denominator = funkcja.as_numer_denom()[1]
        punkty = solve(denominator, x)
        if punkty:
            self.l7.setText(f"Error: W zakresie [a,b] nie mogą znajdować się te punkty: {punkty}")
            return punkty

    def metoda_prostokatow_midpoint(self, n, a, b):
        try:
            start_time = timeit.default_timer()

            h = (b - a) / n
            wynik = 0
            for i in range(n):
                xi = a + (i + 0.5) * h
                wynik += self.f(xi) * h

            end_time = timeit.default_timer()
            time = end_time - start_time

            if math.isnan(wynik):
                self.errory.setText("Error: Podana została zła funkcja lub jej przedziały.")
                self.l6.setText("")
                self.l6l.setText(f"")
                self.l6r.setText(f" ")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l8r.setText(f"")
                self.l9.setText(f"")
                self.l9l.setText(f"")
                self.l9r.setText(f"")
                return None
            else:
                self.l6.setText(f"Wynik dla midpoint: {wynik}")
                self.l8.setText(f"Czas potrzebny do obliczenia midpoint: {time}")
                return wynik

        except Exception as e:
            self.errory.setText("Error: Problem z obliczeniem wartości funkcji.")
            self.l6.setText(f"")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return e

    def metoda_prostokatow_leftside(self, n, a, b):
        try:
            start_time = timeit.default_timer()

            h = (b - a) / n
            wynik = 0
            for i in range(n):
                xi = a + i * h
                wynik += self.f(xi) * h

            end_time = timeit.default_timer()
            time = end_time - start_time

            if math.isnan(wynik):
                self.errory.setText("Error: Podana została zła funkcja lub jej przedziały.2")
                self.l6.setText("")
                self.l6l.setText(f"")
                self.l6r.setText(f" ")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l8r.setText(f"")
                self.l9.setText(f"")
                self.l9l.setText(f"")
                self.l9r.setText(f"")
                return None
            else:
                self.l6l.setText(f"Wynik da left side: {wynik}")
                self.l8l.setText(f"Czas potrzebny do obliczenia left side: {time}")
                return wynik

        except Exception as e:
            self.errory.setText(f"Error: Problem z obliczeniem wartości funkcji.")
            self.l6.setText(f".")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return e

    def metoda_prostokatow_rightside(self, n, a, b):
        try:
            start_time = timeit.default_timer()

            h = (b - a) / n
            wynik = 0
            for i in range(1, n + 1):
                xi = a + i * h
                wynik += self.f(xi) * h

            end_time = timeit.default_timer()
            time = end_time - start_time

            if math.isnan(wynik):
                self.errory.setText("Error: Podana została zła funkcja lub jej przedziały.3")
                self.l6.setText("")
                self.l6l.setText(f"")
                self.l6r.setText(f" ")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l8r.setText(f"")
                self.l9.setText(f"")
                self.l9l.setText(f"")
                self.l9r.setText(f"")
                return
            else:
                self.l6r.setText(f"Wynik rightside: {wynik}")
                self.l8r.setText(f"Czas potrzebny do obliczenia right side: {time}")
                return wynik
        except Exception as e:
            self.errory.setText(f"Error: Problem z obliczeniem wartości funkcji.")
            self.l6.setText(f"")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return e

    def error(self, a, b, ls, rs, mp):
        try:

            accurate_result, _ = quad(self.f, a, b)

            error_m = abs(accurate_result - mp)
            error_l = abs(accurate_result - ls)
            error_r = abs(accurate_result - rs)

            self.l9.setText(f"Błąd dla midpoint:  +-{error_m}")
            self.l9l.setText(f"Błąd dla left side:  +-{error_l}")
            self.l9r.setText(f"Błąd dla right side:  +-{error_r}")
        except Exception as e:
            self.l9.setText(f"Error: Problem z obliczeniem błędu.")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return e

    def slider_nodes(self, value):
        self.n = value
        self.wartosc.setText(f"Ilość n: {value}")
        self.get_a_b()

    def get_a_b(self):
        if self.rownanie.text().strip() == "":
            self.errory.setText("Error: Wpisz równanie")
            self.l6.setText("")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return
        if self.a.text().strip() == "":
            self.errory.setText("Error: a nie może być puste")
            self.l6.setText("")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return
        if self.b.text().strip() == "":
            self.errory.setText("Error: b nie może być puste")
            self.l6.setText("")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return
        try:
            a = float(self.a.text())
            b = float(self.b.text())
        except ValueError:
            self.errory.setText("Error: Nieprawidłowe dane wejściowe dla a lub b.")
            self.l6.setText("")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return
        if a >= b:
            self.errory.setText("Error: a powinno być mniejsze niż b.")
            self.l6.setText("")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return

        rownanie_matematyczne, x_sym_sorted = self.converter()
        zera = self.dzielenie_przez_zero(rownanie_matematyczne, x_sym_sorted)

        if zera:
            for i in zera:
                if i == a or i == b or a <= i <= b:
                    self.errory.setText("Error: Nieprawidłowe dane wejściowe dla a lub b.")
                    self.l6.setText(f"")
                    self.l6l.setText(f"")
                    self.l6r.setText(f" ")
                    self.l8.setText(f"")
                    self.l8l.setText(f"")
                    self.l8r.setText(f"")
                    self.l9.setText(f"")
                    self.l9l.setText(f"")
                    self.l9r.setText(f"")
                    return

        try:

            result_midpoint = self.metoda_prostokatow_midpoint(self.n, a, b)
            if result_midpoint is None:
                self.l6.setText("Error: Problem z obliczeniem wartości.")
                self.l8.setText(f"")
                self.l9.setText(f"")
                return

            result_leftside = self.metoda_prostokatow_leftside(self.n, a, b)
            if result_leftside is None:
                self.l6l.setText("Error: Problem z obliczeniem wartości.")
                self.l8l.setText(f"")
                self.l9l.setText(f"")
                return

            result_rightside = self.metoda_prostokatow_rightside(self.n, a, b)
            if result_rightside is None:
                self.l6r.setText("Error: Problem z obliczeniem wartości.")
                self.l8r.setText(f"")
                self.l9r.setText(f"")
                return
        except Exception as e:
            self.errory.setText(f"Error: Wystąpił problem podczas obliczeń.")
            self.l6.setText(f"")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return
        try:
            self.error(a, b, result_leftside, result_rightside, result_midpoint)
        except Exception as e:
            self.errory.setText(f"Error: Błąd z errorem")
            self.l6.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")
            return e

        self.update_wykres_midpoint(a, b)
        self.update_wykres_leftside(a, b)
        self.update_wykres_rightside(a, b)

    def update_wykres_midpoint(self, a, b):
        if a is None or b is None or a >= b:
            return

        self.figure1.clear()
        ax = self.figure1.add_subplot(111)

        h = (b - a) / self.n
        x = [a + i * h for i in range(self.n)]
        y = [self.f(a + (i + 0.5) * h) for i in range(self.n)]
        ax.grid(True, alpha=0.2)
        xi = [x[i] + h / 2 for i in range(self.n)]
        ax.scatter(xi, y, color='red', marker=".")

        for i in range(self.n):
            rect = Rectangle((x[i], 0), h, y[i], linewidth=1, edgecolor='r', facecolor='r',
                             alpha=0.5)
            ax.add_patch(rect)

        start = a - 2
        stop = b + 2

        x_f = np.linspace(start, stop, 300)
        y_f = self.f(x_f)
        ax.plot(x_f, y_f, 'b-', linewidth=1, label=self.rownanie.text())
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend(loc='upper left')
        self.canvas1.draw()

    def update_wykres_leftside(self, a, b):
        if a is None or b is None or a >= b:
            return

        self.figure2.clear()
        ax = self.figure2.add_subplot(111)

        h = (b - a) / self.n
        x_left = [a + i * h for i in range(self.n)]
        y_left = [self.f(x) for x in x_left]
        ax.scatter(x_left, y_left, color='red', marker=".")
        ax.grid(True, alpha=0.2)
        for i in range(len(x_left)):
            rect = Rectangle((x_left[i], 0), h, y_left[i], linewidth=1, edgecolor='r', facecolor='r', alpha=0.5)
            ax.add_patch(rect)

        start, stop = a - 2, b + 2
        x_f = np.linspace(start, stop, 300)
        y_f = self.f(x_f)
        ax.plot(x_f, y_f, 'b-', linewidth=1, label=self.rownanie.text())
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend(loc='upper left')
        self.canvas2.draw()

    def update_wykres_rightside(self, a, b):
        if a is None or b is None or a >= b:
            return

        self.figure3.clear()
        ax = self.figure3.add_subplot(111)
        h = (b - a) / self.n
        x_right = [a + (i + 1) * h for i in range(self.n)]
        y_right = [self.f(x) for x in x_right]
        ax.scatter(x_right, y_right, color='red', marker=".")
        ax.grid(True, alpha=0.2)
        for i in range(self.n):
            rect = Rectangle((x_right[i] - h, 0), h, y_right[i], linewidth=1, edgecolor='r', facecolor='r', alpha=0.5)
            ax.add_patch(rect)

        start, stop = a - 2, b + 2
        x_f = np.linspace(start, stop, 300)
        y_f = self.f(x_f)
        ax.plot(x_f, y_f, 'b-', linewidth=1, label=self.rownanie.text())
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend(loc='upper left')
        self.canvas3.draw()
