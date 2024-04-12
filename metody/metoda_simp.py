from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QDialog)
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QPixmap, QFont
from obliczenia import oblicz_simpson
from wykresy import wykres_metoda_simp


class MetodaSimp(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(qtg.QIcon('zdjecia/icon.png'))

        # layouty
        layout_for_buttons = QHBoxLayout()
        layout_horizontal_new = QHBoxLayout()
        layout = QVBoxLayout()

        # czcionka
        font = QFont()
        font.setPointSize(10)

        labels_1 = [
            "<h3>Metoda Simpsona</h3>",
            "Metoda Simpsona inaczej metoda parabol polega na przybliżeniu pola pod krzywą polami figur płaskich.",
            "Podstawą jest przedział całkowania, a bokami są wartości funkcji całkowanej w punktach brzegowych.",
            "W tej metodzie jako przybliżenie stosuje się parabolę."

        ]

        l1 = QLabel("n to liczba przedziałów, a w tym przypadku n=2, więc: ")
        l2 = QLabel("Wtedy wzór możemy zapisać:")
        l3 = QLabel("Przy czym błąd wzoru Simpsona wynosi:")
        l4 = QLabel("gdzie: ")
        l5 = QLabel("Na przedziale [a,b], równomiernie rozmieszczamy węzły x<sub>0</sub>=a, x<sub>2</sub>=b i "
                    "x<sub>1</sub>=a+h, gdzie:  ")

        for text in labels_1:
            label = QLabel(text)
            add_label(label, layout)

        add_label(l5, layout)

        wykres = QPushButton('Pokaż wykres dla metody Simpsona')
        wykres.clicked.connect(self.open_przedzial_simpson)
        layout.addWidget(wykres)
        wykres.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

        add_pic("zdjecia/podprzedzial_h_2.png", layout)

        add_label(l1, layout)

        add_pic("zdjecia/Simpson/przedzial_h_2.png", layout)

        add_label(l2, layout)

        add_pic("zdjecia/Simpson/metoda_simp_wzor.png", layout)

        add_label(l3, layout)

        add_pic("zdjecia/Simpson/metoda_simp_blad.png", layout)

        add_label(l4, layout_horizontal_new)
        add_pic("zdjecia/ksi.png", layout_horizontal_new)
        layout.addLayout(layout_horizontal_new)

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
        self.setWindowTitle('Metoda Simpsona')

    def open_przedzial_simpson(self):
        self.w = wykres_metoda_simp.WykresSimp()
        self.w.show()

    def open_oblicz(self):
        if hasattr(self, 'w') and self.w.isVisible():
            self.w.close()

        self.w2 = oblicz_simpson.ObliczSimpson()
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
