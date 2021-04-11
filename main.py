import sys
import MainWindow_class
from PyQt5 import QtWidgets
import qdarkstyle
# import seaborn as sns

from PyQt5 import QtCore


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    mw = MainWindow_class.MainWindow()
    sys.exit(app.exec_())


