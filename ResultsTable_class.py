import PyQt5
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import csv
import numpy as np
import pandas as pd

from TableWidget_class import TableWidget


class ResultsTableWidget(QWidget):
    signal_for_ml_widget = pyqtSignal(str)

    def __init__(self):
        print('subwindow init')
        super(ResultsTableWidget, self).__init__()


        # self.main_layout = QVBoxLayout(self)
        self.main_layout = QGridLayout(self)

        # self.table = Right_Table(10,10)
        self.table = TableWidget(1, 15)

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)  # +++
        self.table.customContextMenuRequested.connect(self.generateMenu)  # +++
        self.table.viewport().installEventFilter(self)


        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(' Results ')


        self.b_predict = QPushButton(self)
        self.b_predict.setText('test button')
        self.b_predict.clicked.connect(self.predict)
        self.b_predict.setMinimumHeight(30)

        self.b_clear= QPushButton(self)
        self.b_clear.setText('clear table')
        self.b_clear.clicked.connect(self.reset)
        self.b_clear.setMinimumHeight(30)

        self.b_save= QPushButton(self)
        self.b_save.setText('save results')
        self.b_save.clicked.connect(self.save_file_act)
        self.b_save.setMinimumHeight(30)

        # self.main_layout.addWidget(self.label)
        # self.main_layout.addWidget(self.table)
        # self.main_layout.addWidget(self.b_predict)
        # self.main_layout.addWidget(self.b_clear)
        # self.main_layout.addWidget(self.b_save)

        self.lay_right = QGridLayout()
        self.lay_right.addWidget(self.b_predict, 0,0)
        self.lay_right.addWidget(self.b_clear, 1,0)
        self.lay_right.addWidget(self.b_save, 2,0)



        # self.main_layout.addWidget(self.label, 0,0)
        # self.main_layout.addWidget(self.table, 1,0)
        # self.main_layout.addLayout(self.lay_right, 0,1,2,1)

        self.main_layout.addLayout(self.lay_right, 0,0, 3,1)
        self.main_layout.addWidget(self.label, 0,1, 1,4)
        self.main_layout.addWidget(self.table, 1,1, 6,4)



        # self.main_layout.addWidget(self.b_predict, 2,0)
        # self.main_layout.addWidget(self.b_clear, 3,0)
        # self.main_layout.addWidget(self.b_save, 4,0)


        self.complete_data = []
        self.labels_a = []
        self.labels_b = []
        self.labels_c = []
        self.first_time_value = True

        # Create initial dataframe
        # x = 4
        # self.col_labels = [str(i) for i in range(x)]
        # self.data_init = np.zeros((1,x))
        # print(self.data_init)
        # # self.data_init[0,0] = np.nan
        # self.dataframe = pd.DataFrame(self.data_init, columns = self.col_labels)
        # self.update_with_values(self.data_init, self.col_labels)
        self.dataframe = pd.DataFrame()

        # Sygnały
        # self.procStart.connect(self.ml_widget.on_procStart)
        # self.show()

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonPress
                and event.buttons() == Qt.RightButton
                and source is self.table.viewport()):

            item = self.table.itemAt(event.pos())

            print('Global Pos:', event.globalPos())
            if item is not None:
                print('Table Item:', item.row(), item.column())
                self.menu = QMenu(self)
                # self.menu.addAction(item.text())         #(QAction('test'))
                self.ag = QActionGroup(self, exclusive=True)
                self.act0 = QAction('default', self.menu, checkable=True)
                self.act0.setChecked(True)  # default
                z = self.ag.addAction(self.act0)


                self.submenu_add_data = QMenu('Add', self)
                self.act3 = QAction('Add column on the right', self.menu, checkable=True)
                self.act4 = QAction('Add row on the bottom', self.menu, checkable=True)
                self.act3.triggered.connect(lambda: self.add_column_right(item))
                self.act4.triggered.connect(lambda: self.add_row_bottom(item))
                self.submenu_add_data.addAction(self.act3)
                self.submenu_add_data.addAction(self.act4)

                self.submenu_clear_data = QMenu('Clear data', self)
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

                # menu.exec_(event.globalPos())
        return super(ResultsTableWidget, self).eventFilter(source, event)

    def generateMenu(self, pos):
        print("pos======", pos)
        try:
            self.menu.exec_(self.table.mapToGlobal(pos))  # +++

        except AttributeError:
            print('load data')
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

        self.table.clear_selected_data()


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
    # ======================= SIGNALS ==============================

    @pyqtSlot()
    def emit_signal_for_ml_widget(self):
        self.signal_for_ml_widget.emit('hasło od right table')

    @pyqtSlot(tuple)
    def get_signal_from_ml_widget(self, parameters):
        print("From ML WIDGET:  ", parameters)

        self.update_table_with_results(parameters)
        self.raise_()

    # ======================= METHODS ==============================

    def predict(self):
        self.emit_signal_for_ml_widget()

    def is_visible(self):
        return self.is_visible()

    def extract_values_from_list(self):
        print('exr from list')

        # a = []
        # for l in self.labels_a:
        #     for l2 in l:
        #         a.append(l2)
        # a_set = np.array(a)
        # a_set = np.unique(a_set)
        # a_out = a_set.tolist()
        #
        # print(a_out)

        # Tutaj jeśli 4

        a_out = self.labels_a[0]

        b= []
        for l in self.labels_b:
            for l2 in l:
                b.append(l2)
        # b_set = np.array(b)
        # b_set = np.unique(b_set)
        # b_out = b_set.tolist()
        b_out = []
        for i in b:
            if i not in b_out:
                b_out.append(i)

        print(b_out)

        c = []
        for l in self.labels_c:
            for l2 in l:
                c.append(l2)
        # c_set = np.array(c)
        # c_set = np.unique(c_set)
        # c_out = c_set.tolist()
        c_out = []
        for i in c:
            if i not in c_out:
                c_out.append(i)

        print(c_out)
        print(len(a_out))
        print(len(b_out))
        print(len(c_out))

        # zwraca listy podzielone a-c oraz ich długości
        return a_out,len(a_out), b_out,len(b_out), c_out, len(c_out)

    def show_current_labels(self):
        print('current labels')
        print('a')
        print(self.labels_a)
        print('b')
        print(self.labels_b)
        print('c')
        print(self.labels_c)


    def update_lens(self, parameters_labels, len):
        print('update lens')
        a = len[0]  # 5
        b = len[0] + len[1] # 6
        c = b + len[2]  # 8
        print(a,b,c)
        print('update labels lists')
        print(parameters_labels[:a])
        print(parameters_labels[a:b])
        print(parameters_labels[b:c])
        
        self.labels_a.append(parameters_labels[:a])
        self.labels_b.append(parameters_labels[a:b])
        self.labels_c.append(parameters_labels[b:c])


    def first_time(self, par, parameters_labels, len):

        # Dodaje dane - par, i labele do funkcji update_with_values()
        # update lens - dodaje kolumny dla każdego wiersza
        print('first time')
        print(par)
        print(parameters_labels)
        self.update_lens(parameters_labels, len)

        self.dataframe = pd.DataFrame(data=np.array(par).reshape(1,-1), columns = parameters_labels)
        # self.set_column_labels(parameters_labels)
        self.table.update_from_df(self.dataframe)

    def next_time(self, par, parameters_labels, len):
        a = len[0]  # 5
        b = len[0] + len[1] # 6
        c = b + len[2]  # 8
        print(a,b,c)
        self.show_current_labels()

        # Nowy wiersz
        new_a = pd.DataFrame(data=np.array(par[:a]).reshape(1, -1), columns=parameters_labels[:a])
        print('a shapes: ', new_a.shape)
        print('a')
        print(new_a)
        new_b = pd.DataFrame(data=np.array(par[a:b]).reshape(1, -1), columns=parameters_labels[a:b])
        print('b shapes: ', new_b.shape)
        print('b')
        print(new_b)
        new_c = pd.DataFrame(data=np.array(par[b:]).reshape(1, -1), columns=parameters_labels[b:])
        print('c shapes: ', new_c.shape)
        print(new_c)

        # pobranie aktualnych list labeli A-C
        la, a2, lb, b2, lc, c2 = self.extract_values_from_list()
        print(la, lb, lc)
        # print(type(la))
        b2 += a2
        c2 += b2
        # a2 = len(la)
        # print(a2)
        # b2= len(lb) + a2
        # c2= len(lc) + b2
        print(a2, b2, c2)
        print(self.dataframe)
        # Dataframe A-C z aktualnych danych
        df_a = pd.DataFrame(data=self.dataframe.values[:, :a2], columns=la)
        df_b = pd.DataFrame(data=self.dataframe.values[:, a2:b2], columns=lb)
        df_c = pd.DataFrame(data=self.dataframe.values[:, b2:], columns=lc)
        print('CURRENT DATASET SPLITTED')
        print('a shapes: ', df_a.shape)
        print('a')
        print(df_a)

        print('b shapes: ', df_b.shape)
        print('b')
        print(df_b)

        print('c shapes: ', df_c.shape)
        print('c')
        print(df_c)

        df_aa = new_a.append(df_a, ignore_index=True)
        df_bb = new_b.append(df_b, ignore_index=True)
        df_cc = new_c.append(df_c, ignore_index=True)
        print('PO ZŁĄCZENIU')
        print('a')
        print(df_aa)
        print(df_aa.shape)

        print('b')
        print(df_bb)
        print(df_bb.shape)

        print('c')
        print(df_cc)
        print(df_cc.shape)

        r = pd.concat([df_aa, df_bb, df_cc], axis=1)
        r = r.astype(str)
        print('r')
        print(r)
        self.dataframe = r
        self.table.update_from_df(self.dataframe)

        self.update_lens(parameters_labels, len)


    def update_table_with_results(self, parameters_list):
        print('update_table_with_results')
        print(self.dataframe)

        par, parameters_labels, len = parameters_list

        # Jeśli pierwsze dodanie
        if self.first_time_value is True:
            print('f')
            self.first_time(par, parameters_labels, len)
            self.first_time_value = False
        # kolejne dodanie
        else:
            self.next_time(par, parameters_labels, len)
        self.table.set_column_labels(self.dataframe.columns)



    def reset(self):
        print('reset table ')
        self.table.reset()
        self.first_time_value = True
        # self.table.reset()

    def save_file_act(self):
        '''
        taking data from self.table and saving to csv file
        '''
        print('save file action')
        path = QFileDialog.getSaveFileName(self, 'Save CSV', "Text files(.csv)")
        if path[0] != '':
            print(path)
            print(self.table.col_labels)
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


