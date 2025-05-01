import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

def mainui():
    # GUI import
    app = QApplication([])

    window = QWidget()
    window.setWindowTitle("PyOCR")
    helloMsg = QLabel("<h1>PyOCR</h1>", parent=window)
    helloMsg.move(60, 15)
    window.show()
    sys.exit(app.exec())
