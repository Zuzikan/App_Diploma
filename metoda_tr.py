from obliczenia import oblicz_trapez
import wykres_metoda_tr
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QHBoxLayout,QSizePolicy, QDialog)
import PyQt5.QtCore as qtc
from PyQt5.QtGui import QPixmap, QFont


class MetodaTr(QDialog):
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
            "<h3>Metoda trapezów</h3>",
            "Metoda prostokątów nie jest zbyt dokładna, ponieważ użyte w niej pola prostokątów ",
            "źle odwzorowują powierzchnię pola pod krzywą.",
            "Lepszą opcja jest podstawienie trapezów zamiast prostokątów o wysokości dx.",
            "Aby przybliżyć sobie metodę trapezów zacznijmy od rozważenia przypadku dla n=1, czyli dla dwóch węzłów. ",
            "Wzór trapezów dla jednego przedziału, gdzie początek przedziału to a, natomiast koniec to b.",
            "Przybliżoną wartość całki wyraża się wzorem:"

        ]

        l1 = QLabel("Błąd tej metody dla jednego przedziału wynosi:")
        l2 = QLabel("gdzie: ")
        l3 = QLabel("Jeśli przedział [a,b] jest duży możemy podzielić go na n segmentów i do każdego z nich "
                    "zastosować metodę trapezów. ")
        l4 = QLabel("Przedział całkowania [a, b] dzielimy na podprzedziały punktami:")
        l5 = QLabel("Przyjmujemy oznaczenie h jako długość przedziału:")
        l6 = QLabel("Więc wzór możemy zapisać:")
        l7 = QLabel("Natomiast błąd tej metody wyraża się wzorem:")
        l8 = QLabel("gdzie: ")

        for text in labels_1:
            label = QLabel(text)
            add_label(label, layout)

        add_pic("zdjecia/Trapezy/metoda_tr_jeden_trapez.png", layout)

        add_label(l1, layout)

        add_pic("zdjecia/Trapezy/metoda_tr_jeden_blad.png", layout)

        add_label(l2, layout_horizontal)
        add_pic("zdjecia/ksi.png", layout_horizontal)
        layout.addLayout(layout_horizontal)

        wykres_kwadrat = QPushButton('Pokaż wykres z jednym trapezem')
        wykres_kwadrat.clicked.connect(self.open_przedzial_trapez)
        layout.addWidget(wykres_kwadrat)
        wykres_kwadrat.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

        add_label(l3, layout)
        add_label(l4, layout)

        add_pic("zdjecia/Prostokaty/metoda_pr_przedzial.png", layout)

        add_label(l5, layout)

        add_pic("zdjecia/podprzedzial_h_2.png", layout)

        add_label(l6, layout)

        add_pic("zdjecia/Trapezy/metoda_tr_wiele_trapezow.png", layout)

        add_label(l7, layout)

        add_pic("zdjecia/Trapezy/metoda_tr_wiele_blad.png", layout)

        add_label(l8, layout_horizontal_new)
        add_pic("zdjecia/ksi.png", layout_horizontal_new)
        layout.addLayout(layout_horizontal_new)

        wykres_kwadraty = QPushButton('Pokaż wykres z wieloma trapezami')
        wykres_kwadraty.clicked.connect(self.open_przedzial_trapezy)
        layout.addWidget(wykres_kwadraty)
        wykres_kwadraty.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

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
        self.setWindowTitle('Metoda trapezów')

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
