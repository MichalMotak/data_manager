import sys
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem
import pandas as pd



class MyTable(QTableWidget):
    def __init__(self, r,c):
        super().__init__(r,c)

        self.signals()

    def signals(self):
        self.cellClicked.connect(self.clicked)
        self.show()

    def clicked(self):

        for item in self.selectedItems():
            print(item.text())
        # item = self.currentItem()
        #
        # # item = self.item(2,2)
        # print(item)
        # print(item.text())


class Sheet(QMainWindow):
    def __init__(self, file_path):
        super(Sheet, self).__init__()
        self.data = None
        self.load_csv(file_path)
        print(self.data.shape)

        # self.form_widget = MyTable(self.data.shape[0], self.data.shape[1])
        self.form_widget = MyTable(10,10)
        self.setCentralWidget(self.form_widget)


        print(self.col_labels)
        self.form_widget.setHorizontalHeaderLabels(self.col_labels)

        # self.show_data()
        self.show()

    def load_csv(self,file_path):
        self.data = pd.read_csv(file_path)
        self.col_labels = self.data.columns.tolist()
        self.data = self.data.values[:100,:]

        # return self.col_labels

    def show_data(self):
        # stuff = 'ddd'
        # item = QTableWidgetItem(stuff)
        # self.form_widget.setItem(2,2, item)

        self.form_widget.setRowCount(0)
        self.form_widget.setColumnCount(3)

        for row_data in self.data:
            print(row_data)
            row = self.form_widget.rowCount()
            self.form_widget.insertRow(row)
            if len(row_data) > 100:
                self.form_widget.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(str(stuff))
                print(row, column, stuff)
                self.form_widget.setItem(row,column, item)


app = QApplication(sys.argv)
file_path = 'countries.csv'
# file_path = 'dent.txt'
table = Sheet(file_path)
file_path = 'countries.csv'
# table.load_csv(file_path)
sys.exit(app.exec_())