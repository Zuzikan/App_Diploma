from obliczenia import oblicz_herm
import wykres_metoda_tr
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QDialog)
import PyQt5.QtCore as qtc
from PyQt5.QtGui import QPixmap, QFont


class MetodaHerm(QDialog):
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
            "<h3>Kwadratura Gaussa-Hermite'a</h3>",
            "W kwadraturze Gaussa-Hermite’a przedział całkowania jest nieskończony co wyróżnia ją spośród innych ",
            "kwadratur Gaussa. Kwadratura ta umożliwia dokładne przybliżenie całki przy użyciu niewielkiej liczby ",
            "punktów. W tej metodzie jako wielomiany ortogonalne wykorzystywane są wielomiany Hermite’a."

        ]

        l1 = QLabel("Wielomiany ortogonalne Hermite’a mają postać:")
        l2 = QLabel("Funkcja wagowa, czyli 'waga' wkładu poszczególnych części przedziału całkowania, dla tych "
                    "wielomianów to:")

        l4 = QLabel("a przedział całkowania (-∞,∞).")
        l5 = QLabel("Zatem całkę poniżej można przybliżyć za pomocą kwadratur Gaussa-Hermite’a:")
        l6 = QLabel("W tych kwadraturach węzły x<sub>i</sub> są pierwiastkami wielomianu ortogonalnego Hermite’a "
                    "stopnia (n+1),")
        l6c = QLabel("a wartości A<sub>i</sub> odpowiadającymi im współczynnikami. W poniższej tabeli przedstawiono ")
        l6cc=QLabel("wartości współczynników dla wielomianów stopnia 1-4.")


        for text in labels_1:
            label = QLabel(text)
            add_label(label, layout)

        add_label(l1, layout)

        add_pic("zdjecia/Hermit/wielomiany_orto.png", layout)

        add_label(l2, layout)
        add_pic("zdjecia/Hermit/wagowa.png", layout)
        add_label(l4, layout)


        add_label(l5, layout)


        add_pic("zdjecia/Hermit/calka.png", layout)

        add_label(l6, layout)
        add_label(l6c, layout)
        add_label(l6cc, layout)
        add_label(QLabel(""), layout)
        add_pic("zdjecia/Hermit/tabela.png", layout)
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

        self.w2 = oblicz_herm.ObliczHerm()
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
