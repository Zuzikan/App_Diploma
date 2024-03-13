import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class WykresSimp(QWidget):
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
        self.setWindowTitle('Przedział Metoda Simpsona')

    def create_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        x = np.linspace(0, 5, 200)
        y_f = self.f(x)
        y_f2 = self.f_2(x)
        ax.clear()
        ax.plot(x, y_f)
        ax.plot(x, y_f2)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.grid(True, alpha=0.2)
        idx = np.argwhere(np.diff(np.sign(y_f - y_f2))).flatten()
        intersections_x = x[idx]
        ax.plot(x[idx], y_f2[idx], 'ro')
        ax.fill_between(x, 0, y_f2, where=(x >= intersections_x[0]) & (x <= intersections_x[2]), color='orange',
                        alpha=0.3)
        ax.text(1, self.f_2(intersections_x[0]), "a=x0", fontsize=12, ha='right', va='bottom')
        #ax.text(2.5, 0, "x1", fontsize=12, ha='left', va='bottom')
        ax.text(2.5, self.f_2(intersections_x[1]), "x1", fontsize=12, ha='right', va='bottom')
        ax.text(4, self.f_2(intersections_x[2]), "b=x2", fontsize=12, ha='left', va='bottom')
        #ax.scatter([1, 2.5, 4], [0, 0, 0], color='red')

        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title("Przedział: [1;4], n = 2")
        self.show()
        self.canvas.draw()

    @staticmethod
    def f(x):
        return 0.8 * np.sin(x) + 0.5 * x

    @staticmethod
    def f_2(x):
        return -0.19773791977030136*x**2 + 1.0624833374872868*x + 0.3084313701293318


