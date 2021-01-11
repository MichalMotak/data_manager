from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import numpy as np
import pandas as pd

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

        self.b_clear= QPushButton(self)
        self.b_clear.setText('clear table')
        self.b_clear.clicked.connect(self.reset)

        self.main_layout.addWidget(self.table)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.b_predict)
        self.main_layout.addWidget(self.b_clear)


        self.complete_data = []
        self.labels_a = []
        self.labels_b = []
        self.labels_c = []
        self.iter = 0

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
        self.show()

    # ======================= SIGNALS ==============================

    @pyqtSlot()
    def emit_signal_for_ml_widget(self):
        self.signal_for_ml_widget.emit('hasło od right table')

    @pyqtSlot(tuple)
    def get_signal_for_ml_widget(self, parameters):
        print("From ML WIDGET:  ", parameters)

        self.update_table_with_results(parameters[0], parameters[1], parameters[2])
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
        b_set = np.array(b)
        b_set = np.unique(b_set)
        b_out = b_set.tolist()

        print(b_out)

        c = []
        for l in self.labels_c:
            for l2 in l:
                c.append(l2)
        c_set = np.array(c)
        c_set = np.unique(c_set)
        c_out = c_set.tolist()

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
        self.update_with_values(self.dataframe.values, parameters_labels)

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


        # if new_a.shape[1] >= df_a.shape[1]:
        #     df_aa = new_a.append(df_a, ignore_index=True)
        # else:
        #     df_aa = df_a.append(new_a, ignore_index=True)
        #
        #
        # if new_b.shape[1] >= df_b.shape[1]:
        #     df_bb = new_b.append(df_b, ignore_index=True)
        # else:
        #     df_bb = df_b.append(new_b, ignore_index=True)
        #
        # if new_c.shape[1] >= df_c.shape[1]:
        #     df_cc = new_c.append(df_c, ignore_index=True)
        # else:
        #     df_cc = df_c.append(new_c, ignore_index=True)

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
        print('r')
        print(r)
        self.dataframe = r
        self.update_with_values(self.dataframe.values, list(self.dataframe.columns))

        self.update_lens(parameters_labels, len)


    def update_table_with_results(self, par, parameters_labels, len):
        print('update_table_with_results')
        print(self.dataframe)
        # self.complete_data.append(len)
        # Jeśli pierwsze dodanie
        if self.iter == 0:
            self.first_time(par, parameters_labels, len)
            self.iter += 1
        # kolejne dodanie
        else:
            self.next_time(par, parameters_labels, len)

        # ############################################
        # a = len[0]  # 5
        # b = len[0] + len[1] # 6
        # c = b + len[2]  # 8
        # print(a,b,c)
        #
        #
        # print(self.labels_b)
        # print(len(self.labels_b))
        # if len(self.labels_b) == 0:
        #     print('dddddddddddddddddddd')
        #
        # arr = np.array(self.complete_data)
        # sum = np.max(arr, axis = 0)
        # a0 = sum[0]
        # b0 = sum[0] + sum[1]
        # c0 = b0 + sum[2]
        # print(a0, b0, c0)
        #
        # self.labels_b = list(self.dataframe.columns[a0:b0])
        # print('labels b: ', self.labels_b)
        #
        # new_labels_b = parameters_labels[a:b]
        #
        # for n in new_labels_b:
        #     if n not in self.labels_b:
        #         self.labels_b.append(n)
        # print('labels b :', self.labels_b)
        #
        # new_labels_c = parameters_labels[b:]
        #
        # for n in new_labels_c:
        #     if n not in self.labels_c:
        #         self.labels_c.append(n)
        # print('labels c :', self.labels_c)
        #
        #
        # ind_1 = list(self.dataframe.columns).index(self.labels_c[0])
        # ind_2 = list(self.dataframe.columns).index(self.labels_c[-1])
        #
        #
        # print(ind1, ind_2)
        #
        # df_a = pd.DataFrame(data=self.dataframe.values[:,:a0], columns=list(self.dataframe.columns[:a0]))
        # df2_a = pd.DataFrame(data=np.array(par[:a]).reshape(1, -1), columns=parameters_labels[:a])
        # print('a shapes: ', df_a.shape, df2_a.shape)
        #
        # if df2_a.shape[1] >= df_a.shape[1]:
        #     df_aa = df2_a.append(df_a, ignore_index=True)
        # else:
        #     df_aa = df_a.append(df2_a, ignore_index=True)
        # print('a')
        # print(df_a)
        # print(df2_a)
        # print(df_aa)
        # print(df_aa.shape)
        #
        # df_b = pd.DataFrame(data=self.dataframe.values[:,a0:b0], columns=list(self.dataframe.columns[a0:b0]))
        # df2_b = pd.DataFrame(data=np.array(par[a:b]).reshape(1, -1), columns=parameters_labels[a:b])
        # print('b shapes: ', df_b.shape, df2_b.shape)
        #
        # print('b')
        # print(df_b)
        # print(df2_b)
        #
        # if df2_b.shape[1] >= df_b.shape[1]:
        #     df_bb = df2_b.append(df_b, ignore_index=True)
        # else:
        #     df_bb = df_b.append(df2_b, ignore_index=True)
        #
        #
        # print(df_bb)
        # print(df_bb.shape)
        #
        # df_c = pd.DataFrame(data=self.dataframe.values[:,b0:], columns=list(self.dataframe.columns[b0:]))
        # df2_c = pd.DataFrame(data=np.array(par[b:]).reshape(1, -1), columns=parameters_labels[b:])
        # print('c shapes: ', df_c.shape, df2_c.shape)
        #
        # print(df_c)
        # print(df2_c)
        #
        # if df2_c.shape[1] >= df_c.shape[1]:
        #     df_cc = df2_c.append(df_c, ignore_index=True)
        # else:
        #     df_cc = df_c.append(df2_c, ignore_index=True)
        #
        # print(df_cc)
        # print(df_cc.shape)
        #
        # r = pd.concat([df_aa, df_bb, df_cc], axis=1)
        # print('r')
        # print(r)
        # self.dataframe = r
        # self.update_with_values(self.dataframe.values, list(self.dataframe.columns))
        # return r

        ############################################
        # par = np.array(par)
        # par2 = par.reshape(1,-1)
        # print(self.dataframe.shape, par2.shape)
        #
        # # df1 = pd.DataFrame(par2, columns = [str(x) for x in range(par2.shape[1])])
        # df1 = pd.DataFrame(par2, columns = parameters_label#s)
        #
        # print('df1')
        # print(df1)
        # print('df1')
        #
        # if df1.shape[1] > self.dataframe.shape[0]:
        #     self.dataframe = df1.append(self.dataframe,ignore_index = True)
        # else:
        #     self.dataframe = self.dataframe.append(df1, ignore_index=True)
        #
        # print(self.dataframe)
        # # print(x)
        # # print('x')
        # self.update_with_values(self.dataframe.values, parameters_labels)



    def set_column_labels(self, list):
        print('sel column labels')
        print(list)
        self.col_labels = list
        print(self.col_labels)
        self.table.setHorizontalHeaderLabels(list)
        # self.table.setHorizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.table.show()
        # self.resizeColumnsToContents()

    def update_with_values(self, data, new_col_labels=[]):
        print('update wi')
        self.data = data
        print(self.data.shape)

        # new_col_labeles = [str(x) for x in range(data.shape[1])]

        self.table.setRowCount(0)
        self.table.setColumnCount(self.data.shape[1])
        # self.set_column_labels(self.col_labels)
        self.set_column_labels(new_col_labels)

        for row_data in self.data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            # if len(row_data) > 100:
            #     self.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(str(stuff))
                item.setTextAlignment(Qt.AlignHCenter)
                self.table.setItem(row, column, item)

    def reset(self):
        self.dataframe = pd.DataFrame()
        self.update_with_values(self.dataframe.values)


class Right_Table(QTableWidget):
    def __init__(self, r ,c ):
        super().__init__(r,c)
        self.rows = r
        self.columns = c


