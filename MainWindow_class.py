import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDesktopWidget,\
    QSplitter, QGridLayout, QAction, QApplication, QMainWindow, \
    QPushButton,QMessageBox, QCheckBox, QFileDialog, QLabel,QSizePolicy, QLineEdit, QComboBox
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Subwindow_class import Subwindow_Database
import csv
from MyTable_class import MyTable
from PlotCanvas_class import PlotCanvas
from MLWidget_class import MLWidget
from Right_table_class import Right_Table, Right_Table_Widget




class MainWindow(QMainWindow):


    def __init__(self):
        super(MainWindow, self).__init__()

        self.left, self.top  = 100, 100
        self.height, self.width,  = 800, 1600

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


        self.menubar = self.menuBar()
        self.File_menu = self.menubar.addMenu('&File')

        self.load_file_action = QAction('Load file')
        self.File_menu.addAction(self.load_file_action)
        self.save_file_action = QAction('Save file')
        self.File_menu.addAction(self.save_file_action)


        self.load_file_action.triggered.connect(lambda:self.load_file_act())
        self.save_file_action.triggered.connect(lambda: self.save_file_act())


        # Menu Manage Layout

        self.manage_layout_menu = self.menubar.addMenu('&Manage layout')

        self.manage_layout_action_table = QAction('Table', checkable=True)
        self.manage_layout_menu.addAction(self.manage_layout_action_table)
        self.manage_layout_action_table.setChecked(True)
        self.manage_layout_action_table.triggered.connect(self.manage_layout_checked_action)

        self.manage_layout_action_plot = QAction('Plot', checkable=True)
        self.manage_layout_menu.addAction(self.manage_layout_action_plot)
        self.manage_layout_action_plot.setChecked(True)
        self.manage_layout_action_plot.triggered.connect(self.manage_layout_checked_action)

        self.manage_layout_action_MLWidget = QAction('ML Widget', checkable=True)
        self.manage_layout_menu.addAction(self.manage_layout_action_MLWidget)
        self.manage_layout_action_MLWidget.setChecked(True)
        self.manage_layout_action_MLWidget.triggered.connect(self.manage_layout_checked_action)

        self.manage_layout_action_right_table = QAction('Right Table', checkable=True)
        self.manage_layout_menu.addAction(self.manage_layout_action_right_table)
        self.manage_layout_action_right_table.setChecked(True)
        self.manage_layout_action_right_table.triggered.connect(self.manage_layout_checked_action)

        self.main_layout = QtWidgets.QHBoxLayout(self._main)

        # self.frame_up = QFrame(self)


        # ========================== Menu Database

        self.Database_menu = self.menubar.addMenu('&Database')
        self.add_db_action = QAction('add database')
        self.Database_menu.addAction(self.add_db_action)
        self.add_db_action.triggered.connect(lambda: self.create_subwindow_subw())



        self.frame_left = QFrame(self)
        self.frame_left.setStyleSheet("QFrame {background-color: rgb(250, 255, 255);"
                                      "border-width: 1;"
                                      "border-radius: 3;"
                                      "border-style: solid;"
                                      "border-color: rgb(50,50,50)}"
                                      )

        # ======================= Left upper frame

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
        self.pushButton.setText('add column')
        self.pushButton.clicked.connect(self.button)
        self.button_lay.addWidget(self.pushButton)

        self.pushButton2 = QPushButton(self)
        self.pushButton2.setGeometry(QRect(350, 100, 80, 20))
        self.pushButton2.setText('Clear table')
        self.pushButton2.clicked.connect(self.clear_table)

        self.button_lay.addWidget(self.pushButton2)

        self.le_add_col = QLineEdit(self)
        self.button_lay.addWidget(self.le_add_col)

        self.line = QLineEdit(self)
        self.line.setGeometry(QRect(350, 100, 80, 20))
        self.button_lay.addWidget(self.line)

        self.frame_button_lay.setLayout(self.button_lay)


        # =================== Layout of frame and table on the left

        self.hor_lay_left = QVBoxLayout()
        self.hor_lay_left.addWidget(self.frame_button_lay)
        self.hor_lay_left.addWidget(self.table)

        self.frame_left.setLayout(self.hor_lay_left)

        # table_width = self.frame_left.frameGeometry().width()
        # table_height = self.frame_left.frameGeometry().height()
        # print('d', table_width, table_height)
        self.frame_left.setMinimumWidth(self.width/6)



        # ================== Center Frame and Layout

        self.frame_center = QFrame(self)
        self.frame_center.setStyleSheet("QFrame {background-color: rgb(255, 255, 255);"
                                "border-width: 1;"
                                "border-radius: 3;"
                                "border-style: solid;"
                                "border-color: rgb(50,50,50)}")
        self.frame_center.setMinimumWidth(self.width / 6)

        self.center_lay = QVBoxLayout(self)


        self.frame_center.setLayout(self.center_lay)
        # self.frame_center.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Maximum)
        # table_width = self.frame_center.frameGeometry().width()
        # table_height = self.frame_center.frameGeometry().height()
        # print('d', table_width, table_height)
        # self.frame_center.setMinimumWidth(table_width)
        # self.frame_center.setMinimumHeight(table_height)
        #



        self.frame_MLWidget = QFrame(self)
        self.layout_MLWidget = QGridLayout()

        self.ml_widget = MLWidget()

        self.layout_MLWidget.addWidget(self.ml_widget)

        self.frame_MLWidget.setStyleSheet("QFrame {background-color: rgb(250, 255, 255);"
                                      "border-width: 1;"
                                      "border-radius: 3;"
                                      "border-style: solid;"
                                      "border-color: rgb(50,50,50)}"
                                      )

        self.frame_MLWidget.setLayout(self.layout_MLWidget)
        self.frame_MLWidget.setMinimumWidth(self.width / 6)

        self.layout_MLWidget.setContentsMargins(5,5,5,5)


        # ============== RIGHT TABLE WIDGET  ================================


        self.frame_right_table = QFrame(self)
        self.frame_right_table.setStyleSheet("QFrame {background-color: rgb(250, 255, 255);"
                                      "border-width: 1;"
                                      "border-radius: 3;"
                                      "border-style: solid;"
                                      "border-color: rgb(50,50,50)}"
                                      )

        self.layout_right_table = QGridLayout()

        # self.label = QLabel()
        # self.label.setAlignment(Qt.AlignCenter)
        # self.label.setText(' labelllllllllllllllllllll ')
        #
        #
        self.right_table = Right_Table_Widget()
        # self.b_right_table = QPushButton(self)
        # self.b_right_table.setText('predict')
        # self.b_right_table.clicked.connect(self.predict)


        self.layout_right_table.addWidget(self.right_table)
        # self.layout_right_table.addWidget(self.label)
        # self.layout_right_table.addWidget(self.b_right_table)



        self.frame_right_table.setLayout(self.layout_right_table)

        # ============== FINAL SPLITTER ================================

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.frame_left)
        self.splitter.addWidget(self.frame_center)
        self.splitter.addWidget(self.frame_MLWidget)
        self.splitter.addWidget(self.frame_right_table)

        self.splitter.setStretchFactor(10, 10)

        self.main_layout.addWidget(self.splitter)


        # =============== Frame and layout under canvas ======================================

        self.under_canv_layout = QGridLayout()

        self.frame_under_canv = QFrame(self)
        self.frame_under_canv.setLayout(self.under_canv_layout)

        self.label_pt = QLabel(self)
        self.label_pt.setText('Plot type')
        # self.label1.setFixedSize(80, 30)
        self.label_x = QLabel(self)
        self.label_x.setText('X axis')
        self.label_y = QLabel(self)
        self.label_y.setText('Y axis')
        self.label_h = QLabel(self)
        self.label_h.setText('Hue')


        self.cb_plot_type = QComboBox(self)
        self.cb_plot_type.setMinimumSize(100, 40)
        self.cb_plot_type.addItem('Line plot')
        self.cb_plot_type.addItem('Bar plot')
        self.cb_plot_type.addItem('Scatter plot')

        self.le_x_axis = QLineEdit(self)
        self.le_x_axis.setMinimumSize(80, 40)

        self.le_y_axis = QLineEdit(self)
        self.le_y_axis.setMinimumSize(80, 40)

        self.le_hue = QLineEdit(self)
        self.le_hue.setMinimumSize(80, 40)

        self.b_plot = QPushButton(self)
        self.b_plot.setText('Plot')
        self.b_plot.setMinimumSize(80, 30)
        self.b_plot.clicked.connect(self.plot)

        self.b_clear_plot = QPushButton(self)
        self.b_clear_plot.setText('Clear Plot')
        self.b_clear_plot.setMinimumSize(100, 30)
        self.b_clear_plot.clicked.connect(self.clear_plot)

        self.checkbox =QCheckBox("col_names/indexes ", self)
        self.checkbox.stateChanged.connect(lambda:self.checkbox_changed(self.checkbox))

        self.under_canv_layout.addWidget(self.label_pt, 0, 1)
        self.under_canv_layout.addWidget(self.label_x, 0, 2)
        self.under_canv_layout.addWidget(self.label_y, 0, 3)
        self.under_canv_layout.addWidget(self.label_h, 0, 4)
        self.under_canv_layout.addWidget(self.b_plot, 0, 5)
        self.under_canv_layout.addWidget(self.b_clear_plot, 0, 6)
        self.under_canv_layout.addWidget(self.cb_plot_type, 1, 1)
        self.under_canv_layout.addWidget(self.le_x_axis, 1, 2)
        self.under_canv_layout.addWidget(self.le_y_axis, 1, 3)
        self.under_canv_layout.addWidget(self.le_hue, 1, 4)
        self.under_canv_layout.addWidget(self.checkbox, 1,5)


        # ================= Center splitter between canv and frame under canv =======================

        self.splitter_center = QSplitter(Qt.Vertical)
        self.splitter_center.addWidget(self.canv)
        self.splitter_center.addWidget(self.frame_under_canv)
        self.center_lay.addWidget(self.splitter_center)


        self.right_table.signal_for_ml_widget.connect(self.ml_widget.get_signal_for_right_table)
        self.ml_widget.signal_for_right_table.connect(self.right_table.get_signal_for_ml_widget)

        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # +++
        self.table.customContextMenuRequested.connect(self.generateMenu)  # +++
        self.table.viewport().installEventFilter(self)

        self.show()

    def predict(self):
        print('predict')
        # self.frame_center.show()

        combobox_output = self.combo_box_Y.currentText()
        print(combobox_output)
        self.ml_widget.predict(self.table, combobox_output)

    def manage_layout_checked_action(self):

        # dokończyć implementacje layout managment - znikanie widgetów itd.

        # x = self.sender().text()
        sender = self.sender()
        print(sender)
        x = sender.text()
        print(x)
        is_checked = sender.isChecked()
        print(is_checked)

        # print(self.main_layout.count())
        # for i in range(self.main_layout.count()):
        #     print(self.main_layout.itemAt(i))
        #
        # spliter = self.main_layout.itemAt(0)
        # num_of_splitter_widgets = spliter.widget().count()
        # print(num_of_splitter_widgets)
        # print(spliter)
        # # print(spliter.widget())
        # # print(spliter.widget().widget(0))
        #
        # spliter_widgets_list = [spliter.widget().widget(i) for i in range(num_of_splitter_widgets)]
        # print(spliter_widgets_list)
        #
        # spliter.removeWidget(spliter_widgets_list[0])
        # spliter_widgets_list[0].setParent(None)
        # spliter_widgets_list[0].deleteLater()

        if x == 'Plot':
            if is_checked:
                self.frame_center.show()
            else:
                self.frame_center.hide()

        elif x == 'Table':
            if is_checked:
                self.frame_left.show()
            else:
                self.frame_left.hide()

        elif x == 'ML Widget':
            if is_checked:
                self.frame_MLWidget.show()
            else:
                self.frame_MLWidget.hide()

        elif x == 'Right Table':
            if is_checked:
                self.frame_right_table.show()
            else:
                self.frame_right_table.hide()

    # Menu for right mouse click on cells in table, with functions

    def eventFilter(self, source, event):
        if(event.type() == QEvent.MouseButtonPress
            and event.buttons() == Qt.RightButton
            and source is self.table.viewport()):

            item = self.table.itemAt(event.pos())

            print('Global Pos:', event.globalPos())
            if item is not None:
                print('Table Item:', item.row(), item.column())
                self.menu = QMenu(self)
                # self.menu.addAction(item.text())         #(QAction('test'))
                self.ag = QActionGroup(self, exclusive=True)
                self.act0 = QAction('default', self.menu, checkable = True)
                self.act0.setChecked(True)  # default
                z = self.ag.addAction(self.act0)

                self.submenu_add_plot = QMenu('Add', self)
                self.act1 = QAction('X axis', checkable = True)
                self.act2 = QAction('Y axis',  checkable = True)
                self.act10 = QAction('Hue',  checkable=True)
                self.act1.triggered.connect(lambda: self.add_x_axis(item))
                self.act2.triggered.connect(lambda: self.add_y_axis(item))
                self.act10.triggered.connect(lambda: self.add_hue(item))
                self.submenu_add_plot.addAction(self.act1)
                self.submenu_add_plot.addAction(self.act2)
                self.submenu_add_plot.addAction(self.act10)

                self.submenu_add_data = QMenu('Add', self)
                self.act3 = QAction('Add column on the right', self.menu, checkable = True)
                self.act4 = QAction('Add row on the bottom', self.menu, checkable=True)
                self.act3.triggered.connect(lambda: self.add_column_right(item))
                self.act4.triggered.connect(lambda: self.add_row_bottom(item))
                self.submenu_add_data.addAction(self.act3)
                self.submenu_add_data.addAction(self.act4)


                self.submenu_clear_data = QMenu('Clear data',self)
                self.act5 = QAction('Clear column')
                self.act6 = QAction('Clear row')
                self.act5.triggered.connect(lambda: self.clear_column(item))
                self.act6.triggered.connect(lambda: self.clear_row(item))
                self.submenu_clear_data.addAction(self.act5)
                self.submenu_clear_data.addAction(self.act6)

                self.submenu_del_data = QMenu('Delete data', self)
                self.act7 = QAction('Delete column')
                self.act8 = QAction('Delete row')
                self.act7.triggered.connect(lambda: self.delete_column(item))
                self.act8.triggered.connect(lambda: self.delete_row(item))
                self.submenu_del_data.addAction(self.act7)
                self.submenu_del_data.addAction(self.act8)

                self.act9 = QAction('Clear cell')
                self.act9.triggered.connect(lambda: self.clear_sel_data())
                self.submenu_clear_data.addAction(self.act9)

                self.submenu_sort_data = QMenu('Sort data', self)
                self.act11 = QAction('Sort ascending data')
                self.act11.triggered.connect(lambda: self.sort_column(item, 'ascending'))
                self.submenu_sort_data.addAction(self.act11)

                self.act12 = QAction('Sort descending data')
                self.act12.triggered.connect(lambda: self.sort_column(item, 'descending'))
                self.submenu_sort_data.addAction(self.act12)



                self.menu.addAction(z)
                self.menu.addMenu(self.submenu_add_plot)
                self.menu.addMenu(self.submenu_sort_data)
                self.menu.addMenu(self.submenu_clear_data)
                self.menu.addMenu(self.submenu_del_data)




                #menu.exec_(event.globalPos())
        return super(MainWindow, self).eventFilter(source, event)

    def generateMenu(self, pos):
        print("pos======", pos)
        self.menu.exec_(self.table.mapToGlobal(pos))  # +++

    def add_column_right(self, item):
        print('add column right')
        col = item.column()
        header_name = self.le_add_col.text()
        print(col, header_name)
        self.table.add_col_right(col, header_name)

    def add_row_bottom(self, item):
        print('add row bottom')
        col = item.row()
        self.table.add_row_bottom(col)


    def clear_column(self, item):
        print('clear column')
        col = item.column()
        self.table.clear_column(col)


    def clear_row(self, item):
        print('clear row')
        row = item.row()
        self.table.clear_row(row)


    def delete_column(self, item):
        col = item.column()
        self.table.removeColumn(col)

    def delete_row(self, item):
        row = item.row()
        self.table.removeRow(row)

    def clear_sel_data(self):
        # cols = self.table.selectionModel().selectedColumns()
        # indexes = []
        # for c in cols:  # c is QModelndex object
        #     print(c.column())
        #     indexes.append(c.column())
        # print('indexes ', indexes)

        self.table.clear_selected_data()

    def add_x_axis(self, item):
        print('zmiana')
        col = item.column()
        print(col)
        l = self.table.col_labels.tolist()[col]
        print(l)
        text = self.le_x_axis.text()
        if text:
            text = text +  ',' +l
        else:
            text = text + l
        print(text)
        self.le_x_axis.setText(text)


    def add_y_axis(self, item):
        print('zmiana')
        col = item.column()
        print(col)
        l = self.table.col_labels.tolist()[col]
        print(l)
        text = self.le_y_axis.text()
        if text:
            text = text +  ',' + l
        else:
            text = text + l
        print(text)
        self.le_y_axis.setText(text)

    def add_hue(self, item):
        print('add hue')
        col = item.column()
        l = self.table.col_labels.tolist()[col]
        text = self.le_hue.text()
        if text:
            text = text +  ',' +l
        else:
            text = text + l
        print(text)
        self.le_hue.setText(text)

    def sort_column(self, item, type):

        # only one column,

        print(type)
        col = item.column()
        if type == 'ascending':
            print('asc')
            self.table.sort_columns([col], type)
        elif type == 'descending':
            print('desc')
            self.table.sort_columns([col], type)


    # ===============================================================================


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
        print('plot')
        t = self.cb_plot_type.currentText()
        x = self.le_x_axis.text()
        y = self.le_y_axis.text()
        h = self.le_hue.text()

        val = self.col_or_indexes(x,y)

        if val == 'col_names':
            print(x)
            self.canv.plot_col_names(t, x, y, h)
        elif val == 'indexes':
            print(x)
            self.canv.plot_indexes(t, x, y, h)
        else:
            print('LineEdits dont match')
            return None

    def checkbox_changed(self, b):

        # This function changed columns names to indexes and vice-versa
        x = self.le_x_axis.text()
        y = self.le_y_axis.text()
        val = self.col_or_indexes(x,y)
        print(val, b.isChecked())

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

            self.le_x_axis.setText(set_x)
            self.le_y_axis.setText(set_y)

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
            self.le_x_axis.setText(set_x_n)
            self.le_y_axis.setText(set_y_n)

        elif val == 'col_names' and b.isChecked() == True:
            None

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

        # self.bbb = QPushButton(self)
        # self.bbb.setText('bbb')
        # self.bbb = Subwindow_Database(self)

        # self.hor_lay_left.addWidget(self.bbb)


        self.center_lay.removeWidget(self.canv)
        self.canv.deleteLater()
        self.canv.setParent(None)


    def clear_plot(self):
        self.canv.ax.clear()


    def clear_table(self):
        print('clear table')
        # self.table.reset()







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

    def create_subwindow_subw(self):
        print('sub')
        subwindow = Subwindow_Database(self)
        # subwindow.show()



    def load_file_act(self):
        print('load file action')
        path = QFileDialog.getOpenFileName(self, 'Open CSV', "Text files(.csv)") #"Text files(.csv)"
        self.file_path = path[0]
        print(self.file_path)
        self.table.load_file(self.file_path)
        print('ddd', self.table.col_labels)

        # self.combo_box_Y.clear()
        # self.combo_box_Y.addItems(self.table.col_labels.tolist())
        print(self.table.dataframe)
        self.ml_widget.set_dataframe(self.table.dataframe)
        self.ml_widget.set_col_labels(self.table.col_labels)


    def save_file_act(self):
        '''
        taking data from self.table and saving to csv file
        '''
        print('save file action')
        path = QFileDialog.getSaveFileName(self, 'Save CSV', "Text files(.csv)")
        print(path)
        print(self.table.col_labels)
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

