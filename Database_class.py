# import mysql.connector as sql
import pandas as pd

from PyQt5.QtWidgets import *

from PyQt5.QtCore import *


class Database():
    def __init__(self, parent, host, user, passwd, database):
        super().__init__()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

        self.x = 111

        self.db = sql.connect(
            host=self.host,  # łaczymy sie jako nasz komputer, localhost
            user=self.user,  # nowy uzytkownik lub ten utworzony przy instalacji
            passwd=self.passwd,  # czyli user, passwd - root
            database=self.database,  # use_pure=True
        )

        self.mycursor = self.db.cursor()

        self.table = parent

        self.commands_list = []

    def handle_commands_list(self):
        print('handle commands list')
        len_ = len(self.commands_list)
        if len_ == 3:
            return None
        else:
            self.commands_list.append(self.command)

    def get_db_column_names(self):
        print('get db column names')
        col_labels = list(self.db_dataframe.columns)
        return col_labels
        # print(self.mycursor)
        # return self.mycursor.column_names


    def set_col_labels(self):
        print('database set col labels')
        # col = list(self.get_db_column_names())
        col = self.get_db_column_names()
        print(col)
        self.table.set_column_labels(col)

    def db_show_data(self):
        print('db show data')
        print(self.mycursor)
        # mycursor = self.db.cursor()
        # self.mycursor.execute("SELECT * FROM customers")

        if self.command[:6] == 'SELECT':
            print('select command')
            self.db_dataframe = pd.read_sql(self.command, self.db)
            self.handle_commands_list()
            print(self.db_dataframe.head(5))
            self.table.update_from_df(self.db_dataframe)
        else:
            print('d')
            self.mycursor.execute(self.command)
            self.handle_commands_list()
            self.db.commit()
            # self.table.setRowCount(0)
            # # self.table.setColumnCount(0)
            # self.table.setColumnCount(len(self.get_db_column_names()))
            #
            # for row_data in self.mycursor:
            #     # print('row', row_data)
            #     row = self.table.rowCount()
            #     self.table.insertRow(row)
            #     # if len(row_data) > 100:
            #     #     self.setColumnCount(len(row_data))
            #     for column, stuff in enumerate(row_data):
            #         item = QTableWidgetItem(str(stuff))
            #         self.table.setItem(row, column, item)

    def add_command(self, text):
        print('add')
        print(text)
        self.command = text
        # print(self.mycursor)
        # self.mycursor.execute(text)



class SubwindowDatabase(QMainWindow):
    def __init__(self, parent):
        print('subwindow init')
        QWidget.__init__(self)
        self.left, self.top =  300, 200
        self.width, self.height = 500, 200

        self.title = "SQL Manager"
        self.table = parent
        self.UI()
        self.show()

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
        self.b_update_table = QPushButton('Execute command', self)
        # self.b_update_table.setGeometry(QRect(0, 0, 100, 30))
        self.b_update_table.clicked.connect(lambda: self.update_table())
        # self.b_update_table.setFixedSize(120, 30)

        self.b_create_db = QPushButton('create database', self)
        # self.b_load_db.setGeometry(QRect(200, 200, 100, 30))
        self.b_create_db.clicked.connect(lambda: self.create_database())
        # self.b_create_db.setFixedSize(120, 30)
        # self.b_create_db.setAlignment(QtCore.Qt.AlignCenter)




        class LE(QLineEdit):

            # klasa jest zrobiona aby keyPressEvent umozliwiał wpisanie znaków do LE

            def __init__(self, parent):
                QLineEdit.__init__(self)
                self.setText('SELECT * FROM customers')
                self.sw = parent

                self.i = 2

            def keyPressEvent(self, event):
                super(LE, self).keyPressEvent(event)
                print(event.key())
                print(self.cursorPosition())
                # 16777235 gora
                # 16777237 dół
                curr_text = self.text()
                print(len(curr_text))
                # if self.cursorPosition() == 0:

                if len(self.sw.database.commands_list) == 3:

                    if event.key() == 16777235: # gorna strzałka
                        print('gora')
                        if (self.i-1) < 0:
                            None
                        else:
                            self.i = self.i - 1

                            text = self.sw.database.commands_list[self.i]
                            print('i, ', self.i)
                            print('text, ', text)
                            self.setText(text)

                            print(self.sw.database.commands_list)

                    elif event.key() == 16777237:
                        print('doł')
                        if (self.i+1) > 2:
                            None
                        else:
                            self.i = self.i + 1

                            text = self.sw.database.commands_list[self.i]
                            print('i, ', self.i)
                            print('text, ', text)
                            self.setText(text)

                            print(self.sw.database.commands_list)





        self.l_com_line = QLabel(self)
        self.l_com_line.setText('Command line')
        # self.el_com_line = QLineEdit(self)
        # self.line.setGeometry(QRect(50, 50, 300, 50))
        # self.el_com_line.setText('SELECT * FROM customers')
        # self.el_com_line.keyPressEvent = self.keyPressEvent
        # self.el_com_line.setFixedSize(500,100)

        self.le_com_line = LE(self)

        self.layout2.addWidget(self.l_com_line)
        self.layout2.addWidget(self.le_com_line)
        self.layout2.addWidget(self.b_create_db)
        self.layout2.addWidget(self.b_update_table)


        self.main_layout.addWidget(self.frame)
        self.main_layout.addWidget(self.frame2)



        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)

        self.setCentralWidget(self.widget)

        self.setFixedSize(self.size())




    # def keyPressEvent(self, event):
    #     print(event.text())
    #
    # def fun1(self):
    #     print('fun1')

    def update_table(self):
        print('update table')
        text = self.le_com_line.text()
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

        self.database = Database(self.table, host=host, user=user,
                                 passwd=passwd, database=database)

