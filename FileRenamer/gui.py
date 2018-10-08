import sys

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton


class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont("SansSerif", 10))

        self.setToolTip("This is <b>QWidget</b> widget")

        btn = QPushButton("Button", self)
        btn.setToolTip("Qpushbutton")
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle("Icon")
        self.setWindowIcon(QIcon("1.jpg"))

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())
