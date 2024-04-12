from obliczenia import oblicz_metoda_prostokatow
from wykresy import wykres_metoda_pr
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QDialog)
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QPixmap, QFont


class MetodaPr(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(qtg.QIcon('zdjecia/icon.png'))

        # layouty
        layout_for_buttons = QHBoxLayout()
        layout_horizontal = QHBoxLayout()
        layout_horizontal_new = QHBoxLayout()
        layout = QVBoxLayout()

        # czcionka
        font = QFont()
        font.setPointSize(10)

        labels_1 = [
            "<h3>Metoda prostokątów</h3>",
            "<p>Metoda prostokątów polega na przybliżeniu obszaru ograniczonego wykresem funkcji poprzez wstawianie"
            "</p>",
            "w ten obszar prostokątów o podstawie równej długości kroku całkowania i wysokości równej wartości",
            "funkcji w przedziale określonym przez punkt całkowania.",
            "Jest to jedna z najprostszych metod całkowania numerycznego, która zastępuje funkcję stałą wartością "
            "równą",
            "wartości funkcji w środku przedziału całkowania.",
            "Przybliżoną wartość całki wyraża się wzorem:"
        ]
        labels_2 = [

            "Gdzie n to liczba przedziałów, które chcemy uzyskać mając na uwadze, że podczas wzrostu wartości n "
            "długość",
            "przedziału powinna maleć. W każdym z takich przedziałów umieszczamy prostokąt, którego jednym bokiem "
            "będzie",
            "długość podprzedziału (szerokość), a drugim wartość zależna od wartości funkcji (wysokość) f(x).",
            "Przyjmujemy oznaczenie h jako długość przedziału:"


        ]

        l1 = QLabel("Jeśli funkcja podcałkowa nie jest wielomianem stopnia co najmniej pierwszego, błąd wynosi:")
        l2 = QLabel("gdzie: ")
        l3 = QLabel("Przedział podcałkowy możemy podzielić na podprzedziały i do każdego z nich zastosować tę metodę.")
        l4 = QLabel("Przedział całkowania [a, b] dzielimy na podprzedziały punktami:")
        l5 = QLabel("Więc wzór możemy zapisać:")
        l6 = QLabel("Natomiast błąd tej metody wyraża się wzorem:")
        l7 = QLabel("gdzie: ")

        for text in labels_1:
            label = QLabel(text)
            add_label(label, layout)

        add_pic("zdjecia/Prostokaty/metoda_pr_jeden_kwadrat.png", layout)

        add_label(l1, layout)

        add_pic("zdjecia/Prostokaty/metoda_pr_jeden_blad.png", layout)

        add_label(l2, layout_horizontal)
        add_pic("zdjecia/Prostokaty/eta_1.png", layout_horizontal)
        layout.addLayout(layout_horizontal)

        wykres_kwadrat = QPushButton('Pokaż wykres dla metody prostokątów z jednym kwadratem')
        wykres_kwadrat.clicked.connect(self.open_przedzial_kwadrat)
        layout.addWidget(wykres_kwadrat)
        wykres_kwadrat.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")

        add_label(l3, layout)
        add_label(l4, layout)

        add_pic("zdjecia/Prostokaty/metoda_pr_przedzial.png", layout)

        for text in labels_2:
            label = QLabel(text)
            add_label(label, layout)

        add_pic("zdjecia/podprzedzial_h.png", layout)

        add_label(l5, layout)

        add_pic("zdjecia/Prostokaty/metoda_pr_wiele_kwadratow.png", layout)

        add_label(l6, layout)

        add_pic("zdjecia/Prostokaty/metoda_pr_wiele_blad.png", layout)

        add_label(l7, layout_horizontal_new)
        add_pic("zdjecia/Prostokaty/eta_1.png", layout_horizontal_new)
        layout.addLayout(layout_horizontal_new)

        wykres_kwadraty = QPushButton('Pokaż wykres dla metody prostokątów z wieloma kwadratami')
        wykres_kwadraty.clicked.connect(self.open_przedzial_kwadraty)
        layout.addWidget(wykres_kwadraty)
        wykres_kwadraty.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
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
        self.setWindowTitle('Metoda prostokątów')

    def open_przedzial_kwadrat(self):
        self.w = wykres_metoda_pr.WykresKwadrat()
        self.w.show()

    def open_przedzial_kwadraty(self):
        self.w1 = wykres_metoda_pr.WykresKwadraty()
        self.w1.show()

    def open_oblicz(self):
        if hasattr(self, 'w') and self.w.isVisible():
            self.w.close()

        if hasattr(self, 'w1') and self.w1.isVisible():
            self.w1.close()

        self.w2 = oblicz_metoda_prostokatow.Oblicz()
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
