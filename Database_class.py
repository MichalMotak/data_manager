import mysql.connector as sql
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidget, QLabel, QComboBox, QApplication, QMainWindow, \
                            QTableWidgetItem, QPushButton, QLineEdit
from PyQt5.QtCore import *

class Database():

    def __init__(self, parent, host, user, passwd, database):
        super().__init__()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

        self.db = sql.connect(
            host=self.host,  # łaczymy sie jako nasz komputer, localhost
            user=self.user,  # nowy uzytkownik lub ten utworzony przy instalacji
            passwd=self.passwd,  # czyli user, passwd - root
            database=self.database, # use_pure=True
        )

        self.mycursor = self.db.cursor()


        self.table = parent




    def get_db_column_names(self):
        print('get db column names')
        print(self.mycursor)
        return self.mycursor.column_names

    def set_col_labels(self):
        col = self.get_db_column_names()
        print(col)
        self.table.set_column_labels(col)

    def db_show_data(self):
        print('db show data')
        print(self.mycursor)
        # mycursor = self.db.cursor()
        # self.mycursor.execute("SELECT * FROM customers")
        # self.mycursor.execute('SELECT * FROM test')

        self.table.setRowCount(0)
        # self.table.setColumnCount(0)
        self.table.setColumnCount(len(self.get_db_column_names()))

        for row_data in self.mycursor:
            # print('row', row_data)
            row = self.table.rowCount()
            self.table.insertRow(row)
            # if len(row_data) > 100:
            #     self.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(str(stuff))
                self.table.setItem(row, column, item)

    def add_command(self, text):
        print('add')
        print(self.mycursor)
        self.mycursor.execute(text)
        # for x in self.mycursor:  # wyswietli info o db
        #     print(x)




