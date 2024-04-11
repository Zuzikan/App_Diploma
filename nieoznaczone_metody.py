import sys

import PyQt5.QtCore as qtc
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QDialog, QApplication)


class Podstawienie(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()

        l1 = QLabel("<h3>Całkowanie przez podstawienie</h3>")
        l2 = QLabel("Zmiana zmiennej całkowania na inną, co ułatwia funkcję podcałkową:")
        l3 = QLabel("np.:")

        add_label(l1, layout)
        add_label(l2, layout)
        add_pic("zdjecia/Nieoznaczone/Podstawienie/podstawienie_1.png", layout)
        add_label(l3, layout)
        add_pic("zdjecia/Nieoznaczone/Podstawienie/podstawienie_2.png", layout)

        self.setLayout(layout)
        self.setWindowTitle("Całkowanie przez podstawienie")


class Czesci(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()

        l1 = QLabel("<h3>Całkowanie przez części</h3>")
        l2 = QLabel("Rozkład trudnych całek na łatwiejsze składniki:")
        l3 = QLabel("np.:")
        l4 = QLabel("lub")

        add_label(l1, layout)
        add_label(l2, layout)
        add_pic("zdjecia/Nieoznaczone/Czesci/czesci_1.png", layout)
        add_label(l4, layout)
        add_pic("zdjecia/Nieoznaczone/Czesci/czesci_2.png", layout)
        add_label(l3, layout)
        add_pic("zdjecia/Nieoznaczone/Czesci/czesci_3.png", layout)

        self.setLayout(layout)
        self.setWindowTitle("Całkowanie przez części")


class Rozklad(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()

        l1 = QLabel("<h3>Rozkład na ułamki proste</h3>")
        l2 = QLabel("Stosowana do funkcji wymiernych, czyli funkcji, które są ilorazem dwóch wielomianów:")
        l3 = QLabel("np.:")

        add_label(l1, layout)
        add_label(l2, layout)
        add_pic("zdjecia/Nieoznaczone/Rozklad/rozklad_1.png", layout)
        add_label(l3, layout)
        add_pic("zdjecia/Nieoznaczone/Rozklad/rozklad_2.png", layout)

        self.setLayout(layout)
        self.setWindowTitle("Rozkład na ułamki proste")


def add_label(name, layout):
    layout.addWidget(name)
    name.setAlignment(qtc.Qt.AlignCenter)


def add_pic(path, layout_name):
    label_pic = QLabel()
    label_pic.setPixmap(QPixmap(path))
    label_pic.setAlignment(qtc.Qt.AlignCenter)
    layout_name.addWidget(label_pic)


def main():
    app = QApplication(sys.argv)
    ex = Czesci()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
