from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QWidget, QVBoxLayout
import sys


# Przykładowe okna, które chcemy otworzyć
class WindowOne(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Okno 1")
        self.setGeometry(100, 100, 300, 300)


class WindowTwo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Okno 2")
        self.setGeometry(100, 100, 300, 300)


# Główne okno aplikacji
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Combo Box Demo')
        self.setGeometry(100, 100, 400, 200)
        self.initializeUI()

    def initializeUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout()

        self.comboBox = QComboBox()
        self.comboBox.addItem("Wybierz okno", "none")
        self.comboBox.addItem("Otwórz Okno 1", "window1")
        self.comboBox.addItem("Otwórz Okno 2", "window2")

        # Połączenie sygnału activated z odpowiednim slotem
        self.comboBox.activated.connect(self.openWindow)

        layout.addWidget(self.comboBox)
        self.centralWidget.setLayout(layout)

    def openWindow(self, index):
        if self.comboBox.itemData(index) == "window1":
            self.window = WindowOne()
            self.window.show()
        elif self.comboBox.itemData(index) == "window2":
            self.window = WindowTwo()
            self.window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
