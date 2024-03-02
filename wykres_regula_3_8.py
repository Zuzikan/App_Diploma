import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class WykresRegula38(QWidget):
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
        self.setWindowTitle('Przedziały Reguła 3/8')

    def create_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        x = np.linspace(0, 13, 200)
        y_f = self.f(x)
        y_f2 = self.f_2(x)
        ax.clear()
        ax.plot(x, y_f)
        ax.plot(x, y_f2)
        ax.grid(True)
        idx = np.argwhere(np.diff(np.sign(y_f - y_f2))).flatten()
        intersections_x = x[idx]
        ax.plot(x[idx], y_f2[idx], 'ro')
        ax.fill_between(x, 0, y_f2, where=(x >= intersections_x[0]) & (x <= intersections_x[3]), color='orange',
                        alpha=0.3)
        ax.text(intersections_x[0], self.f_2(intersections_x[0]), "a", fontsize=12, ha='right', va='bottom')
        ax.text(intersections_x[1], self.f_2(intersections_x[1]), "x1", fontsize=12, ha='left', va='bottom')
        ax.text(intersections_x[2], self.f_2(intersections_x[2]), "x2", fontsize=12, ha='left', va='bottom')
        ax.text(intersections_x[3], self.f_2(intersections_x[3]), "b", fontsize=12, ha='left', va='bottom')

        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        self.show()
        self.canvas.draw()

    @staticmethod
    def f(x):
        return np.sin(x) + 1.5

    @staticmethod
    def f_2(x):
        return np.sin(x + np.pi / 4) + 1.5


