from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QPushButton
from PyQt5.QtCore import *
import pandas as pd
import os
import os.path
import numpy as np


class TableWidget(QTableWidget):
    resized = pyqtSignal()
    signal_for_preprocessing_widget = pyqtSignal(pd.core.frame.DataFrame)
    signal_for_ml_widget = pyqtSignal(pd.core.frame.DataFrame)

    def __init__(self, r ,c ):
        super().__init__(r,c)
        self.rows = r
        self.columns = c
        # print('mywindow', mainw.data.shape)
        # self.data = mainw.data
        # self.signals()
        # mainw.pushButton.hide()
        # self.setGeometry(QtCore.QRect(0,0, 80, 20))

        self.table_test = 'table_test'
        self.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.Alignment(Qt.TextWordWrap))
        self.resized.connect(self.resized_fun)
        # self.show()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MyTable, self).resizeEvent(event)

    def resized_fun(self):
        None
        # print("someFunction")

    def signals(self):
        self.cellClicked.connect(self.clicked)

    def clicked(self):
        for item in self.selectedItems():
            print(item.text())
        print('c')

    def set_column_labels(self, list_):
        """ This function sets self.HorizontalHeaderLabels
        Args:
            list ([type]): list of new header labels
        """
        print('set column labels')
        print(list_)
        self.col_labels = list_
        self.setHorizontalHeaderLabels(list_)
        self.show()

    def set_row_labeles(self, list_):
        print('set row labels')
        print(list_)
        self.col_labels = list_
        self.setVerticalHeaderLabels(list_)
        self.show()  

    def update_from_df(self, dataframe):
        print('update from df')
        self.dataframe = dataframe
        self.col_labels = self.dataframe.columns

        self.data = self.dataframe.values
        print(self.data.shape)

        self.setRowCount(0)
        self.setColumnCount(self.data.shape[1])
        self.set_column_labels(self.col_labels)

        for row_data in self.data:
            row = self.rowCount()
            self.insertRow(row)
            # if len(row_data) > 100:
            #     self.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(str(stuff))
                self.setItem(row, column, item)

        self.emit_signal_for_preprocessing_widget()
        self.emit_signal_for_ml_widget()


    def add_row_bottom(self, row):

        df1 = self.dataframe.iloc[:row+1,:]  # split df
        df2 = self.dataframe.iloc[row+1:,:]
        df1 = df1.append(pd.Series(), ignore_index = True) # add empty row
        ind = df2.index.values.tolist()
        ind = [i+1 for i in ind]
        df2 = df2.set_index([ind])
        final_df = pd.concat([df1,df2], ignore_index = True)  # concat

        self.update_from_df(final_df)

    def add_col_right(self, col, header_name):
        print('add col right')

        final_df = self.dataframe
        final_df[header_name] = ""
        col = col+1
        column = self.dataframe.columns.tolist()
        c1 = column[:col]
        c1.append(header_name)
        c3 = column[col:-1]
        column = c1 + c3
        final_df = final_df[column]

        self.update_from_df(final_df)



    def clear_selected_data(self):
        items = self.selectedItems()
        for c in items:
            row = c.row()
            col = c.column()
            item = self.takeItem(row,col)
            item.setText('')

    def clear_column(self, col):
        print(col)
        rows = self.rowCount()
        print(rows)

        # Clear in Table
        for row in range(rows):
            item = self.takeItem(row, col)
            item.setText('')

        # Clear Dataframe
        # df = 
        
        

    def clear_row(self, row):
        print(row)
        columns = self.columnCount()

        for col in range(columns):
            item = self.takeItem(row, col)
            item.setText('')
        

    def delete_row(self, row):
        print('delete row')
        print(row)
        # self.removeRow(row)
        df = self.dataframe.drop([row])
        print(df)
        self.update_from_df(df)

    def delete_column(self, column):
        print('delete column')
        print(column)
        print(self.col_labels)
        # self.removeColumn(column)

        # print(self.col_labels)
        # current_labels = self.col_labels.tolist()
        # print(current_labels)
        # current_labels.pop(column)
        # print(current_labels)
        # self.set_column_labels(current_labels)
        # print(self.col_labels)

        # Delete column from Dataframe
        print('delete column from df')
        col_name = self.col_labels[column]
        print(col_name)
        df = self.dataframe.drop(col_name, 1)
        print(df)
        self.update_from_df(df)

    def sort_columns(self, columns_l, type):

        c = self.col_labels.tolist()
        columns_l = [c[i] for i in columns_l]
        print(columns_l)
        if type == 'ascending':
            asc = True
            print('asc')
        elif type == 'descending':
            asc = False
            print('desc')


        df = self.dataframe.sort_values(by=columns_l, ascending=asc)
        print('d')
        self.update_from_df(df)

    def reset(self):
        print('reset table ')
        df = pd.DataFrame()
        self.update_from_df(df)

        self.setRowCount(self.rows)
        self.setColumnCount(self.columns)

        self.update()


    def load_file(self, file_path):

        ext = os.path.splitext(file_path)[1]
        print(ext)

        print('show data')
        if ext == '.csv':
            self.dataframe = pd.read_csv(file_path)
        elif ext == '.xlsx':
            self.dataframe = pd.read_excel(file_path)
        elif ext == '.json':
            self.dataframe = pd.read_json(file_path)
        else:
            return None

        self.update_from_df(self.dataframe)


    @pyqtSlot()
    def emit_signal_for_preprocessing_widget(self):
        print('emit_signal_for_table ', self.dataframe)
        self.signal_for_preprocessing_widget.emit(self.dataframe)


    @pyqtSlot(pd.core.frame.DataFrame)
    def get_signal_from_preprocessing_widget(self, df):
        print("signal_for_table ")
        print(df.shape)
        self.update_from_df(df)
        self.raise_()

    @pyqtSlot()
    def emit_signal_for_ml_widget(self):
        print('emit_signal_for_table ', self.dataframe)
        self.signal_for_ml_widget.emit(self.dataframe)
