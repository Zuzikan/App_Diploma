import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def create_square(ax, x_values, y_values):
    kwadrat_x = [-1, -1, 1, 1, -1]
    kwadrat_y = [3, -3, -3, 3, 3]
    ax.plot(kwadrat_x, kwadrat_y, color='red')
    ax.fill_between(x_values, -3, y_values, where=(x_values >= -1) & (x_values <= 1), color='red', alpha=0.5)
    ax.text(-1, -1, 'a', fontsize=10, ha='right', va='bottom')
    ax.text(1, 3, 'b', fontsize=10, ha='right', va='bottom')


class WykresKwadrat(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: white;")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.create_plot()

        self.setLayout(layout)
        self.setWindowTitle('Przedział z jednym kwadratem')

    def create_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        x_values = np.linspace(-2, 2, 100)
        y_values = self.f(x_values)
        ax.plot(x_values, y_values, color='b')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.scatter([-1, 1], [self.f(-1), self.f(1)], color='r')
        ax.grid(True)
        create_square(ax, x_values, y_values)
        self.show()
        self.canvas.draw()

    @staticmethod
    def f(x):
        return 2 * x + 1


class WykresKwadraty(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: white;")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.create_plot_2()

        self.setLayout(layout)
        self.setWindowTitle('Przedział z wieloma kwadratami')

    def create_plot_2(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        x_values = np.linspace(-5, 6, 100)
        y_values = self.f(x_values)
        ax.plot(x_values, y_values, color='b')
        ax.scatter([1, 2, 3, 4, 5], [self.f(1), self.f(2), self.f(3), self.f(4), self.f(5)], color='r')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.grid(True)
        for i in range(0, 4):
            kwadrat_x = [1 + i, 2 + i, 2 + i, 1 + i, 1 + i]
            kwadrat_y = [self.f(1 + i), self.f(1 + i), 0, 0, self.f(1 + i)]
            ax.fill_between(kwadrat_x, kwadrat_y, color='red', alpha=0.5)
            ax.plot(kwadrat_x, kwadrat_y, color='red')
        labels = ["x2", "x3", "x4"]
        for i, label in enumerate(labels):
            ax.text(i+2, self.f(i+2), label, fontsize=10, ha='right', va='bottom')
        ax.text(1, self.f(1), "a=x1", fontsize=10, ha='right', va='bottom')
        line_x = [5, 5]
        line_y = [0, self.f(5)]
        ax.plot(line_x, line_y, color='red', )
        ax.text(5, self.f(5), 'b=x5', fontsize=10, ha='right', va='bottom')
        self.show()
        self.canvas.draw()

    @staticmethod
    def f(x):
        return 2 * x ** 2
