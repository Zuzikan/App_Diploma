import sys

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.interpolate import CubicSpline


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
        x_points = np.linspace(0, 10, 7)
        y_points = [self.f(x) for x in x_points]
        ax.scatter(x_points, y_points, color='red', marker=".")
        ax.grid(True, alpha=0.2)
        ax.scatter(x_points, y_points, color='red')

        for i in range(0, 6, 3):
            if i + 3 < 7:
                x_sub = x_points[i:i + 4]
                y_sub = y_points[i:i + 4]

                cs = CubicSpline(x_sub, y_sub)
                x_sub_fine = np.linspace(x_sub[0], x_sub[-1], 100)
                ax.plot(x_sub_fine, cs(x_sub_fine), 'r-', alpha=0.5,
                        label='Reguła 3/8' if i == 0 else "")
                ax.fill_between(x_sub_fine, cs(x_sub_fine),color='orange',alpha=0.3)
        x_fine = np.linspace(0, 10, 300)
        y_fine = [self.f(x) for x in x_fine]
        ax.plot(x_fine, y_fine, 'b-', linewidth=1)

        ax.legend()
        ax.legend()
        self.show()
        self.canvas.draw()

    @staticmethod
    def f(x):
        return np.sin(x) + 1.5

    @staticmethod
    def f_2(x):
        return np.sin(x + np.pi / 4) + 1.5


def main():
    app = QApplication(sys.argv)
    ex = WykresRegula38()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()