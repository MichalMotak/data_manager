from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QPushButton
from PyQt5 import QtCore
import pandas as pd
import os
import os.path


class MyTable(QTableWidget):
    resized = QtCore.pyqtSignal()
    def __init__(self, mainw, r ,c ):
        super().__init__(r,c )
        # print('mywindow', mainw.data.shape)
        # self.data = mainw.data
        print(mainw)
        # self.signals()
        # mainw.pushButton.hide()

        # self.setGeometry(QtCore.QRect(0,0, 80, 20))

        self.table_test = 'table_test'

        self.resized.connect(self.resized_fun)


        self.show()

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
        # item = self.currentItem()
        #
        # # item = self.item(2,2)
        # print(item)
        # print(item.text())

    def set_column_labels(self, list):
        print('sel column labels')
        print(list)
        self.c = len(list)
        self.setHorizontalHeaderLabels(list)
        self.show()
        # self.resizeColumnsToContents()

    def load_file(self, file_path):

        ext = os.path.splitext(file_path)[1]
        print(ext)

        print('show data')
        if ext == '.csv':
            dataframe = pd.read_csv(file_path)
        elif ext == '.xlsx':
            dataframe = pd.read_excel(file_path)
        else:
            return None
        self.col_labels = dataframe.columns

        self.data = dataframe.values
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
                self.setItem(row,column, item)