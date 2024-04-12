import sys
import PyQt5.QtGui as qtg

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.special import roots_chebyt


class WykresCzeb(QWidget):
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

        self.create_plot(-1, 1, 15)

        self.setLayout(layout)
        self.setWindowTitle("Przykład kwadratury Gaussa-Czebyszewa")

    def create_plot(self, a, b, n):

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        t_points, _ = roots_chebyt(n)
        x_points = (b - a) / 2 * t_points + (b + a) / 2
        y_points = [self.f(x) for x in x_points]
        ax.scatter(x_points, y_points, color='red', marker=".", label="Węzły Czebyszewa")
        ax.grid(True, alpha=0.2)

        x_fine = np.linspace(a, b, 300)
        y_fine = [self.f(x) for x in x_fine]
        ax.plot(x_fine, y_fine, 'b-', linewidth=1, label="x²+2x+20")
        ax.set_title("Przedział: [-1,1], n = 15")
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend(loc='upper left')
        self.canvas.draw()

    @staticmethod
    def f(x):
        return x ** 2 + 2 * x + 20


def main():
    app = QApplication(sys.argv)
    ex = WykresCzeb()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
