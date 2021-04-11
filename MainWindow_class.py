import sys
from PyQt5 import QtCore
# from PyQt5.QtWidgets import QDesktopWidget,\
#     QSplitter, QGridLayout, QAction, QApplication, QMainWindow, \
#     QPushButton,QMessageBox, QCheckBox, QFileDialog, QLabel,QSizePolicy, QLineEdit, QComboBox

import pandas as pd
import csv

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


import Database_class
import TableWidget_class
import MLWidget_class
import ResultsTable_class
import PlotWidget_class
import CustomDialogWidgets
import PreprocessingWidget_class
import ToolBarClass

# from CustomDialogWidgets import CustomMessageBoxInformation, CustomMessageBoxWarning

import qdarkstyle


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.left, self.top  = 100, 100
        self.height, self.width,  = 1000, 1600

        # self.setStyleSheet(qdarkstyle.load_stylesheet())

        self.UI()
        self.show()

    def UI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Data Manager')
        self.move_to_center()


        # layout = QGridLayout(self)
        self._main = QWidget()
        self.setCentralWidget(self._main)
        # self.setCentralWidget(self.table)
        # self.canv = PlotCanvas(self.table, 5, 3)

        self.xxxx = 34
        self.toolbarBox = ToolBarClass.MyToolBarClass()
        self.toolbarBox.setOrientation(QtCore.Qt.Vertical)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbarBox)

        # self.toolbarBox.open_action.triggered.connect(self.fun3)


        # font = self.toolbarBox.font()
        # font.setPointSize(18)
        # self.toolbarBox.setFont(font)

        # self.toolbarBox.actionTriggered[QAction].connect(self.toolbtnpressed)
        # self.open_action.triggered.connect(self.fun_open)

        # "border-width: 1;"
        # "border-radius: 1;"
        # "border-style: solid;"
        # "border-color: rgb(100,57,0);"
        # "background-color: #ABABAB;"



        self.menubar = QMenuBar()
        self.menubar.setStyleSheet(

                                          "padding: 2px;"
                                          "font-size: 26px;}"
                                      )


        self.setMenuBar(self.menubar)
        
        # ToolBar signals

        self.toolbarBox.load_file_action.triggered.connect(lambda:self.load_file_act())
        self.toolbarBox.save_file_action.triggered.connect(lambda: self.save_file_act())


        self.toolbarBox.set_layout_action_data.triggered.connect(self.set_layout_checked_action)
        self.toolbarBox.set_layout_action_plot.triggered.connect(self.set_layout_checked_action)
        self.toolbarBox.set_layout_action_ML.triggered.connect(self.set_layout_checked_action)

        self.toolbarBox.manage_layout_action_table.triggered.connect(self.manage_layout_checked_action)
        self.toolbarBox.manage_layout_action_MLWidget.triggered.connect(self.manage_layout_checked_action)
        self.toolbarBox.manage_layout_action_right_table.triggered.connect(self.manage_layout_checked_action)
        self.toolbarBox.manage_layout_action_preprocessing_widget.triggered.connect(self.manage_layout_checked_action)
        self.toolbarBox.manage_layout_action_plot.triggered.connect(self.manage_layout_checked_action)


        # ===========================================

        self.main_layout = QVBoxLayout()
        self._main.setLayout(self.main_layout)

        # ================== Menu Database ==================

        self.Database_menu = self.menubar.addMenu('&Database')
        self.add_db_action = QAction('add database')
        self.Database_menu.addAction(self.add_db_action)
        self.add_db_action.triggered.connect(lambda: self.create_subwindow_subw())


        # ================== Tables Widgets ==================

        self.table = TableWidget_class.TableWidget(20, 5)
        self.table.customContextMenuRequested.connect(self.generateMenu)
        self.table.viewport().installEventFilter(self)

        self.table.horizontalHeader().customContextMenuRequested.connect(self.generateMenu_hor)
        self.table.horizontalHeader().installEventFilter(self)

        print('eeee', self.table.horizontalHeader().sectionsClickable())



        self.table_describe = TableWidget_class.TableWidget(5,3)
        self.table_describe.hide()

        # ================== Frame and Layout Preprocessing Widget ==================
        
        self.frame_preproc_widget = QFrame()
        self.layout_preproc_widget = QVBoxLayout()

        self.preproc_widget = PreprocessingWidget_class.PreprocessingWidget()
        self.layout_preproc_widget.addWidget(self.preproc_widget)
        self.frame_preproc_widget.setLayout(self.layout_preproc_widget)


        # ================== Frame, Layout and Spliiter Left  ==================
 
        self.splitter_left = QSplitter(Qt.Vertical)

        self.splitter_left.addWidget(self.table)
        self.splitter_left.addWidget(self.table_describe)
        self.splitter_left.addWidget(self.frame_preproc_widget)

        index = self.splitter_left.indexOf(self.table_describe)
        self.splitter_left.setCollapsible(index, False)

        self.splitter_left.setStretchFactor(0, 10)
        self.splitter_left.setStretchFactor(1, 1)


        self.frame_left = QFrame(self)
        self.frame_left.setStyleSheet("QFrame {"
                                      "border-width: 1;"
                                      "border-radius: 3;"
                                      "border-style: solid;"
                                      "border-color: rgb(0,0,0)}"
                                      )

        self.layout_left = QVBoxLayout()
        self.layout_left.addWidget(self.splitter_left)

        self.frame_left.setLayout(self.layout_left)
        self.frame_left.setMinimumWidth(self.width/6)



        # ================== Frame and Layout Plot Widget ==================

        self.frame_PlotWidget = QFrame(self)
        self.frame_PlotWidget.setStyleSheet("QFrame {"
                                "border-width: 1;"
                                "border-radius: 3;"
                                "border-style: solid;"
                                "border-color: rgb(0,0,0)}"
                                )
        self.frame_PlotWidget.setMinimumWidth(self.width / 6)

        self.layout_PlotWidget = QVBoxLayout(self)
        self.plot_widget = PlotWidget_class.PlotWidget(self.table)

        self.layout_PlotWidget.addWidget(self.plot_widget)

        self.frame_PlotWidget.setLayout(self.layout_PlotWidget)


        # ================== Frame and Layout ML Widget ==================


        self.frame_MLWidget = QFrame(self)
        self.frame_MLWidget.setStyleSheet("QFrame {"
                                "border-width: 1;"
                                "border-radius: 3;"
                                "border-style: solid;"
                                "border-color: rgb(0,0,0)}"
                                )
        self.layout_MLWidget = QGridLayout()


        self.ml_widget = MLWidget_class.MLWidget()
        self.layout_MLWidget.addWidget(self.ml_widget)

        self.frame_MLWidget.setLayout(self.layout_MLWidget)
        self.frame_MLWidget.setMinimumWidth(self.width / 6)

        self.layout_MLWidget.setContentsMargins(5,5,5,5)


        # ============== Frame and Layout Results Table Widget  ================================
        self.frame_results_table = QFrame(self)

        self.frame_results_table.setStyleSheet("QFrame {"
                                "border-width: 1;"
                                "border-radius: 3;"
                                "border-style: solid;"
                                "border-color: rgb(0,0,0)}"
                                )

        self.layout_results_table = QGridLayout()
        self.results_table = ResultsTable_class.ResultsTableWidget()
        self.layout_results_table.addWidget(self.results_table)
        self.frame_results_table.setLayout(self.layout_results_table)

        # ============== Splitters ================================

        self.splitter_hor = QSplitter(Qt.Horizontal)
        self.splitter_hor.addWidget(self.frame_left)
        self.splitter_hor.addWidget(self.frame_PlotWidget)
        self.splitter_hor.addWidget(self.frame_MLWidget)
        self.splitter_hor.addWidget(self.frame_results_table)

        # self.splitter_vert = QSplitter(Qt.Vertical)
        # self.splitter_vert.addWidget(self.splitter_hor)
        # self.splitter_vert.addWidget(self.frame_results_table)
        #
        # self.splitter_vert.setStretchFactor(0, 10)
        # self.splitter_vert.setStretchFactor(1, 3)
        #
        # self.main_layout.addWidget(self.splitter_vert)
        self.main_layout.addWidget(self.splitter_hor)

        # ============== Connect Signals ================================


        self.results_table.signal_for_ml_widget.connect(self.ml_widget.get_signal_from_results_table)
        self.ml_widget.signal_for_results_table.connect(self.results_table.get_signal_from_ml_widget)


        self.table.signal_for_preprocessing_widget.connect(self.preproc_widget.get_signal_from_table)
        self.preproc_widget.signal_for_table.connect(self.table.get_signal_from_preprocessing_widget)

        self.table.signal_for_ml_widget.connect(self.ml_widget.get_signal_from_table)

        self.preproc_widget.signal_for_ml_widget.connect(self.ml_widget.get_signal_from_preprocessing_widget)
        self.ml_widget.signal_for_preprocessing_widget.connect(self.preproc_widget.get_signal_from_preprocessing_widget)

        self.preproc_widget.signal_for_PlotWidget.connect(self.plot_widget.get_signal_from_preprocessing_widget)

        self.table.signal_for_plot_widget.connect(self.plot_widget.get_signal_from_table_widget)

        self.plot_widget.tab7.signal_for_ml_widget.connect(self.ml_widget.get_signal_from_classplot_widget)

        self.ml_widget.signal_for_classplot_widget.connect(self.plot_widget.tab7.get_signal_from_ML_widget)

        self.plot_widget.tab8.signal_for_ml_widget.connect(self.ml_widget.get_signal_from_classplot_widget)

        self.ml_widget.signal_for_regplot_widget.connect(self.plot_widget.tab8.get_signal_from_ML_widget)


        # ToolBarClass signals

        self.toolbarBox.signal_for_mainwindow.connect(self.receive_toolbar_signals)







        self.set_layout('Data description')


    def manage_layout_checked_action(self):
        """
        This function manages trigger action from self.manage_layout_menu
        """
        print('manage_layout_checked_action')

        # sender PyQt5.QtWidgets.QAction, element of self.manage_layout_menu submenu
        sender = self.sender()
        # sender Text, Plot, Table etc.
        sender_text = sender.text()
        # True/False - sender checked or unchecked
        is_checked = sender.isChecked()

        def fun(obj):
            """ Helping function showing or hiding given object
            Args:
                obj (PyQt5.QtWidgets.QFrame): object 
            """
            if is_checked:
                obj.show()
            else:
                obj.hide()

        if sender_text == 'Plot':
            fun(self.frame_PlotWidget)

        elif sender_text == 'Table':
            fun(self.frame_left)

        elif sender_text == 'ML Widget':
            fun(self.frame_MLWidget)

        elif sender_text == 'Right Table':
            fun(self.frame_results_table)

        elif sender_text == 'Preprocessing Widget':
            print(self.frame_left.isHidden())
            if self.frame_left.isHidden():
                self.frame_left.show()
                self.plot_widget.hide()
            self.frame_preproc_widget.show()
            # fun(self.frame_preproc_widget)

    # Menu for right mouse click on cells in table, with functions

    def eventFilter(self, source, event):
        """ This function handles events 

        Args:
            source (PyQt5.QtWidgets.QWidget): [source]
            event (PyQt5.QtGui.QEvent): [description]

        Returns:
            [type]: [description]
        """
        # print('event')
        # print(source, event)
        # print(type(source), type(event))

        # if event.type  == MouseButtonPress and button is Right Mouse Click on self.table 
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
                self.act1.triggered.connect(lambda: self.plot_widget.add_axis(item, 'x'))
                self.act2.triggered.connect(lambda: self.plot_widget.add_axis(item, 'y'))
                self.act10.triggered.connect(lambda: self.plot_widget.add_hue(item))
                self.submenu_add_plot.addAction(self.act1)
                self.submenu_add_plot.addAction(self.act2)
                self.submenu_add_plot.addAction(self.act10)

                self.submenu_add_data = QMenu('Add data', self)
                self.act3 = QAction('Add column on the right', self.menu, checkable = True)
                self.act4 = QAction('Add row on the bottom', self.menu, checkable=True)
                self.act3.triggered.connect(lambda: self.table.add_col_right(item))
                self.act4.triggered.connect(lambda: self.table.add_row_bottom(item))
                self.submenu_add_data.addAction(self.act3)
                self.submenu_add_data.addAction(self.act4)


                self.submenu_clear_data = QMenu('Clear data',self)
                self.act5 = QAction('Clear column')
                self.act6 = QAction('Clear row')
                self.act5.triggered.connect(lambda: self.table.clear_column(item))
                self.act6.triggered.connect(lambda: self.table.clear_row(item))
                self.submenu_clear_data.addAction(self.act5)
                self.submenu_clear_data.addAction(self.act6)

                self.submenu_del_data = QMenu('Delete data', self)
                self.act7 = QAction('Delete column')
                self.act8 = QAction('Delete row')
                self.act7.triggered.connect(lambda: self.table.delete_column(item))
                self.act8.triggered.connect(lambda: self.table.delete_row(item))
                self.submenu_del_data.addAction(self.act7)
                self.submenu_del_data.addAction(self.act8)

                self.act9 = QAction('Clear cell')
                self.act9.triggered.connect(lambda: self.table.clear_selected_data())
                self.submenu_clear_data.addAction(self.act9)

                self.submenu_sort_data = QMenu('Sort data', self)
                self.act11 = QAction('Sort ascending data')
                self.act11.triggered.connect(lambda: self.table.sort_columns(item, 'ascending'))
                self.submenu_sort_data.addAction(self.act11)

                self.act12 = QAction('Sort descending data')
                self.act12.triggered.connect(lambda: self.table.sort_columns(item, 'descending'))
                self.submenu_sort_data.addAction(self.act12)



                self.menu.addAction(z)
                self.menu.addMenu(self.submenu_add_plot)
                # self.menu.addMenu(self.submenu_add_data)
                self.menu.addMenu(self.submenu_sort_data)
                self.menu.addMenu(self.submenu_clear_data)
                self.menu.addMenu(self.submenu_del_data)


                #menu.exec_(event.globalPos())
        return super(MainWindow, self).eventFilter(source, event)

    # @QtCore.pyqtSlot(QtCore.QPoint)
    # def header_connection(self, source, event):
    #     print('d')
    #     # print(pos)
    #     source = self.sender()
    #     print(source)
    #     event = self.event()
    #     print(event)
    #     if(event.type() == QEvent.MouseButtonPress
    #         and event.buttons() == Qt.RightButton
    #         and source is self.table.horizontal_header):
    #             print('clicked horizontal header')
    #
    #     return super(MainWindow, self).eventFilter(source, event)

    @QtCore.pyqtSlot(QtCore.QPoint)
    def generateMenu(self, pos):
        print("pos======", pos)
        try:
            self.menu.exec_(self.table.mapToGlobal(pos))
        except AttributeError:
            d = CustomDialogWidgets.CustomMessageBoxWarning('Load data to table')

    @QtCore.pyqtSlot(QtCore.QPoint)
    def generateMenu_hor(self, pos):
        print('gen menu hor')

        menu = QMenu(self)
        # self.menu.addAction(item.text())         #(QAction('test'))
        ag = QActionGroup(self, exclusive=True)
        act0 = QAction('default', menu, checkable=True, checked = True)
        # z = ag.addAction(act0)
        menu.addAction(act0)


        menu.exec_(self.table.horizontalHeader().mapToGlobal(pos))


    # ===============================================================================


    def move_to_center(self):
        qtRectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(center_point)
        self.move(qtRectangle.topLeft())


    # def clear_table(self):
    #     print('clear table')
    #     self.table.reset()

    def show_describe(self):
        print('show_describe')

        if not self.table_describe.isVisible(): # jeśli ukryty
            self.table_describe.show()

            try:
                x = self.table.dataframe
                d = x.describe(include='all')
                print(d)
                print(x.dtypes)
                self.table_describe.update_from_df(d)

                row_labels = list(d.index)
                self.table_describe.set_row_labeles(row_labels)
            except AttributeError or ValueError:
                d = CustomDialogWidgets.CustomMessageBoxWarning('Data not found')

        else:
            self.table_describe.hide()

    def button(self):
        self.bbb = Database_class.SubwindowDatabase(self)
        self.hor_lay_left.addWidget(self.bbb)


    def create_subwindow_subw(self):
        print('sub')
        self.subwindow_db = Database_class.SubwindowDatabase(self.table)
        # self.hor_lay_left.addWidget(self.subwindow_db)



    # Functions on self.File_menu actions - load and save file

    def load_file_act(self):
        print('load file action')
        path = QFileDialog.getOpenFileName(self, 'Open CSV', "Text files(.csv)") #"Text files(.csv)"

        self.file_path = path[0]
        if self.file_path != '':
            print(self.file_path)
            self.table.load_file(self.file_path)

            self.ml_widget.set_dataframe(self.table.dataframe)
            # self.ml_widget.set_col_labels(self.table.col_labels)

            self.preproc_widget.set_dataframe(self.table.dataframe)
            # self.preproc_widget.set_col_labels(self.table.col_labels)


            self.plot_widget.clear_axes()
        else:
            print('nie działa dd')


    def save_file_act(self):
        '''
        taking data from self.table and saving to csv file
        '''

        print('save file action')
        path = QFileDialog.getSaveFileName(self, 'Save CSV', "Text files(.csv)")
        if path[0] != '':
            print(self.table.col_labels)
            print(path[0])
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


    def set_layout(self, text):
        print('set layout ', text)
        self.frame_PlotWidget.hide()
        self.frame_left.hide()
        self.frame_preproc_widget.hide()
        self.frame_MLWidget.hide()
        self.frame_results_table.hide()

        self.toolbarBox.manage_layout_action_plot.setChecked(True)
        self.toolbarBox.manage_layout_action_preprocessing_widget.setChecked(True)
        self.toolbarBox.manage_layout_action_MLWidget.setChecked(True)
        self.toolbarBox.manage_layout_action_table.setChecked(True)
        self.toolbarBox.manage_layout_action_right_table.setChecked(True)

        if text == 'Plotting':
            self.frame_PlotWidget.show()
            self.frame_left.show()

            self.toolbarBox.manage_layout_action_preprocessing_widget.setChecked(False)
            self.toolbarBox.manage_layout_action_MLWidget.setChecked(False)
            self.toolbarBox.manage_layout_action_right_table.setChecked(False)

        elif text == 'Data description':
            # pass
            self.frame_left.show()
            self.frame_preproc_widget.show()
            #
            self.toolbarBox.manage_layout_action_plot.setChecked(False)
            self.toolbarBox.manage_layout_action_MLWidget.setChecked(False)
            self.toolbarBox.manage_layout_action_right_table.setChecked(False)

        elif text == 'Machine Learning':

            self.toolbarBox.manage_layout_action_plot.setChecked(False)
            self.toolbarBox.manage_layout_action_preprocessing_widget.setChecked(False)
            self.toolbarBox.manage_layout_action_table.setChecked(False)

            self.frame_MLWidget.show()
            self.frame_results_table.show()


    def set_layout_checked_action(self):
        print('set lay')
        # sender PyQt5.QtWidgets.QAction, element of self.manage_layout_menu submenu
        sender = self.toolbarBox.sender()
        print(sender)
        # sender Text, Plot, Table etc.
        sender_text = sender.text()

        print(sender_text)
        self.set_layout(sender_text)
        self.toolbarBox.update_tab(sender_text)

    def manage_layout_checked_action(self):
        sender_text = self.sender().text()
        print(sender_text)

        def fun(frame):
            print(frame.isHidden())
            if frame.isHidden():
                frame.show()
            else:
                frame.hide()
        if sender_text == 'Table':
            fun(self.frame_left)
        elif sender_text == 'Plot':
            fun(self.frame_PlotWidget)
        elif sender_text == 'ML Widget':
            fun(self.frame_MLWidget)
        elif sender_text == 'Right Table':
            fun(self.results_table)
        elif sender_text == 'Preprocessing Widget':
            fun(self.frame_preproc_widget)


    @pyqtSlot(str)
    def receive_toolbar_signals(self,sender_text):
        print('rec ', sender_text)

        if sender_text == 'Clear Table':
            self.clear_table()

        if sender_text == 'Description Table':
            self.show_describe()


