import sys

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import PyQt5.QtGui as qtg


def fc(x):
    return (x ** 3) / 3


class WykresNieo(QWidget):
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
        self.setWindowTitle("Całka nieoznaczona")

    def create_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        x = np.linspace(-10, 10, 300)
        y = self.f(x)
        y_fine_integral = fc(x)

        ax.plot(x, y, 'b-', linewidth=1, label="x²")
        ax.plot(x, y_fine_integral, color="orange", linestyle='--', linewidth=1, label="x³/3+C")
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.2)
        ax.legend(loc='upper left')
        self.canvas.draw()

    @staticmethod
    def f(x):
        return x ** 2


def main():
    app = QApplication(sys.argv)
    ex = WykresNieo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
