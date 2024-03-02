import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    @staticmethod
    def f(x):
        return np.sin(x) + 1.5

    @staticmethod
    def f_2(x):
        return np.sin(x + np.pi / 4) + 1.5

    def plot(self):
        x = np.linspace(0, 13, 200)
        y_f = PlotCanvas.f(x)
        y_f2 = PlotCanvas.f_2(x)
        ax = self.axes
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
        self.draw()


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Matplotlib Example'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        m = PlotCanvas(self, width=5, height=4)
        m.move(0, 0)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
