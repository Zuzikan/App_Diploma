import oblicz_boole
import oblicz_trapez
import wykres_metoda_tr
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QHBoxLayout,QSizePolicy, QDialog)
import PyQt5.QtCore as qtc
from PyQt5.QtGui import QPixmap, QFont


class MetodaBoole(QDialog):
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

            "Złożona metoda Boole’a (Composite Boole’s Rule) jest ulepszeniem prostej metody. Przedział [x<sub>0</sub>,x<sub>4</sub>] ",
            "możemy podzielić na małe podprzedziały o szerokości 4h i dla każdego z nich zastosować regułę Boole’a. ",
            "Suma pól wszystkich podprzedziałów jest całką przedziału [x<sub>0</sub>,x<sub>4</sub>]. ",
            "Mimo tego, że jest to metoda bardziej pracochłonna, oferuje większą precyzję i elastyczność."

        ]

        l1 = QLabel("<h3>Metoda Boole'a</h3>")
        l2 = QLabel("Polega na przybliżeniu całki f(x) w przedziale [x<sub>0</sub>,x<sub>4</sub>], czyli n=4, a liczba punktów to 5.")
        l3 = QLabel("gdzie: ")
        l4 = QLabel("Jest to wzór prostej metody Boole’a (Simple Boole’s Rule). ")
        l5 = QLabel("")


        add_label(l1, layout)
        add_label(l2, layout)
        add_pic("zdjecia/Boole/boole_1.png", layout)
        add_label(l3, layout)
        add_pic("zdjecia/Boole/boole_2.png", layout)
        add_label(l4, layout)
        for text in labels_1:
            label = QLabel(text)
            add_label(label, layout)

        add_pic("zdjecia/Boole/boole_3.png", layout)


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
        self.setWindowTitle("Metoda Boole'a")

    def open_przedzial_trapez(self):
        self.w = wykres_metoda_tr.WykresTrapez()
        self.w.show()

    def open_przedzial_trapezy(self):
        self.w1 = wykres_metoda_tr.WykresTrapezy()
        self.w1.show()

    def open_oblicz(self):
        if hasattr(self, 'w') and self.w.isVisible():
            self.w.close()

        if hasattr(self, 'w1') and self.w1.isVisible():
            self.w1.close()

        self.w2 = oblicz_boole.ObliczBoole()
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
