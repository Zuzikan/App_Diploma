import sys
import timeit
import numpy as np
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QComboBox, QLineEdit, QHBoxLayout,
                             QPushButton, QDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy import sympify, lambdify, integrate

import instrukcja
import oblicz_boole
import oblicz_metoda_prostokatow
import oblicz_regula_3_8
import oblicz_simpson
import oblicz_trapez


class ObliczNieoznaczona(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # self.setStyleSheet("background-color: white;")
        self.font = QFont()
        self.font.setPointSize(10)

        layout = QGridLayout()
        sliderLayout = QHBoxLayout()

        layout_for_buttons = QHBoxLayout()

        self.combo = QComboBox(self)

        l1 = QLabel("Porównaj z: ", self)
        self.error_ocurred = False
        l2 = QLabel("Wpisz równanie: ", self)
        self.rownanie = QLineEdit(self)
        instrukcja = QPushButton('Instrukcja', self)
        self.l6 = QLabel(self)
        self.l8 = QLabel(self)
        oblicz = QPushButton('Oblicz', self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        instrukcja.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        oblicz.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        l2.setAlignment(Qt.AlignCenter)
        self.rownanie.setPlaceholderText("Wpisz wartość całki")

        self.combo.addItem("Wybierz", "none")
        self.combo.addItem("Metoda prostokątów", "window1")
        self.combo.addItem("Metoda trapezów", "window2")
        self.combo.addItem("Metoda Simpsona", "window3")
        self.combo.addItem("Reguła 3/8", "window4")
        self.combo.addItem("Metoda Boole'a", "window5")

        self.combo.activated.connect(self.porownaj)
        layout.addWidget(l1, 4, 0)
        layout.addWidget(self.combo, 4, 1)

        layout.addWidget(l2, 5, 0, 1, 2)
        layout.addWidget(self.rownanie, 6, 0, 1, 2)
        layout.addWidget(instrukcja, 7, 0)
        instrukcja.clicked.connect(self.open_inst)

        layout.addWidget(oblicz, 7, 1)
        oblicz.clicked.connect(self.check_errors)

        layout.addWidget(self.l6, 8, 0, 1, 2)
        layout.addWidget(self.l8, 9, 0, 1, 2)

        layout.addWidget(self.canvas, 0, 3, 15, 1)

        zamknij = QPushButton('Zamknij program')
        zamknij_okno = QPushButton("Zamknij okno")
        powrot = QPushButton("Powrót")

        zamknij_okno.clicked.connect(self.close)
        zamknij.clicked.connect(QCoreApplication.instance().quit)
        # powrot.clicked.connect(self.wroc)

        powrot.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        zamknij.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")
        zamknij_okno.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")

        layout_for_buttons.addWidget(powrot)
        layout_for_buttons.addWidget(zamknij)
        layout_for_buttons.addWidget(zamknij_okno)

        layout.addLayout(layout_for_buttons, 14, 0, 1, 2)

        self.setLayout(layout)
        self.setFontForLayout(layout_for_buttons, self.font)
        self.setFontForLayout(layout, self.font)
        self.setWindowTitle('Obliczenia całki nieoznaczone')

    """
    def wroc(self):
        self.w = metoda_tr.MetodaTr()
        self.w.show()
        self.close()
    """

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

    def pass_data(self, window):
        try:
            rownanie = self.rownanie.text()
            self.window.rownanie.setText(rownanie)
            self.window.check_errors()
        except Exception as e:
            return

    def open_inst(self):
        self.wi = instrukcja.Instrukcja()
        self.wi.show()

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
            self.l6.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.1")
            self.l8.setText(f"")
            return
        try:
            self.get_a_b()
        except Exception as e:
            self.l6.setText(f"Error: Nieprawidłowe równanie. Sprawdź wpisane dane.2")
            self.l8.setText(f"")
            return

    def f(self, x):
        try:
            rownanie_matematyczne, x_sym_sorted = self.converter()
        except Exception as e:
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.3")
            self.l8.setText(f"")
            return None
        try:
            funkcja = lambdify(x_sym_sorted, rownanie_matematyczne, 'numpy')
            return funkcja(x)
        except ValueError:
            self.l6.setText("Error: Wartość nieprawidłowa.")
            self.l8.setText(f"")
            return
        except Exception as e:
            self.l6.setText("Error: Podana została zła funkcja. Sprawdź wpisane dane.4")
            self.l8.setText(f"")
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
            if len(x_sym_sorted) != 1:
                self.l6.setText("Error: Funkcja powinna zawierać tylko jedną zmienną.")
                self.l8.setText(f"")
                return None
            return rownanie_matematyczne, x_sym_sorted

        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji. 1")
            self.l8.setText(f"")
            return e

    def nieoznaczona(self):
        try:

            rownanie_matematyczne, x_sym_sorted = self.converter()
            start_time = timeit.default_timer()
            calka = integrate(rownanie_matematyczne, x_sym_sorted[0])
            end_time = timeit.default_timer()
            time = end_time - start_time
            self.l8.setText(f"Czas potrzebny do obliczenia: {time}")

            self.l6.setText(f"Wynik: {calka} + C")
            return calka

        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji. 1")
            self.l8.setText(f"")
            return e

    def get_a_b(self):
        if self.rownanie.text().strip() == "":
            self.l6.setText("Error: Wpisz równanie")
            self.l8.setText(f"")
            return

        try:

            result_nieoznaczona = self.nieoznaczona()
            if result_nieoznaczona is None:
                self.l6.setText("Error: Problem z obliczeniem wartości. 1")
                return
        except Exception as e:
            self.l6.setText(f"Error: Wystąpił problem podczas obliczeń.")
            return

        self.update_wykres(self.nieoznaczona())

    def update_wykres(self, calka):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        rownanie_string = self.rownanie.text()
        x_sym_sorted = self.symbols(rownanie_string)
        funkcja = lambdify(x_sym_sorted, calka, 'numpy')

        x = np.linspace(-10, 10, 300)
        y = self.f(x)
        y_fine_integral = funkcja(x)

        ax.plot(x, y, 'b-', linewidth=1, label=rownanie_string)
        ax.plot(x, y_fine_integral, color="orange", linestyle='--', linewidth=1, label=calka)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True, alpha=0.2)
        ax.legend(loc='upper left')
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    ex = ObliczNieoznaczona()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
