import sys
from MainWindow_class import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = MainWindow()
    sys.exit(app.exec_())
