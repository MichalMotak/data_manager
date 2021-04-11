
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui

class MyToolBarClass(QToolBar):


    signal_for_mainwindow = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        print(self)

        self.setOrientation(QtCore.Qt.Vertical)

        self.open_action = QAction(QtGui.QIcon(), "TEST")

        self.addAction(self.open_action)
        self.addAction(QtGui.QIcon(), "TEST2")

        font = QtGui.QFont()
        font.setPointSize(30)
        self.setFont(font)

        self.setStyleSheet("""
                                  QPushButton{
                                      padding: 6px;
                                      font-size: 22px;}
                            """)
        # self.setStyleSheet("""
        #                        QToolBar {
        #                     background: #eee;
        #                     padding: 0px;
        #                     border: 0px;}
        #
        #                          QAction{
        #                               padding: 6px;
        #                               font-size: 22px;}
        #
        #                         QPushButton{
        #                               padding: 6px;
        #                               font-size: 22px;}
        #
        #                         QToolButton{
        #                         background-color: #59f;
        #                         padding: 10px;}
        #
        #                     """)

        self.manage_layout_menu = QMenu('&Manage layout')
        self.manage_layout_button = QPushButton("Manage \n Layout")
        self.addWidget(self.manage_layout_button)
        self.manage_layout_button.setMenu(self.manage_layout_menu)

        self.manage_layout_action_table = QAction('Table', checkable=True, checked=True)
        self.manage_layout_menu.addAction(self.manage_layout_action_table)
        # self.manage_layout_action_table.triggered.connect(self.manage_layout_checked_action)

        self.manage_layout_action_plot = QAction('Plot', checkable=True, checked=True)
        self.manage_layout_menu.addAction(self.manage_layout_action_plot)
        # self.manage_layout_action_plot.triggered.connect(self.manage_layout_checked_action)

        self.manage_layout_action_MLWidget = QAction('ML Widget', checkable=True, checked=True)
        self.manage_layout_menu.addAction(self.manage_layout_action_MLWidget)
        # self.manage_layout_action_MLWidget.triggered.connect(self.manage_layout_checked_action)

        self.manage_layout_action_right_table = QAction('Right Table', checkable=True, checked=True)
        self.manage_layout_menu.addAction(self.manage_layout_action_right_table)
        # self.manage_layout_action_right_table.triggered.connect(self.manage_layout_checked_action)

        self.manage_layout_action_preprocessing_widget = QAction('Preprocessing Widget', checkable=True, checked=True)
        self.manage_layout_menu.addAction(self.manage_layout_action_preprocessing_widget)
        # self.manage_layout_action_preprocessing_widget.triggered.connect(self.manage_layout_checked_action)

        # ===============================================================


        self.set_layout_menu = QMenu('&Set layout')

        self.set_layout_button  = QPushButton("Choose \n Layout")
        self.addWidget(self.set_layout_button)
        self.set_layout_button.setMenu(self.set_layout_menu)

        self.set_layout_action_data = QAction(QtGui.QIcon('icons/table.png'), 'Data description')
        self.set_layout_menu.addAction(self.set_layout_action_data)

        self.set_layout_action_plot = QAction(QtGui.QIcon('icons/chart.png'), 'Plotting')
        self.set_layout_menu.addAction(self.set_layout_action_plot)

        self.set_layout_action_ML = QAction(QtGui.QIcon('icons/computer.png'), 'Machine Learning')
        self.set_layout_menu.addAction(self.set_layout_action_ML)

        # self.font = self.set_layout_menu.font()
        # self.font.setPointSize(16)
        # self.set_layout_menu.setFont(self.font)

        self.addSeparator()

    def update_tab(self, name):
        print('update tab')

        if name == 'Plotting':
            pass
        elif name == 'Data description':
            self.clear_table = QAction(QtGui.QIcon('icons/table--minus.png'), "Clear Table")
            self.description_table = QAction(QtGui.QIcon(''), "Description Table")

            self.addAction(self.clear_table)
            self.addAction(self.description_table)

            self.clear_table.triggered.connect(self.clear_table_signal)
            self.description_table.triggered.connect(self.clear_table_signal)

            # print(self.addAction.menu())
            print(self.clear_table.menu())

    def clear_table_signal(self):
        print('ct signal')
        sender_text = self.sender().text()
        print(self.sender())
        print(sender_text)
        self.signal_for_mainwindow.emit(sender_text)


    # def manage_layout_checked_action(self):
    #     sender_text = self.sender().text()
    #     print(self.sender())
    #
    #     print(sender_text)
    #     self.signal_for_mainwindow.emit(sender_text)
