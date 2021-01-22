import sys
from MainWindow_class import MainWindow
from PyQt5 import QtWidgets
import qdarkstyle


import seaborn as sns

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    mw = MainWindow()
    sys.exit(app.exec_())


