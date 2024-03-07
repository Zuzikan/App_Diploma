import sys
import numpy as np
import timeit
from sympy import symbols, sympify, lambdify
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QComboBox, QLineEdit, QSlider, QHBoxLayout,
                             QPushButton, QDialog)
from PyQt5.QtGui import QDoubleValidator, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from sympy.core.sympify import SympifyError


class Oblicz(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # self.setStyleSheet("background-color: white;")
        font = QFont()
        font.setPointSize(12)

        layout = QGridLayout()
        sliderLayout = QHBoxLayout()
        abHorizontal = QHBoxLayout()
        layout_for_buttons = QHBoxLayout()

        combo = QComboBox(self)
        combo.addItems(["Page 1", "Page 2"])
        l1 = QLabel("Porównaj z: ", self)
        l2 = QLabel("Wpisz równanie: ", self)
        l3 = QLabel("Podaj przedział [a,b]:", self)
        self.rownanie = QLineEdit(self)
        instrukcja = QPushButton('Instrukcja', self)
        la = QLabel("a: ", self)
        lb = QLabel("b:", self)
        self.a = QLineEdit(self)
        self.b = QLineEdit(self)
        self.n = 2
        self.l6 = QLabel("Wynik: ", self)
        self.l7 = QLabel(self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(2)
        self.slider.setMaximum(50)
        self.slider.setValue(2)
        start = QLabel('2')
        end = QLabel('50')
        oblicz = QPushButton('Oblicz', self)
        self.wartosc = QLabel("Liczba node'ów: 2", self)
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
        self.a.setPlaceholderText("Wpisz wartość a")
        self.b.setPlaceholderText("Wpisz wartość b")
        self.a.setValidator(QDoubleValidator())
        self.b.setValidator(QDoubleValidator())
        self.rownanie.setPlaceholderText("Wpisz wartość całki")
        l3.setAlignment(Qt.AlignCenter)
        self.wartosc.setAlignment(Qt.AlignCenter)

        # Connect the combo box's signal to the slot
        # self.combo.activated[str].connect(self.onActivated)
        layout.addWidget(l1, 3, 0)
        layout.addWidget(combo, 3, 1)

        layout.addWidget(l2, 4, 0)
        layout.addWidget(self.rownanie, 4, 1)
        layout.addWidget(instrukcja, 5, 0, 1, 2)

        layout.addWidget(l3, 6, 0, 1, 2)

        abHorizontal.addWidget(la)
        abHorizontal.addWidget(self.a)

        abHorizontal.addWidget(lb)
        abHorizontal.addWidget(self.b)

        layout.addLayout(abHorizontal, 7, 0, 1, 2)

        layout.addWidget(oblicz, 8, 0, 1, 2)
        oblicz.clicked.connect(self.get_a_b)

        layout.addWidget(self.wartosc, 9, 0, 1, 2)

        sliderLayout.addWidget(start)
        sliderLayout.addWidget(self.slider)
        sliderLayout.addWidget(end)

        sliderLayout.setStretch(0, 1)
        sliderLayout.setStretch(1, 50)
        sliderLayout.setStretch(2, 1)

        layout.addLayout(sliderLayout, 10, 0, 1, 2)

        layout.addWidget(self.l6, 11, 0, 1, 2)
        layout.addWidget(self.l7, 12, 0, 1, 2)

        layout.addWidget(self.canvas, 0, 3, 15, 1)

        zamknij = QPushButton('Zamknij program')
        zamknij_okno = QPushButton("Zamknij okno")

        zamknij_okno.clicked.connect(self.close)
        zamknij.clicked.connect(QCoreApplication.instance().quit)

        zamknij.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")
        zamknij_okno.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")

        layout_for_buttons.addWidget(zamknij)
        layout_for_buttons.addWidget(zamknij_okno)

        layout.addLayout(layout_for_buttons, 16, 0, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle('Oblicz')

    def onActivated(self, text):
        self.label.setText(f"You selected: {text}")
        self.label.adjustSize()

    def f(self, x):
        rownanie_string = self.rownanie.text()
        try:
            x_sym = symbols('x')
            rownanie_matematyczne = sympify(rownanie_string)
        except SympifyError:
            self.l6.setText("Error: Nieprawidłowe równanie. Sprawdź wpisane dane.")
            return None

        try:
            funkcja = lambdify(x_sym, rownanie_matematyczne, 'numpy')
        except Exception as e:
            self.l6.setText(f"Error: Nie można przetworzyć równania: {e}")
            return None

        try:
            return funkcja(x)
        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji: {e}")
            return None

    def metoda_prostokatow(self, n, a, b):
        try:
            h = (b - a) / n
            wynik = 0
            for i in range(n):
                xi = a + (i + 0.5) * h
                wynik += self.f(xi) * h
            self.l6.setText(f"Wynik: {wynik}")
        except Exception as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji: {e}")

    def slider_nodes(self, value):
        self.n = value
        self.wartosc.setText(f"Liczba node'ów: {value}")
        self.get_a_b()

    def get_a_b(self):
        if self.rownanie.text().strip() == "":
            self.l6.setText("Error: Wpisz równanie")
            return
        if self.a.text().strip() == "":
            self.l6.setText("Error: a nie może być puste")
            return
        if self.b.text().strip() == "":
            self.l6.setText("Error: b nie może być puste")
            return
        try:
            a = int(self.a.text())
            b = int(self.b.text())
        except ValueError:
            self.l6.setText("Error: Nieprawidłowe dane wejściowe dla a lub b")
            return
        if a >= b:
            self.l6.setText("Error: a powinno być mniejsze niż b")
            return
        try:
            start_time = timeit.default_timer()
            self.metoda_prostokatow(self.n, a, b)
            end_time = timeit.default_timer()
            time = end_time - start_time
            self.l7.setText(f"Czas potrzebny do obliczenia: {time}")
        except ValueError as e:
            self.l6.setText(f"Error: Problem z obliczeniem wartości funkcji: {e}")

        self.update_wykres(a, b)

    def update_wykres(self, a, b):
        if a is None or b is None or a >= b:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        # ax.set_xlim(a, b)
        h = (b - a) / self.n
        x = [a + i * h for i in range(self.n)]
        y = [self.f(a + (i + 0.5) * h) for i in range(self.n)]
        ax.grid(True, alpha=0.2)
        y_max = max(y)
        # ax.set_ylim(0, y_max + y_max * 0.1)

        for i in range(self.n):
            rect = Rectangle((x[i], 0), h, y[i], linewidth=1, edgecolor='r', facecolor='r',
                             alpha=0.5)
            ax.add_patch(rect)

        start = a - 4
        stop = b + 4

        x_f = np.linspace(start, stop, 300)
        y_f = self.f(x_f)
        ax.plot(x_f, y_f, 'b-', linewidth=1)
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    ex = Oblicz()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
