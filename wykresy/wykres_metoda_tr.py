import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import PyQt5.QtGui as qtg


class WykresTrapez(QWidget):
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

        self.create_plot()

        self.setLayout(layout)
        self.setWindowTitle('Przedział z jednym trapezem')

    def create_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        x_values = np.linspace(-5, 6, 100)
        y_values = self.f(x_values)
        ax.plot(x_values, y_values, color='b', label="x²")
        ax.scatter([2, 5], [self.f(2), self.f(5)], color='r')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.grid(True, alpha=0.2)
        trapez_x = [2, 5, 5, 2, 2]
        trapez_y = [self.f(2), self.f(5), 0, 0, self.f(2)]
        ax.fill(trapez_x, trapez_y, color='red', alpha=0.4)
        ax.plot(trapez_x, trapez_y, color='red')
        ax.text(2, self.f(2), "a=x0", fontsize=10, ha='right', va='bottom')
        ax.text(5, self.f(5), 'b=x1', fontsize=10, ha='right', va='bottom')
        ax.set_title("Przedział: [2;5], n = 1")
        ax.legend(loc='upper left')
        self.show()
        self.canvas.draw()

    @staticmethod
    def f(x):
        return x ** 2


class WykresTrapezy(QWidget):
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

        self.create_plot_2()

        self.setLayout(layout)
        self.setWindowTitle('Przedział z wieloma trapezami')

    def create_plot_2(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        x_values = np.linspace(-1, 6, 100)
        y_values = self.f(x_values)
        ax.plot(x_values, y_values, color='b', label="sin(x)+sin(2x)+sin(3x)+4")
        ax.scatter([0, 1, 2, 3, 4, 5], [self.f(0), self.f(1), self.f(2), self.f(3), self.f(4), self.f(5)], color='r')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.grid(True, alpha=0.2)
        for i in range(5):
            trapez_x = [i, i + 1]
            trapez_y = [self.f(i), self.f(i + 1)]
            ax.fill_between(trapez_x, [0, 0], trapez_y, color='red', alpha=0.4)
        labels = ["a = x1", "x2", "x3", "x4", "x5", "b = x6"]
        for i, label in enumerate(labels):
            ax.text(i, self.f(i), label, fontsize=10, ha='left', va='bottom')
        ax.plot([5, 5], [0, self.f(5)], color='red')
        ax.set_title("Przedział: [0,5], n = 5")
        ax.legend(loc='upper left')
        self.show()
        self.canvas.draw()

    @staticmethod
    def f(x):
        return np.sin(x) + np.sin(2*x) + np.sin(3*x) + 4
