import oblicz_trapez
import wykres_metoda_tr
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QHBoxLayout,QSizePolicy, QDialog)
import PyQt5.QtCore as qtc
from PyQt5.QtGui import QPixmap, QFont


class MetodaCzeb(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        # layouty
        layout_for_buttons = QHBoxLayout()
        layout = QVBoxLayout()

        # czcionka
        font = QFont()
        font.setPointSize(10)

        labels_1 = [
            "<h3>Kwadratura Gaussa-Czebyszewa</h3>",
            "W tej metodzie jako wielomiany ortogonalne  wykorzystywane są wielomiany Czebyszewa. ",
            "Natomiast wielomiany ortogonalne to sekwencja wielomianów, które są ortogonalne względem ",
            "pewnego iloczynu skalarnego.",
            "Kwadratura jest szczególnie efektywna przy całkowaniu funkcji z dużą osobliwością  w ",
            "punktach końcowych przedziału, to znaczy gdy funkcja doświadcza silnej zmienności w tych punktach. "

        ]

        l1 = QLabel("Wielomiany ortogonalne Czebyszewa są postaci:")
        l2 = QLabel("Jest to jeden z czterech najczęściej używanych rodzajów wielomianów ortogonalnych, które są ")
        l2c =QLabel("związane z odpowiadającymi im kwadraturami Gaussa.")
        l4 = QLabel("Funkcja wagowa, czyli 'waga' wkładu poszczególnych części przedziału całkowania, dla tych wielomianów to:")
        l5 = QLabel("a przedział całkowania [-1,1].")
        l6 = QLabel("Całkę poniżej możemy przybliżać kwadraturami Gaussa-Czebyszewa:")
        l7 = QLabel("w której węzły x<sub>i</sub> są pierwiastkami wielomianu ortogonalnego Czebyszewa stopnia (n+1), ")
        l7c =QLabel("a wartości A<sub>i</sub> są odpowiadającymi im współczynnikami.")
        l8 = QLabel("Wartości węzłów i współczynników dla kwadratur Gaussa-Czebyszewa wyraża się wzorami:")
        l9 = QLabel("")

        for text in labels_1:
            label = QLabel(text)
            add_label(label, layout)

        add_label(l1, layout)

        add_pic("zdjecia/Czebyszew/wielomiany.png", layout)
        add_label(QLabel(""), layout)
        add_label(l2, layout)
        add_label(l2c, layout)
        add_label(l4, layout)

        add_pic("zdjecia/Czebyszew/funkcja_w.png", layout)
        add_label(l5, layout)
        add_label(QLabel(""), layout)
        add_label(l6, layout)
        add_pic("zdjecia/Czebyszew/kwadratura.png", layout)
        add_label(l7, layout)
        add_label(l7c, layout)
        add_label(l8, layout)
        add_pic("zdjecia/Czebyszew/wzory.png", layout)
        add_label(QLabel(""), layout)

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
        self.setWindowTitle('Kwadratura Gaussa-Czebyszewa')

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

        self.w2 = oblicz_trapez.ObliczTrapezy()
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
