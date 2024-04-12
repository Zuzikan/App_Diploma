from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QDialog)
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QPixmap, QFont
from obliczenia import oblicz_regula_3_8
from wykresy import wykres_regula_3_8


class Regula38(QDialog):
    def __init__(self):
        super().__init__()


        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(qtg.QIcon('zdjecia/icon.png'))

        # layouty
        layout_for_buttons = QHBoxLayout()
        layout_horizontal = QHBoxLayout()

        layout = QVBoxLayout()

        # czcionka
        font = QFont()
        font.setPointSize(10)

        labels_1 = [
            "<h3>Reguła 3/8</h3>",
            "Jest to reguła będąca rozwinięciem metody Simpsona. Przybliżenie funkcji podcałkowej wielomianem ",
            "3-go stopnia oraz przybliżone obliczanie pola pod wielomianem. Używamy jej w przypadku",
            ", gdy liczba segmentów jest podzielna przez 3."
        ]

        l1 = QLabel("Na przedziale [a,b], równomiernie rozmieszczamy węzły x<sub>0</sub>=a, x<sub>1</sub>=a+h, "
                    "x<sub>2</sub>=2a+h i x<sub>3</sub>=b, gdzie:")
        l2 = QLabel("n to liczba przedziałów, a w tym przypadku n=3, więc:")
        l3 = QLabel("Zatem:")
        l4 = QLabel("Przy czym błąd wynosi:")

        l5 = QLabel("gdzie: ")

        for text in labels_1:
            label = QLabel(text)
            add_label(label, layout)

        wykres = QPushButton("Pokaż wykres dla reguły 3/8")
        wykres.clicked.connect(self.open_przedzial_regula)
        layout.addWidget(wykres)
        wykres.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

        add_label(l1, layout)

        add_pic("zdjecia/podprzedzial_h_2.png", layout)

        add_label(l2, layout)

        add_pic("zdjecia/Regula_3_8/przedzial_h_3.png", layout)

        add_label(l3, layout)
        add_pic("zdjecia/Regula_3_8/regula_3_8_wzor.png", layout)

        add_label(l4, layout)
        add_pic("zdjecia/Regula_3_8/regula_3_8_blad.png", layout)

        add_label(l5, layout_horizontal)
        add_pic("zdjecia/ksi.png", layout_horizontal)
        layout.addLayout(layout_horizontal)

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
        self.setWindowTitle('Reguła 3/8')

    def open_przedzial_regula(self):
        self.w = wykres_regula_3_8.WykresRegula38()
        self.w.show()

    def open_oblicz(self):
        if hasattr(self, 'w') and self.w.isVisible():
            self.w.close()

        self.w2 = oblicz_regula_3_8.ObliczRegula()
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
