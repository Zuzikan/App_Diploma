import sys
import PyQt5.QtGui as qtg
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy.polynomial.hermite import hermgauss


class WykresHerm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(qtg.QIcon('zdjecia/icon.png'))

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.create_plot(15)

        self.setLayout(layout)
        self.setWindowTitle("Przykład kwadratury Gaussa-Czebyszewa")

    def create_plot(self, n):

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        nodes, weights = hermgauss(n)
        y_points = [self.f(x) * np.exp(-x ** 2) for x in nodes]
        x_fine = np.linspace(-4, 4, 3000)
        y_fine = [self.f(x) for x in x_fine]

        ax.scatter(nodes, y_points, color='red', marker=".", label="Węzły Gaussa-Hermite'a")
        ax.grid(True, alpha=0.2)

        ax.plot(x_fine, y_fine, 'b-', linewidth=1, label="x²+2x+20")
        ax.set_title("Przedział: [-∞,∞], n = 15")
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend(loc='upper left')
        self.canvas.draw()

    @staticmethod
    def f(x):
        return x ** 2 + 2 * x + 20


def main():
    app = QApplication(sys.argv)
    ex = WykresHerm()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
