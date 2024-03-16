import numpy as np
import timeit
import math
from sympy import sympify, lambdify, solve, diff, symbols
from PyQt5.QtCore import Qt, QCoreApplication, QLocale
from PyQt5.QtWidgets import (QGridLayout, QLabel, QComboBox, QLineEdit, QSlider, QHBoxLayout,
                             QPushButton, QDialog, QTabWidget, QVBoxLayout, QWidget)
from PyQt5.QtGui import QDoubleValidator, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from sympy.core.sympify import SympifyError

import instrukcja
import metoda_pr
import oblicz_regula_3_8
import oblicz_simpson
import oblicz_trapez


class Oblicz(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # self.setStyleSheet("background-color: white;")
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
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(1)
        start = QLabel('1')
        end = QLabel('50')
        oblicz = QPushButton('Oblicz', self)
        self.wartosc = QLabel("Liczba node'ów: 1", self)
        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.figure3 = Figure()
        self.canvas3 = FigureCanvas(self.figure3)

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
        self.combo.addItem("Metoda trapezów", "window1")
        self.combo.addItem("Metoda Simpsona", "window2")
        self.combo.addItem("Reguła 3/8", "window3")

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
        layout.addWidget(self.l6l, 10, 0, 1, 2)
        layout.addWidget(self.l6r, 11, 0, 1, 2)
        layout.addWidget(self.l7, 12, 0, 1, 2)

        # tab for errors and time

        self.tabTimeErrors = QTabWidget(self)

        self.tabt = QWidget()
        self.tabt.layout = QVBoxLayout(self.tabt)
        self.tabt.layout.addWidget(self.l8)
        self.tabt.layout.addWidget(self.l8l)
        self.tabt.layout.addWidget(self.l8r)

        self.tabe = QWidget()
        self.tabe.layout = QVBoxLayout(self.tabt)
        self.tabe.layout.addWidget(self.l9)
        self.tabe.layout.addWidget(self.l9l)
        self.tabe.layout.addWidget(self.l9r)

        self.tabTimeErrors.addTab(self.tabt, "Czas")
        self.tabTimeErrors.addTab(self.tabe, "Błędy")

        layout.addWidget(self.tabTimeErrors, 13, 0, 4, 2)

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

        # layout.addWidget(self.canvas, 0, 3, 15, 1)
        layout.addWidget(self.tabWidget, 0, 3, 17, 1)

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

        layout.addLayout(layout_for_buttons, 25, 0, 1, 2)

        self.setLayout(layout)
        self.setFontForLayout(layout, self.font)
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
            self.window.show()
        elif self.combo.itemData(index) == "window2":
            self.window = oblicz_simpson.ObliczSimpson()
            self.window.show()
        elif self.combo.itemData(index) == "window3":
            self.window = oblicz_regula_3_8.ObliczRegula()
            self.window.show()

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
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_occured = True
            return
        try:
            self.get_a_b()
        except Exception as e:
            self.l6.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.2")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_occured = True
            return

    def f(self, x):
        rownanie_string = self.rownanie.text()
        try:
            rownanie_matematyczne = sympify(rownanie_string)
            x_sym = rownanie_matematyczne.free_symbols
            x_sym_sorted = sorted(x_sym, key=lambda s: s.name)
            if len(x_sym_sorted) != 1:
                self.l6.setText("Error: Funkcja powinna zawierać tylko jedną zmienną.")
                self.l6l.setText(f"")
                self.l6r.setText(f" ")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l8r.setText(f"")
                self.error_ocurred = True

                return None
        except Exception as e:
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.3")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_ocurred = True

            return None
        try:
            funkcja = lambdify(x_sym_sorted, rownanie_matematyczne, 'numpy')
            return funkcja(x)
        except ValueError:
            self.l6.setText("Error: Wartość nieprawidłowa.")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            return
        except Exception as e:
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.4")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")

            self.error_ocurred = True

            return

    def dzielenie_przez_zero(self, funkcja, x):
        denominator = funkcja.as_numer_denom()[1]
        punkty = solve(denominator, x)
        if punkty:
            self.l7.setText(f"Error: W zakresie [a,b] nie mogą znajdować sie te punkty: {punkty}")
            return punkty

    def metoda_prostokatow_midpoint(self, n, a, b):
        try:
            h = (b - a) / n
            wynik = 0
            for i in range(n):
                xi = a + (i + 0.5) * h
                wynik += self.f(xi) * h

            if math.isnan(wynik):
                self.l6.setText("Error: Podana została zła funkcja lub jej przedziały.")
                self.l6l.setText(f"")
                self.l6r.setText(f" ")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l8r.setText(f"")
                self.error_occured = True
                return None
            else:
                self.l6.setText(f"Wynik dla midpoint: {wynik}")
                return wynik

        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji.")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_occured = True
            return e

    def metoda_prostokatow_leftside(self, n, a, b):
        try:
            h = (b - a) / n
            wynik = 0
            for i in range(n):
                xi = a + i * h
                wynik += self.f(xi) * h

            if math.isnan(wynik):
                self.l6.setText("Error: Podana została zła funkcja lub jej przedziały.")
                self.l6l.setText(f"")
                self.l6r.setText(f" ")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l8r.setText(f"")
                self.error_occured = True
                return None
            else:
                self.l6l.setText(f"Wynik da left side: {wynik}")
                return wynik

        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji.")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_occured = True
            return e

    def metoda_prostokatow_rightside(self, n, a, b):
        try:
            h = (b - a) / n
            wynik = 0
            for i in range(1, n + 1):
                xi = a + i * h
                wynik += self.f(xi) * h

            if math.isnan(wynik):
                self.l6.setText("Error: Podana została zła funkcja lub jej przedziały.")
                self.l6l.setText(f"")
                self.l6r.setText(f" ")
                self.l8.setText(f"")
                self.l8l.setText(f"")
                self.l8r.setText(f"")
                self.error_occured = True
                return None
            else:
                self.l6r.setText(f"Wynik rightside: {wynik}")
                return wynik
        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji.")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_occured = True
            return e

    def error(self, n, a, b, rownanie, symbol):
        if len(symbol) != 1:
            self.l6.setText("Error: Funkcja powinna zawierać tylko jedną zmienną. 2")
            self.l6l.setText(f"")
            self.l6r.setText(f"")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.l9.setText(f"")
            self.l9l.setText(f"")
            self.l9r.setText(f"")

        else:
            x = symbol[0]

        values = np.linspace(a, b, n + 1) # nie jestem pewna tego n+1
        h = (b - a) / n
        df = diff(rownanie, x)
        f_prime = lambdify(symbol, df, 'numpy')
        M1 = max(abs(f_prime(xi)) for xi in values)
        d2f = diff(df, x)
        f_double_prime = lambdify(symbol, d2f, 'numpy')
        M2 = max(abs(f_double_prime(xi)) for xi in values)
        try:
            error_m = (b - a)**3 / 24 * self.n**2 * M2
            error_l = (b - a)**2 / (2*self.n) * M1
            error_r = (b - a)**2 / (2*self.n) * M1

            self.l9.setText(f"Błąd dla midpoint: {error_m}")
            self.l9l.setText(f"Błąd dla left side: {error_l}")
            self.l9r.setText(f"Błąd dla right side: {error_r}")
        except Exception as e:
            self.l6.setText(f"Error: Nie można obliczyć błędów metody")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            return

    def slider_nodes(self, value):
        self.n = value
        self.wartosc.setText(f"Liczba node'ów: {value}")
        self.get_a_b()

    def get_a_b(self):
        if self.rownanie.text().strip() == "":
            self.l6.setText("Error: Wpisz równanie")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_ocurred = True
            return
        if self.a.text().strip() == "":
            self.l6.setText("Error: a nie może być puste")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_ocurred = True
            return
        if self.b.text().strip() == "":
            self.l6.setText("Error: b nie może być puste")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_ocurred = True
            return
        try:
            a = float(self.a.text())
            b = float(self.b.text())
        except ValueError:
            self.l6.setText("Error: Nieprawidłowe dane wejściowe dla a lub b.")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_ocurred = True
            return
        if a >= b:
            self.l6.setText("Error: a powinno być mniejsze niż b.")
            self.l6l.setText(f"")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            self.error_ocurred = True
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
            result_midpoint = self.metoda_prostokatow_midpoint(self.n, a, b)
            end_time = timeit.default_timer()
            if result_midpoint is None:
                self.l6.setText("Error: Problem z obliczeniem wartości dla midpoint.")
                return
            time = end_time - start_time
            self.l8.setText(f"Czas potrzebny do obliczenia midpoint: {time}")

            start_timel = timeit.default_timer()
            result_leftside = self.metoda_prostokatow_leftside(self.n, a, b)
            end_timel = timeit.default_timer()
            if result_leftside is None:
                self.l6l.setText("Error: Problem z obliczeniem wartości dla left side.")
                return
            timel = end_timel - start_timel
            self.l8l.setText(f"Czas potrzebny do obliczenia left side: {timel}")

            start_timer = timeit.default_timer()
            result_rightside = self.metoda_prostokatow_rightside(self.n, a, b)
            end_timer = timeit.default_timer()
            if result_rightside is None:
                self.l6r.setText("Error: Problem z obliczeniem wartości dla right side.")
                return
            timer = end_timer - start_timer
            self.l8r.setText(f"Czas potrzebny do obliczenia right side: {timer}")
        except Exception as e:
            self.l6.setText(f"Error: Wystąpił problem podczas obliczeń.")
            self.l6l.setText(f"rror: Wystąpił problem podczas obliczeń.")
            self.l6r.setText(f" ")
            self.l8.setText(f"")
            self.l8l.setText(f"")
            self.l8r.setText(f"")
            return
        try:
            self.error(self.n, a, b, rownanie_matematyczne, x_sym_sorted)
        except Exception as e:
            self.l6.setText(f"Error: Błąd z errorem")
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
        ax.plot(x_f, y_f, 'b-', linewidth=1)
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
        ax.plot(x_f, y_f, 'b-', linewidth=1)
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
        ax.plot(x_f, y_f, 'b-', linewidth=1)
        self.canvas3.draw()
