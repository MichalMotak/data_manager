from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Tab1(QWidget):
    def __init__(self):
        super(Tab1, self).__init__()

        self.layout = QVBoxLayout()
        self.height, self.width,  = 100,100
        self.pushButton2 = QPushButton(self)
        self.pushButton2.setGeometry(QRect(50, 50, 80, 20))
        self.pushButton2.setText('tab1')
        # self.pushButton2.clicked.connect(self.create_database)
        self.layout.addWidget(self.pushButton2)

        self.setLayout(self.layout)


        self.x1 = 3

class Tab2(QWidget):
    def __init__(self):
        super(Tab2, self).__init__()

        self.layout = QVBoxLayout()
        self.height, self.width,  = 100,100
        self.pushButton2 = QPushButton(self)
        self.pushButton2.setGeometry(QRect(50, 50, 80, 20))
        self.pushButton2.setText('tab2')
        # self.pushButton2.clicked.connect(self.create_database)
        self.layout.addWidget(self.pushButton2)

        self.setLayout(self.layout)


        self.x1 = 3



class MLWidget(QWidget):
    def __init__(self):
        print('subwindow init')
        QWidget.__init__(self)
        self.left, self.top =  300, 200
        self.width, self.height = 500, 200
        self.UI()

    def UI(self):
        print('ml widget createed')


        # self.pushButton3 = QPushButton(self)
        # self.pushButton3.setGeometry(QRect(10,10, 80, 20))
        # self.pushButton3.setText('ML Button')

        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget(self)


        self.tab1 = Tab1()
        self.tab2 = Tab2()

        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        self.layout.addWidget(self.tabs)

        self.show()

