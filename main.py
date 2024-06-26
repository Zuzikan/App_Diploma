import sys
import os
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

sys.path.append('metody')
from metody import (metoda_czeb, metoda_herm, metoda_monte, metoda_pr, metoda_tr, metoda_simp, nieoznaczone,
                    regula_3_8, metoda_boolea)

sys.path.append('wykresy')
sys.path.append('obliczenia')
sys.path.append('zdjecia')


class MainWindow(qtw.QDialog):
    def __init__(self):
        super().__init__()

        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.p5 = None
        self.p6 = None
        self.p7 = None
        self.p8 = None
        self.p10 = None
        self.nieoznaczone = None
        self.zamknij = None
        self.metoda_m_c = None
        self.kwadratura_g_h = None
        self.kwadratura_g_c = None
        self.regula_3_8 = None
        self.metoda_boole = None
        self.metoda_simp = None
        self.metoda_tr = None
        self.metoda_pr = None
        self.intro = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Menu")
        self.setWindowIcon(qtg.QIcon('zdjecia/icon.png'))

        self.setLayout(qtw.QVBoxLayout())
        self.intro = qtw.QLabel("<h3>Wybierz metodę</h3>")
        self.layout().addWidget(self.intro)
        self.intro.setAlignment(qtc.Qt.AlignCenter)

        self.metoda_pr = qtw.QPushButton("Metoda prostokątów")
        self.layout().addWidget(self.metoda_pr)
        self.metoda_pr.clicked.connect(self.open_metoda_pr)
        self.metoda_pr.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.metoda_tr = qtw.QPushButton("Metoda trapezów")
        self.layout().addWidget(self.metoda_tr)
        self.metoda_tr.clicked.connect(self.open_metoda_tr)
        self.metoda_tr.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.metoda_simp = qtw.QPushButton("Metoda Simpsona")
        self.layout().addWidget(self.metoda_simp)
        self.metoda_simp.clicked.connect(self.open_metoda_simp)
        self.metoda_simp.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.regula_3_8 = qtw.QPushButton("Reguła 3/8")
        self.layout().addWidget(self.regula_3_8)
        self.regula_3_8.clicked.connect(self.open_regula_3_8)
        self.regula_3_8.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.metoda_boole = qtw.QPushButton("Metoda Boole'a")
        self.layout().addWidget(self.metoda_boole)
        self.metoda_boole.clicked.connect(self.open_metoda_boole)
        self.metoda_boole.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.kwadratura_g_c = qtw.QPushButton("Kwadratura Gaussa-Czebyszewa")
        self.layout().addWidget(self.kwadratura_g_c)
        self.kwadratura_g_c.clicked.connect(self.open_kwadratura_g_c)
        self.kwadratura_g_c.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.kwadratura_g_h = qtw.QPushButton("Kwadratura Gaussa-Hermite'a")
        self.layout().addWidget(self.kwadratura_g_h)
        self.kwadratura_g_h.clicked.connect(self.open_kwadratura_g_h)
        self.kwadratura_g_h.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.metoda_m_c = qtw.QPushButton("Metoda Monte Carlo 1D i 2D")
        self.layout().addWidget(self.metoda_m_c)
        self.metoda_m_c.clicked.connect(self.open_metoda_m_c)
        self.metoda_m_c.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.nieoznaczone = qtw.QPushButton("Całki nieoznaczone")
        self.layout().addWidget(self.nieoznaczone)
        self.nieoznaczone.clicked.connect(self.open_nieoznaczone)
        self.nieoznaczone.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.nieoznaczone.setStyleSheet("border-radius : 3px; background-color : #E1D9E2")

        self.zamknij = qtw.QPushButton('Zamknij')
        self.layout().addWidget(self.zamknij)
        self.zamknij.move(50, 50)
        self.zamknij.resize(self.zamknij.sizeHint())
        self.zamknij.clicked.connect(qtc.QCoreApplication.instance().quit)
        self.zamknij.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.zamknij.setStyleSheet("border-radius : 5px; background-color : #FCDDDD")

    def open_metoda_pr(self):
        self.p1 = metoda_pr.MetodaPr()
        self.p1.show()

    def open_metoda_tr(self):
        self.p2 = metoda_tr.MetodaTr()
        self.p2.show()

    def open_metoda_simp(self):
        self.p3 = metoda_simp.MetodaSimp()
        self.p3.show()

    def open_regula_3_8(self):
        self.p4 = regula_3_8.Regula38()
        self.p4.show()

    def open_metoda_boole(self):
        self.p5 = metoda_boolea.MetodaBoole()
        self.p5.show()

    def open_kwadratura_g_c(self):
        self.p6 = metoda_czeb.MetodaCzeb()
        self.p6.show()

    def open_kwadratura_g_h(self):
        self.p7 = metoda_herm.MetodaHerm()
        self.p7.show()

    def open_metoda_m_c(self):
        self.p8 = metoda_monte.MetodaMonte()
        self.p8.show()

    def open_nieoznaczone(self):
        self.p10 = nieoznaczone.Nieoznaczone()
        self.p10.show()


def main():
    app = qtw.QApplication([])

    appFont = qtg.QFont()
    appFont.setPointSize(10)
    app.setFont(appFont)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
