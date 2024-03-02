import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import metoda_pr
import metoda_tr
import metoda_simp
import regula_3_8


class MainWindow(qtw.QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Menu")

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

        self.kwadratura_g_c = qtw.QPushButton("Kwadratura Gaussa-Czebyszewa")
        self.layout().addWidget(self.kwadratura_g_c)
        self.kwadratura_g_c.clicked.connect(self.open_kwadratura_g_c)
        self.kwadratura_g_c.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.kwadratura_g_h = qtw.QPushButton("Kwadratura Gaussa-Hermite'a")
        self.layout().addWidget(self.kwadratura_g_h)
        self.kwadratura_g_h.clicked.connect(self.open_kwadratura_g_h)
        self.kwadratura_g_h.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.metoda_m_c_1 = qtw.QPushButton("Metoda Monte-Carlo 1D")
        self.layout().addWidget(self.metoda_m_c_1)
        self.metoda_m_c_1.clicked.connect(self.open_metoda_m_c_1)
        self.metoda_m_c_1.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.metoda_m_c_2 = qtw.QPushButton("Metoda Monte-Carlo 2D")
        self.layout().addWidget(self.metoda_m_c_2)
        self.metoda_m_c_2.clicked.connect(self.open_metoda_m_c_2)
        self.metoda_m_c_2.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

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
        self.w = regula_3_8.Regula38()
        self.w.show()

    def open_kwadratura_g_c(self):
        self.w = metoda_pr.MetodaPr()
        self.w.show()

    def open_kwadratura_g_h(self):
        self.w = metoda_pr.MetodaPr()
        self.w.show()

    def open_metoda_m_c_1(self):
        self.w = metoda_pr.MetodaPr()
        self.w.show()

    def open_metoda_m_c_2(self):
        self.w = metoda_pr.MetodaPr()
        self.w.show()


if __name__ == "__main__":
    app = qtw.QApplication([])

    appFont = qtg.QFont()
    appFont.setPointSize(10)  # Adjust application-wide font size as needed
    app.setFont(appFont)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
