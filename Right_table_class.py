
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



class Right_Table_Widget(QWidget):

    signal_for_ml_widget = pyqtSignal(str)

    def __init__(self):
        print('subwindow init')
        super(Right_Table_Widget, self).__init__()


        self.main_layout = QVBoxLayout(self)

        self.table = Right_Table(10,10)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(' labelllllllllllllllllllll ')


        self.b_predict = QPushButton(self)
        self.b_predict.setText('predict')
        self.b_predict.clicked.connect(self.predict)

        self.main_layout.addWidget(self.table)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.b_predict)


        # Sygnały
        # self.procStart.connect(self.ml_widget.on_procStart)

        self.show()

    # ======================= SIGNALS ==============================

    @pyqtSlot()
    def emit_signal_for_ml_widget(self):
        self.signal_for_ml_widget.emit('hasło od right table')

    @pyqtSlot(list)
    def get_signal_for_ml_widget(self, parameters):
        print("From ML WIDGET:  ", parameters)
        self.raise_()

    # ======================= METHODS ==============================

    def predict(self):
        self.emit_signal_for_ml_widget()

    def is_visible(self):
        return self.is_visible()





class Right_Table(QTableWidget):
    def __init__(self, r ,c ):
        super().__init__(r,c)
        self.rows = r
        self.columns = c


