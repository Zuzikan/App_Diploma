import sys

from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QDialog, QApplication)
import PyQt5.QtCore as qtc
from PyQt5.QtGui import QPixmap, QFont


def setFontForLayout(layout, font):
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.setFont(font)


class Instrukcja(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(self)
        self.font = QFont()
        self.font.setPointSize(11)

        labels_1 = [
            "<h3>Instrukcja</h3>",
            "",
            "x<sup>i</sup> = x**i lub x^i",
            "π = pi lub 3.14",
            "arccos(x) = acos(x)",
            "arcsin(x) = asin(x)",
            "arctg(x) = atan(x)",
            "arcctg(x) = acot(x)",
            "2×3 = 2*3",
            "10÷5 = 10/5",
            "|x-5| = abs(x-5)",
            "√i = sqrt(i)",
            "ln(x) = log(x)",
            "                                                ",
        ]

        for text in labels_1:
            label = QLabel(text)
            add_label(label, layout)

        zamknij = QPushButton('Zamknij')
        zamknij.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")

        layout.addWidget(zamknij)
        zamknij.clicked.connect(self.close)

        self.setLayout(layout)
        setFontForLayout(layout, self.font)
        self.setWindowTitle('Instrukcja')


def add_label(name, layout):
    layout.addWidget(name)
    name.setAlignment(qtc.Qt.AlignCenter)


def main():
    app = QApplication(sys.argv)
    ex = Instrukcja()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
