import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QComboBox, QLineEdit, QSlider, QHBoxLayout,
                             QPushButton, QDialog)
from PyQt5.QtGui import QIntValidator
from sympy import sympify, simplify


class Oblicz(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        sliderLayout = QHBoxLayout()
        abHorizontal = QHBoxLayout()
        nodeHorizontal = QHBoxLayout()

        combo = QComboBox(self)
        combo.addItems(["Page 1", "Page 2"])
        l1 = QLabel("Porównaj z: ", self)
        l2 = QLabel("Wpisz równanie: ", self)
        l3 = QLabel("Podaj przedział [a,b]:", self)
        self.rownanie = QLineEdit(self)
        instrukcja = QPushButton('Instrukcja', self)
        la = QLabel("a: ", self)
        lb = QLabel("b:", self)
        self.a = QLineEdit(self)
        self.b = QLineEdit(self)
        # l5 = QLabel("n: ", self)
        l6 = QLabel("Wynik: ", self)
        slider = QSlider(Qt.Horizontal, self)
        slider.setMinimum(2)
        slider.setMaximum(50)
        slider.setValue(2)
        start = QLabel('2')
        end = QLabel('50')
        oblicz = QPushButton('Oblicz', self)
        self.wartosc = QLabel("Liczba node'ów: 2", self)

        slider.valueChanged.connect(self.silder_wartosc)
        instrukcja.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        oblicz.setStyleSheet("border-radius : 5px; background-color : #CCDDFF")
        slider.setStyleSheet("""
                QSlider::handle:horizontal {
                    background: #333;
                    border: 1px solid #555;
                    width: 8px;
                    height: 8px;
                    margin: -8px 0;  
                    border-radius:4px;  
                }
                """)
        self.a.setPlaceholderText("Wpisz wartość a")
        self.b.setPlaceholderText("Wpisz wartość b")
        self.a.setValidator(QIntValidator())
        self.b.setValidator(QIntValidator())
        self.rownanie.setPlaceholderText("Wpisz wartość całki")
        l3.setAlignment(Qt.AlignCenter)
        self.wartosc.setAlignment(Qt.AlignCenter)

        # Connect the combo box's signal to the slot
        # self.combo.activated[str].connect(self.onActivated)
        layout.addWidget(l1, 0, 0)
        layout.addWidget(combo, 0, 1)

        layout.addWidget(l2, 1, 0)
        layout.addWidget(self.rownanie, 1, 1)
        layout.addWidget(instrukcja, 2, 0, 1, 2)

        layout.addWidget(l3, 3, 0, 1, 2)

        abHorizontal.addWidget(la)
        abHorizontal.addWidget(self.a)

        abHorizontal.addWidget(lb)
        abHorizontal.addWidget(self.b)

        layout.addLayout(abHorizontal, 4, 0, 1, 2)

        layout.addWidget(oblicz, 5, 0, 1, 2)
        eq = self.parser()
        oblicz.clicked.connect(self.metoda_prostokatow(2))

        layout.addWidget(self.wartosc, 6, 0, 1, 2)

        sliderLayout.addWidget(start)
        sliderLayout.addWidget(slider)
        sliderLayout.addWidget(end)

        sliderLayout.setStretch(0, 1)
        sliderLayout.setStretch(1, 50)
        sliderLayout.setStretch(2, 1)

        layout.addLayout(sliderLayout, 7, 0, 1, 2)

        layout.addWidget(l6, 7, 3, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle('Oblicz')

    def onActivated(self, text):
        self.label.setText(f"You selected: {text}")
        self.label.adjustSize()

    def silder_wartosc(self, value):
        self.wartosc.setText(f"Liczba node'ów: {value}")

    def parser(self):
        rownanie_string = self.rownanie.text()
        a = self.a.text()
        b = self.b.text()
        ap = simplify(a)
        bp = simplify(b)
        rownanie_matematyczne = sympify(rownanie_string)
        return rownanie_matematyczne, ap,bp

    def metoda_prostokatow(self, n):
        eq, a, b = self.parser()
        h = (b - a) / n
        wynik = 0
        for i in range(n):
            wysokosc = eq(a + i * h)
            wynik += wysokosc * h

        self.l6.setText(f"Wynik: {wynik}")


def main():
    app = QApplication(sys.argv)
    ex = Oblicz()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
