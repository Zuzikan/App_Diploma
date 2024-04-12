import sys
import PyQt5.QtGui as qtg
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def punkty():
    random_points_x = np.random.uniform(0, 5, 50)
    random_points_y = np.random.uniform(0, 25, 50)
    return random_points_x, random_points_y


def punkty2():
    random_points_x = np.round(np.random.uniform(0, 5, 50), 1)
    random_points_y = np.round(np.random.uniform(0, 5, 50), 1)
    random_points_z = np.round(np.random.uniform(0, 10, 50), 1)

    return random_points_x, random_points_y, random_points_z


class WykresMC2WS(QWidget):
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

        self.create_plot(0, 5)

        self.setLayout(layout)
        self.setWindowTitle("Metoda Monte Carlo 2D wartości średniej")

    def create_plot(self, a, b):
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')
        ar_x, ar_y, ar_z = punkty2()
        f_values = self.fxy(ar_x, ar_y)
        x = np.linspace(a, b, 100)
        y = np.linspace(a, b, 100)
        x, y = np.meshgrid(x, y)
        z = self.fxy(x, y)

        ax.scatter(ar_x, ar_y, f_values, color='red', marker=".", label="Punkty Monte Carlo")

        surf = ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5, linewidth=0, antialiased=False,
                               label="x+y")

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('f(x, y)')
        ax.set_title("Przedział: [0,5], n = 50")
        surf._facecolors2d = surf._facecolor3d
        surf._edgecolors2d = surf._edgecolor3d
        ax.legend(loc='upper left')

        ax.grid(True, alpha=0.2)
        self.canvas.draw()

    @staticmethod
    def fxy(x, y):
        return x + y


class WykresMC2HOM(QWidget):
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

        self.create_plot(0, 5)

        self.setLayout(layout)
        self.setWindowTitle("Metoda Monte Carlo 2D hit or miss")

    def create_plot(self, a, b):
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')
        ar_x, ar_y, ar_z = punkty2()
        f_values = np.array([self.fxy(x, y) for x, y in zip(ar_x, ar_y)])
        threshold = 0.1
        points_on_curve = np.abs(f_values - ar_z) < threshold
        points_under_curve = ar_z < f_values
        points_above_curve = ar_z > f_values

        x = np.linspace(a, b, 100)
        y = np.linspace(a, b, 100)
        x, y = np.meshgrid(x, y)
        z = self.fxy(x, y)

        ax.scatter(ar_x[points_on_curve], ar_y[points_on_curve], ar_z[points_on_curve], color='green', marker=".",
                   label="Punkty w obszarze")
        ax.scatter(ar_x[points_under_curve], ar_y[points_under_curve], ar_z[points_under_curve], color='green',
                   marker=".")
        ax.scatter(ar_x[points_above_curve], ar_y[points_above_curve], ar_z[points_above_curve], color='red',
                   marker=".",
                   label="Punkty poza obszarem")
        surf = ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5, linewidth=0, antialiased=False,
                               label="x+y")

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('f(x, y)')
        ax.set_title("Przedział: [0,5], n = 50")
        surf._facecolors2d = surf._facecolor3d
        surf._edgecolors2d = surf._edgecolor3d
        ax.legend(loc='upper left')

        ax.grid(True, alpha=0.2)
        self.canvas.draw()

    @staticmethod
    def fxy(x, y):
        return x + y


class WykresMC1WS(QWidget):
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

        self.create_plot(0, 5)

        self.setLayout(layout)
        self.setWindowTitle("Metoda Monte Carlo 1D wartości średniej")

    def create_plot(self, a, b):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ar_x, ar_y = punkty()
        y_random = [self.f(x) for x in ar_x]

        ax.scatter(ar_x, y_random, color='red', marker=".", label="Punkty Monte Carlo")

        x_fine = np.linspace(a, b, 3000)
        y_fine = [self.f(x) for x in x_fine]
        ax.plot(x_fine, y_fine, 'b-', linewidth=1, label="x²")
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title("Przedział: [0,5], n = 50")
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.2)
        self.canvas.draw()

    @staticmethod
    def f(x):
        return x ** 2


class WykresMC1HOM(QWidget):
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

        self.create_plot(0, 5)

        self.setLayout(layout)
        self.setWindowTitle('Metoda Monte Carlo 1D hit or miss')

    def create_plot(self, a, b):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ar_x, ar_y = punkty()
        f_values = np.array([self.f(x) for x in ar_x])

        threshold = 0.001
        points_on_curve = np.abs(f_values - ar_y) < threshold
        points_under_curve = ar_y < f_values
        points_above_curve = ~points_under_curve

        ax.scatter(ar_x[points_under_curve], ar_y[points_under_curve], color='green', marker=".",
                   label="W obszarze")
        ax.scatter(ar_x[points_on_curve], ar_y[points_on_curve], color='green', marker=".")
        ax.scatter(ar_x[points_above_curve], ar_y[points_above_curve], color='red', marker=".", label="Poza obszarem")

        x_fine = np.linspace(a, b, 300)
        y_fine = [self.f(x) for x in x_fine]
        ax.plot(x_fine, y_fine, 'b-', linewidth=1, label="x²")

        ax.grid(True, which='both', linestyle='--', linewidth=0.2)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title("Przedział: [0,5], n = 50")
        ax.legend(loc='upper left')
        self.canvas.draw()

    @staticmethod
    def f(x):
        return x ** 2


def main():
    app = QApplication(sys.argv)
    ex = WykresMC1WS()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
