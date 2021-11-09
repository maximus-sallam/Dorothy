from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(640, 480, 320, 240)
    win.setWindowTitle("Maximus Virus")

    label = QtWidgets.QLabel(win)
    label.setText("Your computer has now been infected with the Maximus virus")
    label.move(10, 100)
    label.adjustSize()

    win.show()
    sys.exit(app.exec_())


window()
