import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QSplitter, QGridLayout, QAction, QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QPushButton, QFileDialog
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
import mysql.connector as sql

from Database_class import Database
from Subwindow_class import Subwindow

import csv

from MyTable_class import MyTable
from PlotCanvas_class import PlotCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.left, self.top  = 100, 100
        self.height, self.width,  = 500, 1200

        self.UI()
        self.show()

    def UI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table = MyTable(self, 10, 5)
        # layout = QGridLayout(self)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        # self.setCentralWidget(self.table)
        self.canv = PlotCanvas(self.table, 5,3)



        # self.pushButton2 = QPushButton(self)

        self.menubar = self.menuBar()
        self.File_menu = self.menubar.addMenu('&File')

        self.load_file_action = QAction('Load file')
        self.File_menu.addAction(self.load_file_action)
        self.save_file_action = QAction('Save file')
        self.File_menu.addAction(self.save_file_action)


        self.load_file_action.triggered.connect(lambda:self.load_file_act())
        self.save_file_action.triggered.connect(lambda: self.save_file_act())

        self.Plotting_menu = self.menubar.addMenu('&Plot')

        self.main_layout = QtWidgets.QHBoxLayout(self._main)

        # self.frame_up = QFrame(self)

        self.Database_menu = self.menubar.addMenu('&Database')
        self.add_db_action = QAction('add database')
        self.Database_menu.addAction(self.add_db_action)
        self.add_db_action.triggered.connect(lambda: self.create_subwindow_subw())


        self.frame = QFrame(self)

        self.frame_button_lay = QFrame()
        self.button_lay = QVBoxLayout(self)

        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(350, 100, 80, 20))
        self.pushButton.setText('Show data')
        self.pushButton.clicked.connect(self.button)
        self.button_lay.addWidget(self.pushButton)

        self.pushButton2 = QPushButton(self)
        self.pushButton2.setGeometry(QRect(350, 100, 80, 20))
        self.pushButton2.setText('Show 2data')
        # self.pushButton2.clicked.connect(self.create_database)
        self.button_lay.addWidget(self.pushButton2)


        self.line = QLineEdit(self)
        self.line.setGeometry(QRect(350, 100, 80, 20))
        self.button_lay.addWidget(self.line)


        self.frame_button_lay.setLayout(self.button_lay)

        hor_lay = QVBoxLayout()
        self.frame.setLayout(hor_lay)
        hor_lay.addWidget(self.frame_button_lay)
        hor_lay.addWidget(self.table)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.frame)
        self.splitter.addWidget(self.canv)
        self.main_layout.addWidget(self.splitter)

        # self.main_layout.addWidget(self.button_lay)
        self.show()

    def button(self):
        print('button')

    def create_subwindow_subw(self):
        print('ddd')
        self.db_subwindow = Subwindow(self)




        # z youtube

        # SERVER_NAME = 'MySQL80'
        # DATABASE_NAME = 'sql_store'
        # USERNAME = ''
        # PASSWORD = ''
        #
        # connString = f'DRIVER={{SQL Server}};' \
        #              f'SERVER={SERVER_NAME};' \
        #              f'DATABASE={DATABASE_NAME}'
        # db = QSqlDatabase.addDatabase('QMYSQL')
        # db.setDatabaseName(connString)
        # print(db.open())
        # print(db.driverName())



    def load_file_act(self):
        print('load file action')
        path = QFileDialog.getOpenFileName(self, 'Open CSV', "Text files(.csv)") #"Text files(.csv)"
        self.file_path = path[0]
        print(self.file_path)
        self.table.load_file(self.file_path)



    def save_file_act(self):
        '''
        taking data from self.table and saving to csv file
        '''
        print('save file action')
        path = QFileDialog.getSaveFileName(self, 'Save CSV', "Text files(.csv)")
        print(path)
        if path[0] != '':
            with open(path[0], 'w') as file:
                writer = csv.writer(file, dialect ='excel')
                writer.writerow(self.table.col_labels)
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)







app = QApplication(sys.argv)

table = MainWindow()

sys.exit(app.exec_())
