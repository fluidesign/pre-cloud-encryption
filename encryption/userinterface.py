# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('app.png'))

        self.show()


if __name__ == "__main__":
    # allowed just for testing
    ui = QApplication(sys.argv) #  creating an UI object
    main_window = MainWindow()
    sys.exit(ui.exec_()) # starting the UI inside the sys.exit to ensuse a clean exit
else:
    print("Imported")
    # should be here next