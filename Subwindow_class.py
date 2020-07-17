# from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import  QLineEdit, QWidget, QTableWidget,QVBoxLayout, QLabel, QComboBox, QApplication, QMainWindow, \
                            QTableWidgetItem, QPushButton, QLineEdit, QFrame, QGridLayout
from PyQt5 import QtCore




from Database_class import Database

class Subwindow_Database(QMainWindow):
    def __init__(self, parent):
        print('subwindow init')
        QWidget.__init__(self)
        self.left, self.top =  300, 200
        self.width, self.height = 500, 200

        self.title = "SQL Manager"
        self.mw = parent
        self.UI()

    def UI(self):
        print('iniui child')
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.main_layout = QVBoxLayout(self)

        self.layout = QGridLayout()
        # self.layout = QVBoxLayout()
        self.frame = QFrame()
        self.frame.setLayout(self.layout)


        self.label1 = QLabel(self)
        self.label1.setText('Local host')
        # self.label1.setFixedSize(80, 30)

        self.label2 = QLabel(self)
        self.label2.setText('user')

        self.label3 = QLabel(self)
        self.label3.setText('passwd')

        self.label4 = QLabel(self)
        self.label4.setText('database')

        self.line1 = QLineEdit(self)
        self.line1.setText('localhost')
        self.line2 = QLineEdit(self)
        self.line2.setText('root')
        self.line3 = QLineEdit(self)
        self.line3.setText('root')
        self.line4 = QLineEdit(self)
        self.line4.setText('sql_store')


        self.layout.addWidget(self.label1, 0, 1)
        self.layout.addWidget(self.label2, 0, 2)
        self.layout.addWidget(self.label3, 0, 3)
        self.layout.addWidget(self.label4, 0, 4)

        self.layout.addWidget(self.line1, 1, 1)
        self.layout.addWidget(self.line2, 1, 2)
        self.layout.addWidget(self.line3, 1, 3)
        self.layout.addWidget(self.line4, 1, 4)



        self.layout2 = QVBoxLayout()
        self.frame2 = QFrame()
        self.frame2.setLayout(self.layout2)
        #
        self.b_update_table = QPushButton('show database', self)
        # self.b_update_table.setGeometry(QRect(0, 0, 100, 30))
        self.b_update_table.clicked.connect(lambda: self.update_table())
        # self.b_update_table.setFixedSize(120, 30)

        self.b_create_db = QPushButton('create database', self)
        # self.b_load_db.setGeometry(QRect(200, 200, 100, 30))
        self.b_create_db.clicked.connect(lambda: self.create_database())
        # self.b_create_db.setFixedSize(120, 30)
        # self.b_create_db.setAlignment(QtCore.Qt.AlignCenter)


        self.l_com_line = QLabel(self)
        self.l_com_line.setText('Command line')
        self.el_com_line = QLineEdit(self)
        # self.line.setGeometry(QRect(50, 50, 300, 50))
        self.el_com_line.setText('SELECT * FROM customers')
        # self.el_com_line.setFixedSize(500,100)

        self.layout2.addWidget(self.l_com_line)
        self.layout2.addWidget(self.el_com_line)
        self.layout2.addWidget(self.b_create_db)
        self.layout2.addWidget(self.b_update_table)


        self.main_layout.addWidget(self.frame)
        self.main_layout.addWidget(self.frame2)



        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)

        self.setCentralWidget(self.widget)

        self.setFixedSize(self.size())
        self.show()

    def update_table(self):
        print('update table')
        text = self.el_com_line.text()
        print(text)
        self.database.add_command(text)
        self.database.db_show_data()
        self.database.set_col_labels()


    def create_database(self):

        # zbieramy info, logujemy sie
        host = self.line1.text()
        user = self.line2.text()
        passwd = self.line3.text()
        database = self.line4.text()
        print(host,user,passwd,database)

        self.database = Database(self.mw.table, host=host, user=user,
                                 passwd=passwd, database=database)

        # self.database.db_show_data()
        # col = self.database.get_db_column_names()
        # print(col)
        # self.mw.table.set_column_labels(col)


