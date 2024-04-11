import sys

import PyQt5.QtCore as qtc
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QDialog, QApplication)

import nieoznaczone_metody
from obliczenia import oblicz_nieoznaczone


class Nieoznaczone(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        # layouty
        layout_for_buttons = QHBoxLayout()
        layout_horizontal = QHBoxLayout()
        layout_horizontal_new = QHBoxLayout()
        layout = QVBoxLayout()

        # czcionka
        font = QFont()
        font.setPointSize(10)

        labels_1 = [
            "<h3>Całki nieoznaczone</h3>",
            "Całki nieoznaczone odgrywają dużą role w obliczeniach pola powierzchni figur lub pola pod funkcją. ",
            "Całkowanie nieoznaczone polega na znalezieniu tak zwanej funkcji pierwotnej, czyli funkcji której pochodna ",
            "jest równa danej funkcji podcałkowej. Nie obowiązuje ograniczenie pola poddawanego całkowaniu.",
            "Całka nieoznaczona funkcji f(x) to:",


        ]
        labels_2 = [


            "Całki nieoznaczone nie są unikatowe. Istnieje nieskończona ilość całek każdej funkcji, które można ",
            "uzyskać wybierając dowolne C ze zbioru liczb rzeczywistych. Dlatego C jest zwykle określane jako stała arbitralna.",

        ]

        l1 = QLabel("Dzięki znajomości wzorów pochodnych wielu ważnych funkcji, możemy wywnioskować formuły ich całkowania np.:")
        l2 = QLabel("Niestety nie zawsze jest proste do zauważenia przez co musimy stosować inne metody obliczania")
        l3 = QLabel("całek nieoznaczonych, w tym:")

        for text in labels_1:
            label = QLabel(text)
            add_label(label, layout)

        add_pic("zdjecia/Nieoznaczone/nieoznaczone_1.png", layout)

        for text in labels_2:
            label = QLabel(text)
            add_label(label, layout)

        add_pic("zdjecia/Nieoznaczone/nieoznaczone_2.png", layout)

        add_label(l1, layout)
        add_pic("zdjecia/Nieoznaczone/nieoznaczone_3.png", layout)

        add_label(l2, layout)
        add_label(l3, layout)

        #metody
        podstawianie = QPushButton("Całkowanie przez podstawienie")
        czesci = QPushButton("Całkowanie przez części")
        rozklad = QPushButton("Rozkład na ułamki proste")

        podstawianie.clicked.connect(self.podstawienie)
        czesci.clicked.connect(self.czesci)
        rozklad.clicked.connect(self.rozklad)

        layout_horizontal.addWidget(podstawianie)
        layout_horizontal.addWidget(czesci)
        layout_horizontal.addWidget(rozklad)

        podstawianie.setStyleSheet("border-radius : 5px; background-color : #d1d1d1")
        czesci.setStyleSheet("border-radius : 5px; background-color : #d1d1d1")
        rozklad.setStyleSheet("border-radius : 5px; background-color : #d1d1d1")

        layout.addLayout(layout_horizontal)
        layout.addWidget(QLabel(""))

        #podstawowe
        zamknij = QPushButton('Zamknij program')
        zamknij_okno = QPushButton("Zamknij okno")
        obliczenia = QPushButton('Przejdź do obliczeń')

        obliczenia.clicked.connect(self.open_oblicz)
        zamknij_okno.clicked.connect(self.close)
        zamknij.clicked.connect(qtc.QCoreApplication.instance().quit)

        zamknij.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        zamknij_okno.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        obliczenia.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        zamknij.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")
        zamknij_okno.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")
        obliczenia.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

        layout_for_buttons.addWidget(zamknij)
        layout_for_buttons.addWidget(zamknij_okno)
        layout_for_buttons.addWidget(obliczenia)
        layout.addLayout(layout_for_buttons)

        self.setLayout(layout)
        self.setWindowTitle("Całki nieoznaczone")

    def podstawienie(self):
        self.w = nieoznaczone_metody.Podstawienie()
        self.w.show()

    def czesci(self):
        self.w1 = nieoznaczone_metody.Czesci()
        self.w1.show()

    def rozklad(self):
        self.w2 = nieoznaczone_metody.Rozklad()
        self.w2.show()

    def open_oblicz(self):
        if hasattr(self, 'w') and self.w.isVisible():
            self.w.close()

        if hasattr(self, 'w1') and self.w1.isVisible():
            self.w1.close()

        self.w2 = oblicz_nieoznaczone.ObliczNieoznaczona()
        self.w2.show()
        self.close()

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
    ex = Nieoznaczone()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()