import wykres_m_c
from obliczenia import oblicz_monte
from obliczenia import oblicz_monte2D
import wykres_metoda_tr
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QDialog)
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QPixmap, QFont


class MetodaMonte(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(qtg.QIcon('zdjecia/icon.png'))

        # layouty
        layout_for_buttons = QHBoxLayout()
        layout_monte_2 = QHBoxLayout()
        layout = QVBoxLayout()

        # czcionka
        font = QFont()
        font.setPointSize(10)

        labels_1 = [
            "<h3>Metoda Monte Carlo 1D i 2D</h3>",
            "Metoda Monte Carlo jest stosowana do szacowania wartości całek oznaczonych. Jest szczególnie przydatna w "
            "przypadku funkcji trudnych",
            "do całkowania analitycznego lub gdy całka jest wielowymiarowa. Przykładem ilustrującym zastosowanie "
            "metody Monte Carlo",
            "jest problem oszacowania powierzchni stawu o nieregularnym kształcie. Kamienie są rzucane w taki sposób,",
            "aby wylądowały w losowym miejscu w obrębie wyznaczonego obszaru zawierającego staw. ",
            "Liczymy ile kamieni wpadło do wody, a ile na ląd. Szacowanym polem powierzchni stawu jest pole "
            "wyznaczonego obszaru",
            " pomnożone przez ułamek kamieni które wpadły do wody. Jest ona nazywana „hit or miss method”."

        ]


        l1 = QLabel("gdzie n<sub>s</sub> to ilość kamieni, które wpadły do wody, a n to ilość kamieni rzuconych.")
        l2 = QLabel("Kolejny sposób opiera się na średniej wartości rachunku całkowego. Całkę oznaczoną:")

        l4 = QLabel("wyznacza się przez średnią wartość całki f(x) z zakresu a≤x≤b. Aby wyznaczyć średnią, "
                    "losowo wybieramy próbki x<sub>i</sub>. ")
        l5 = QLabel("Dla całki jednowymiarowej (1D) F oszacowanie za pomocą metody średniej wartości wyraża wzór:")
        l6 = QLabel("gdzie n jest liczbą próbek. Większa liczba próbek oznacza większą dokładność wyniku.")
        l8 = QLabel("Mamy daną powierzchnię A. Losowo wybieramy punkty n o współrzędnych (x<sub>i</sub>, "
                    "y<sub>i</sub>) znajdujące się w obrębie naszej powierzchni. Wtedy możemy zapisać:")

        l9 = QLabel("gdzie n jest liczbą próbek. ")
        l10 = QLabel("Funkcja H (Heaviside) H(x,y)=1 jeśli (x,y) znajduje się w obrębie naszej powierzchni.")
        l11 = QLabel("Metoda Monte Carlo 2D jest stosowana do obliczenia całek podwójnych lub rozwiązywania problemów w "
            "dwuwymiarowych przestrzeniach.")
        l12 = QLabel("Tak samo jak 1D opiera się ona na losowych próbkach, jednak tym razem w dwóch wymiarach. Przyjmijmy całkę oznaczoną dwuwymiarową jako:")

        for text in labels_1:
            label = QLabel(text)
            add_label(label, layout)
        add_pic("zdjecia/Monte/Fn.png", layout)
        add_label(l1, layout)

        wykres_monte_1_hom = QPushButton("Pokaż wykres dla metody Monte Carlo 1D 'hit or miss'")
        wykres_monte_1_hom.clicked.connect(self.open_wykres_monte_1_hom)
        layout.addWidget(wykres_monte_1_hom)
        wykres_monte_1_hom.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

        add_label(l2, layout)
        add_pic("zdjecia/Monte/F.png", layout)
        add_label(l4, layout)


        add_label(l5, layout)

        add_pic("zdjecia/Monte/Fn2.png", layout)
        add_label(l6, layout)

        wykres_monte_1_ws = QPushButton("Pokaż wykres dla metody Monte Carlo 1D 'średniej wartości'")
        wykres_monte_1_ws.clicked.connect(self.open_wykres_monte_1_ws)
        layout.addWidget(wykres_monte_1_ws)
        wykres_monte_1_ws.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

        add_label(l11, layout)

        add_label(l12, layout)
        add_pic("zdjecia/Monte/F2.png", layout)
        add_label(l8, layout)
        add_pic("zdjecia/Monte/Fk.png", layout)
        add_label(l9, layout)
        add_label(l10, layout)

        wykres_monte_2_hom = QPushButton("Pokaż wykres dla metody Monte Carlo 2D 'hit or miss'")
        wykres_monte_2_hom.clicked.connect(self.open_wykres_monte_2_hom)
        layout_monte_2.addWidget(wykres_monte_2_hom)
        wykres_monte_2_hom.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

        wykres_monte_2_ws = QPushButton("Pokaż wykres dla metody Monte Carlo 2D 'średniej wartości'")
        wykres_monte_2_ws.clicked.connect(self.open_wykres_monte_2_ws)
        layout_monte_2.addWidget(wykres_monte_2_ws)
        wykres_monte_2_ws.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        add_label(QLabel(""), layout)

        layout.addLayout(layout_monte_2)
        add_label(QLabel(""), layout)

        zamknij = QPushButton('Zamknij program')
        zamknij_okno = QPushButton("Zamknij okno")
        obliczenia = QPushButton('Przejdź do obliczeń dla 1D')
        obliczenia2 = QPushButton('Przejdź do obliczeń dla 2D')

        obliczenia.clicked.connect(self.open_oblicz)
        obliczenia2.clicked.connect(self.open_oblicz2)
        zamknij_okno.clicked.connect(self.close)
        zamknij.clicked.connect(qtc.QCoreApplication.instance().quit)

        zamknij.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        zamknij_okno.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        obliczenia.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        obliczenia2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        zamknij.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")
        zamknij_okno.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")
        obliczenia.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        obliczenia2.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

        layout_for_buttons.addWidget(zamknij)
        layout_for_buttons.addWidget(zamknij_okno)
        layout_for_buttons.addWidget(obliczenia)
        layout_for_buttons.addWidget(obliczenia2)
        layout.addLayout(layout_for_buttons)

        self.setLayout(layout)
        self.setWindowTitle('Metoda Monte Carlo 1D i 2D')

    def open_wykres_monte_1_hom(self):
        self.w = wykres_m_c.WykresMC1HOM()
        self.w.show()

    def open_wykres_monte_1_ws(self):
        self.w1 = wykres_m_c.WykresMC1WS()
        self.w1.show()

    def open_wykres_monte_2_hom(self):
        self.w2 = wykres_m_c.WykresMC2HOM()
        self.w2.show()

    def open_wykres_monte_2_ws(self):
        self.w3 = wykres_m_c.WykresMC2WS()
        self.w3.show()

    def open_oblicz(self):
        if hasattr(self, 'w') and self.w.isVisible():
            self.w.close()

        if hasattr(self, 'w1') and self.w1.isVisible():
            self.w1.close()

        self.w2 = oblicz_monte.ObliczMonte()
        self.w2.show()
        self.close()

    def open_oblicz2(self):
        if hasattr(self, 'w') and self.w.isVisible():
            self.w.close()

        if hasattr(self, 'w1') and self.w1.isVisible():
            self.w1.close()

        self.w2 = oblicz_monte2D.ObliczMonte2()
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
