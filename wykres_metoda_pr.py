import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle


def create_square(ax, x_values, y_values):
    kwadrat_x = [-1, -1, 1, 1, -1]
    kwadrat_y = [3, -3, -3, 3, 3]
    ax.plot(kwadrat_x, kwadrat_y, color='red')
    ax.fill_between(x_values, -3, y_values, where=(x_values >= -1) & (x_values <= 1), linewidth=1, edgecolor='r',
                    facecolor='r', alpha=0.5)
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
        ax.scatter([-1, 1], [self.f(-1), self.f(1)], linewidth=1, edgecolor='r', facecolor='r')
        ax.grid(True, alpha=0.2)
        create_square(ax, x_values, y_values)
        ax.set_title("Przedział: [-1;1], n = 1")
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
        self.resize(600, 500)
        layout = QVBoxLayout()

        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.figure3 = Figure()
        self.canvas3 = FigureCanvas(self.figure3)

        self.tabWidget = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab1.layout = QVBoxLayout(self.tab1)
        self.tab1.layout.addWidget(self.canvas1)

        self.tab2 = QWidget()
        self.tab2.layout = QVBoxLayout(self.tab2)
        self.tab2.layout.addWidget(self.canvas2)

        self.tab3 = QWidget()
        self.tab3.layout = QVBoxLayout(self.tab3)
        self.tab3.layout.addWidget(self.canvas3)

        self.tabWidget.addTab(self.tab1, "Left side")
        self.tabWidget.addTab(self.tab2, "Midpoint")
        self.tabWidget.addTab(self.tab3, "Right side")

        layout.addWidget(self.tabWidget)
        self.create_plot_2()
        self.create_plot_3()
        self.create_plot_4()

        self.setLayout(layout)
        self.setWindowTitle('Przedział z wieloma kwadratami')

    def create_plot_2(self):
        self.figure1.clear()
        ax = self.figure1.add_subplot(111)

        h = (5 - 1) / 4
        x_left = [1 + i * h for i in range(4)]
        y_left = [self.f(x) for x in x_left]
        ax.scatter(x_left, y_left, color='red', marker=".")
        ax.grid(True, alpha=0.2)
        for i in range(len(x_left)):
            rect = Rectangle((x_left[i], 0), h, y_left[i], linewidth=1, edgecolor='r', facecolor='r', alpha=0.5)
            ax.add_patch(rect)
        ax.text(1, self.f(1), 'a=x1', fontsize=10, ha='right', va='bottom')
        ax.text(2, self.f(2), 'x2', fontsize=10, ha='right', va='bottom')
        ax.text(3, self.f(3), 'x3', fontsize=10, ha='right', va='bottom')
        ax.text(4, self.f(4), 'b=x4', fontsize=10, ha='right', va='bottom')

        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title("Przedział: [1;5], n = 4")

        start, stop = 1 - 2, 5 + 2
        x_f = np.linspace(start, stop, 300)
        y_f = self.f(x_f)
        ax.plot(x_f, y_f, 'b-', linewidth=1)
        self.show()
        self.canvas1.draw()

    def create_plot_3(self):
        self.figure2.clear()
        ax = self.figure2.add_subplot(111)

        h = (5 - 1) / 4
        x = [1 + i * h for i in range(4)]
        y = [self.f(1 + (i + 0.5) * h) for i in range(4)]
        ax.grid(True, alpha=0.2)
        xi = [x[i] + 0.5 for i in range(4)]
        ax.scatter(xi, y, color='red', marker=".")

        for i in range(4):
            rect = Rectangle((x[i], 0), h, y[i], linewidth=1, edgecolor='r', facecolor='r',
                             alpha=0.5)
            ax.add_patch(rect)

        ax.text(1.5, self.f(1.5), 'a=x1', fontsize=10, ha='right', va='bottom')
        ax.text(2.5, self.f(2.5), 'x2', fontsize=10, ha='right', va='bottom')
        ax.text(3.5, self.f(3.5), 'x3', fontsize=10, ha='right', va='bottom')
        ax.text(4.5, self.f(4.5), 'b=x4', fontsize=10, ha='right', va='bottom')

        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title("Przedział: [1;5], n = 4")
        start = 1 - 2
        stop = 5 + 2

        x_f = np.linspace(start, stop, 300)
        y_f = self.f(x_f)
        ax.plot(x_f, y_f, 'b-', linewidth=1)
        self.canvas2.draw()

    def create_plot_4(self):
        self.figure3.clear()
        ax = self.figure3.add_subplot(111)

        h = (5 - 1) / 4
        x = [1 + (i + 1) * h for i in range(4)]
        y = [self.f(i) for i in x]
        ax.grid(True, alpha=0.2)
        ax.scatter(x, y, color='red', marker=".")

        for i in range(4):
            rect = Rectangle((x[i] - h, 0), h, y[i], linewidth=1, edgecolor='r', facecolor='r',
                             alpha=0.5)
            ax.add_patch(rect)


        ax.text(2, self.f(2), 'a=x1', fontsize=10, ha='right', va='bottom')
        ax.text(3, self.f(3), 'x2', fontsize=10, ha='right', va='bottom')
        ax.text(4, self.f(4), 'x3', fontsize=10, ha='right', va='bottom')
        ax.text(5, self.f(5), 'b=x4', fontsize=10, ha='right', va='bottom')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title("Przedział: [1;5], n = 4")

        start = 1 - 2
        stop = 5 + 2

        x_f = np.linspace(start, stop, 300)
        y_f = self.f(x_f)
        ax.plot(x_f, y_f, 'b-', linewidth=1)
        self.canvas3.draw()

    @staticmethod
    def f(x):
        return 2 * x ** 2
