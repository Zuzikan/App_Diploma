import sys
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from sympy import symbols, sympify, lambdify
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import numpy as np


class Oblicz(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.sliderLayout = QHBoxLayout()
        abHorizontal = QHBoxLayout()

        l2 = QLabel("Wpisz równanie: ", self)
        self.rownanie = QLineEdit(self)

        self.l6 = QLabel("Wynik: ", self)
        oblicz = QPushButton('Oblicz', self)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(2)
        self.slider.setMaximum(50)
        self.slider.setValue(2)
        self.n = 2  # Initialize slider value
        start = QLabel('2')
        end = QLabel('50')
        self.wartosc = QLabel("Liczba node'ów: 2", self)

        la = QLabel("a: ", self)
        lb = QLabel("b:", self)
        self.a = QLineEdit(self)
        self.b = QLineEdit(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        oblicz.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

        self.layout.addWidget(l2, 0, 0)
        self.layout.addWidget(self.rownanie, 1, 0)
        self.layout.addWidget(oblicz, 6, 0)
        self.layout.addWidget(self.l6, 2, 0)
        self.layout.addWidget(self.wartosc, 3, 0)

        abHorizontal.addWidget(la)
        abHorizontal.addWidget(self.a)

        abHorizontal.addWidget(lb)
        abHorizontal.addWidget(self.b)

        self.layout.addLayout(abHorizontal, 4, 0, 1, 2)

        self.sliderLayout.addWidget(start)
        self.sliderLayout.addWidget(self.slider)
        self.sliderLayout.addWidget(end)

        self.layout.addLayout(self.sliderLayout, 5, 0, 1, 2)

        # Connection
        self.slider.valueChanged.connect(self.slider_value_changed)
        oblicz.clicked.connect(self.calculate_result)
        self.layout.addWidget(self.canvas, 0, 2, 5, 2)

        self.setLayout(self.layout)
        self.setWindowTitle('Oblicz')

    def f(self, x):
        rownanie_string = self.rownanie.text()
        x_sym = symbols('x')
        rownanie_matematyczne = sympify(rownanie_string)
        funkcja = lambdify(x_sym, rownanie_matematyczne, 'numpy')
        return funkcja(x)

    def metoda_prostokatow(self, n, a, b):
        h = (b - a) / n
        wynik = 0
        for i in range(n):
            xi = a + (i + 0.5) * h
            wynik += self.f(xi) * h
        self.l6.setText(f"Wynik: {wynik}")

    def slider_value_changed(self, value):
        self.n = value
        self.wartosc.setText(f"Liczba node'ów: {value}")
        self.calculate_result()  # Perform calculation whenever the slider value changes

    def calculate_result(self):
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
        self.metoda_prostokatow(self.n, a, b)
        self.update_plot(a, b)

    def update_plot(self, a, b):
        if a is None or b is None or a >= b:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlim(a, b)
        h = (b - a) / self.n
        x_positions = [a + i * h for i in range(self.n)]
        y_positions = [self.f(a + (i + 0.5) * h) for i in range(self.n)]
        y_max = max(y_positions)
        ax.set_ylim(0, y_max + y_max * 0.1)

        for i in range(self.n):
            rect = Rectangle((x_positions[i], 0), h, y_positions[i], linewidth=1, edgecolor='r', facecolor='r',
                             alpha=0.5)
            ax.add_patch(rect)

        x_curve = np.linspace(a, b, 300)
        y_curve = [self.f(x) for x in x_curve]
        ax.plot(x_curve, y_curve, 'b-', linewidth=1)
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    ex = Oblicz()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
