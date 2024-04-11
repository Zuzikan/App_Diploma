import sys

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class WykresBooleProsty(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: white;")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.create_plot(-10, 10, 4)

        self.setLayout(layout)
        self.setWindowTitle("Prosta metoda Boole'a")

    def create_plot(self, a, b, n):

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if n % 4 != 0:
            n += 4 - n % 4

        x_points = np.linspace(a, b, n + 1)
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

        for i in range(0, n, 4):
            xs = x_points[i:i + 5]
            ys = y_points[i:i + 5]
            ax.fill_between(xs, 0, ys, color='red', alpha=0.3, step='pre', linewidth=0.5, edgecolor='r')
            ax.scatter(xs, ys, color='red', marker=".")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title("Przedział: [-10,10], n = 4")
        ax.grid(True, alpha=0.2)
        self.canvas.draw()

    @staticmethod
    def f(x):
        return x ** 2 + 2 * x + 20


class WykresBooleZlozony(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: white;")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.create_plot_2(-10, 10, 12)

        self.setLayout(layout)
        self.setWindowTitle("Złożona metoda Boole'a")

    def create_plot_2(self, a, b, n):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if n % 4 != 0:
            n += 4 - n % 4

        x_points = np.linspace(a, b, n + 1)
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

        for i in range(0, n, 4):
            xs = x_points[i:i + 5]
            ys = y_points[i:i + 5]
            ax.fill_between(xs, 0, ys, color='red', alpha=0.3, step='pre', linewidth=0.5, edgecolor='r')
            ax.scatter(xs, ys, color='red', marker=".")
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title("Przedział: [-10,10], n = 12")
        ax.grid(True, alpha=0.2)
        self.canvas.draw()

    @staticmethod
    def f(x):
        return x ** 2 + 2 * x + 20


def main():
    app = QApplication(sys.argv)
    ex = WykresBooleProsty()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
