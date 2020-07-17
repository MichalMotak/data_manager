import sys
import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDesktopWidget,\
    QSplitter, QGridLayout, QAction, QTableWidget, QApplication, QMainWindow, \
    QTableWidgetItem, QPushButton,QMessageBox, QCheckBox, QFileDialog, QTableView, QLabel, QLineEdit, QComboBox
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
import mysql.connector as sql

from Database_class import Database
from Subwindow_class import Subwindow_Database

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
        self.setWindowTitle('File manager')
        self.move_to_center()

        self.table = MyTable(self, 10, 5)

        # layout = QGridLayout(self)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        # self.setCentralWidget(self.table)
        self.canv = PlotCanvas(self.table, 5, 3)


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




        self.frame_left = QFrame(self)



        self.frame_button_lay = QFrame(self)
        # self.frame_button_lay.setStyleSheet("QFrame {} ")
        self.frame_button_lay.setStyleSheet("QFrame {background-color: rgb(250, 255, 255);"
                                      "border-width: 1;"
                                      "border-radius: 3;"
                                      "border-style: solid;"
                                      "border-color: rgb(50,50,50)}"
                                      )

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


        hor_lay_left = QVBoxLayout()
        hor_lay_left.addWidget(self.frame_button_lay)
        hor_lay_left.addWidget(self.table)

        self.frame_left.setLayout(hor_lay_left)

        # table_width = self.frame_left.frameGeometry().width()
        # table_height = self.frame_left.frameGeometry().height()
        # print('d', table_width, table_height)
        self.frame_left.setMinimumWidth(self.width/3)




        self.frame_right = QFrame(self)
        self.frame_2 = QFrame(self)
        self.layout = QGridLayout()
        self.frame_2.setLayout(self.layout)

        self.frame_right.setStyleSheet("QFrame {background-color: rgb(255, 255, 255);"
                                "border-width: 1;"
                                "border-radius: 3;"
                                "border-style: solid;"
                                "border-color: rgb(50,50,50)}"
                                )

        self.frame_right.setMinimumWidth(self.width / 2)
        # self.p = QPushButton(self)
        # self.p.setGeometry(QRect(350, 100, 80, 20))
        # self.p.setText('Show data')
        # self.frame_2.addWidget(self.p)

        self.right_lay = QVBoxLayout(self)
        self.right_lay.addWidget(self.canv)
        self.right_lay.addWidget(self.frame_2)
        self.frame_right.setLayout(self.right_lay)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.frame_left)
        self.splitter.addWidget(self.frame_right)
        self.splitter.setStretchFactor(10, 10)

        self.main_layout.addWidget(self.splitter)

        self.label0 = QLabel(self)
        self.label0.setText('Plot type')
        # self.label1.setFixedSize(80, 30)
        self.label1 = QLabel(self)
        self.label1.setText('X axis')
        self.label2 = QLabel(self)
        self.label2.setText('Y axis')
        self.label3 = QLabel(self)
        self.label3.setText('Hue')


        self.combo = QComboBox(self)
        self.combo.setMinimumSize(100,40)
        self.combo.addItem('Line plot')
        self.combo.addItem('Bar plot')
        self.combo.addItem('Scatter plot')

        self.line1 = QLineEdit(self)
        self.line1.setMinimumSize(80, 40)

        self.line2 = QLineEdit(self)
        self.line2.setMinimumSize(80, 40)
        self.line3 = QLineEdit(self)
        self.line3.setMinimumSize(80, 40)

        self.b_plot = QPushButton(self)
        self.b_plot.setText('Plot')
        self.b_plot.setMinimumSize(80, 30)
        self.b_plot.clicked.connect(self.plot)

        self.checkbox =QCheckBox("Column names", self)
        self.checkbox.stateChanged.connect(lambda:self.checkbox_changed(self.checkbox))

        self.layout.addWidget(self.label0, 0, 1)
        self.layout.addWidget(self.label1, 0, 2)
        self.layout.addWidget(self.label2, 0, 3)
        self.layout.addWidget(self.label3, 0, 4)
        self.layout.addWidget(self.b_plot, 0, 5)

        self.layout.addWidget(self.combo, 1, 1)
        self.layout.addWidget(self.line1, 1, 2)
        self.layout.addWidget(self.line2, 1, 3)
        self.layout.addWidget(self.line3, 1, 4)
        self.layout.addWidget(self.checkbox, 1,5)

        self.frame_2.setLayout(self.layout)

        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # +++
        self.table.customContextMenuRequested.connect(self.generateMenu)  # +++
        self.table.viewport().installEventFilter(self)

        self.show()


    # implementation of adding columns to X/Y column

    def eventFilter(self, source, event):
        if(event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.RightButton
           and source is self.table.viewport()):

            item = self.table.itemAt(event.pos())

            print('Global Pos:', event.globalPos())
            if item is not None:
                print('Table Item:', item.row(), item.column())
                self.menu = QMenu(self)
                # self.menu.addAction(item.text())         #(QAction('test'))
                self.ag = QActionGroup(self, exclusive=True)
                self.act0 = QAction('default', self.menu, checkable = True)
                self.act1 = QAction('X axis', self.menu, checkable = True)
                self.act2 = QAction('Y axis', self.menu, checkable = True)
                self.act0.setChecked(True)
                z = self.ag.addAction(self.act0)
                a = self.ag.addAction(self.act1)
                b = self.ag.addAction(self.act2)
                self.menu.addAction(z)
                self.menu.addAction(a)
                self.menu.addAction(b)
                self.act1.triggered.connect(lambda:self.fun1(item))
                self.act2.triggered.connect(lambda: self.fun2(item))
                # white_color = QAction('White', checkable=True)
                # black_color = QAction('Black', checkable=True)
                # self.menu.addAction(white_color)
                # self.menu.addAction(black_color)
                #
                # play_action = QAction('Start game')
                # self.menu.addAction(play_action)
                # menu.addMenu(self.menu)

                #menu.exec_(event.globalPos())
        return super(MainWindow, self).eventFilter(source, event)

    def generateMenu(self, pos):
        print("pos======", pos)
        self.menu.exec_(self.table.mapToGlobal(pos))  # +++

    def fun1(self, item):
        print('zmiana')
        col = item.column()
        print(col)
        l = self.table.col_labels.tolist()[col]
        print(l)
        text = self.line1.text()
        if text:
            text = text +  ',' +l
        else:
            text = text + l
        print(text)
        self.line1.setText(text)


    def fun2(self, item):
        print('zmiana')
        col = item.column()
        print(col)
        l = self.table.col_labels.tolist()[col]
        print(l)
        text = self.line2.text()
        if text:
            text = text +  ',' +l
        else:
            text = text + l
        print(text)
        self.line2.setText(text)



    def move_to_center(self):
        qtRectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(center_point)
        self.move(qtRectangle.topLeft())

    def col_or_indexes(self, x,y):

        # check if lineEdits contain indexes or column names
        # returns 'col_names', 'indexes' or None

        print('check')
        xs = x.split(',')
        xs = [i for i in xs]
        ys = y.split(',')
        ys = [i for i in ys]
        print(xs, ys)

        xs2 = set(xs)
        ys2 = set(ys)
        c = self.table.col_labels.tolist()
        ints = [str(i) for i in range(len(c))]
        print(ints)

        if (xs2.issubset(set(c)) and ys2.issubset(set(c))):
            return ('col_names')
        elif (xs2.issubset(set(ints)) and ys2.issubset(set(ints))):
            return ('indexes')
        else:
            return None

    def plot(self):
        t = self.combo.currentText()
        x = self.line1.text()
        y = self.line2.text()
        h = self.line3.text()

        val = self.col_or_indexes(x,y)

        if val == 'col_names':
            print(x)
            # self.canv.plot_col_names(t, x, y, h)
        elif val == 'indexes':
            print(x)
            # self.canv.plot_indexes(t, x, y, h)
        else:
            print('LineEdits dont match')
            return None

    def checkbox_changed(self, b):

        # This function changed columns names to indexes and vice-versa
        x = self.line1.text()
        y = self.line2.text()
        val = self.col_or_indexes(x,y)

        if val == 'indexes' and b.isChecked():
            print('show column names')
            print(self.table.col_labels)
            xs = x.split(',')
            xs = [int(i) for i in xs]
            ys = y.split(',')
            ys = [int(i) for i in ys]
            print(xs,ys)

            # set_x = map(self.table.col_labels.__getitem__, xs)
            set_x = [self.table.col_labels[i] for i in xs]
            set_y = [self.table.col_labels[i] for i in ys]
            set_x = ','.join(map(str,set_x))
            set_y = ','.join(map(str,set_y))
            print(set_x)
            print(set_y)

            self.line1.setText(set_x)
            self.line2.setText(set_y)

        elif val == 'col_names' and b.isChecked() == False:
            print('show numbers')
            print(type(self.table.col_labels))
            xs = x.split(',')
            # xs = [int(i) for i in xs]
            ys = y.split(',')
            # ys = [int(i) for i in ys]
            print(xs, ys)
            # print(self.table.col_labels.tolist().index('diagnosis'))
            set_x = [self.table.col_labels.tolist().index(i) for i in xs]
            set_y = [self.table.col_labels.tolist().index(i) for i in ys]
            print(set_x,set_y)
            set_x_n = ','.join(map(str, set_x))
            set_y_n = ','.join(map(str, set_y))
            # print(set_x_n)
            # print(set_y_n)
            #
            self.line1.setText(set_x_n)
            self.line2.setText(set_y_n)

        else:
            print('message box')
            msg = QMessageBox()
            msg.setWindowTitle('Warning Message')
            msg.setText('X axis and Y axis dont match')
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()
            return None

    def button(self):
        print('button')
        # self.tableview = QTableView()
        # self.tableview.setModel(self.table)
        # print(self.table.selectedRanges())
        cols = self.table.selectionModel().selectedColumns()
        indexes = []
        for c in cols: # c is QModelndex object
            print(c.column())
            indexes.append(c.column())
        print('indexes ', indexes)



    def create_subwindow_subw(self):
        print('ddd')
        self.db_subwindow = Subwindow_Database(self)





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
