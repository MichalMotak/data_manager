from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Upgraded_widgets import *
from metrics import *
from Tab_Classification_classes import *
from Tab_Regression_classes import *

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import auc, accuracy_score, roc_auc_score, roc_curve, precision_score, recall_score, f1_score, confusion_matrix, classification_report, plot_confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, cross_validate


# # new check-able combo box
# class CheckableComboBox(QComboBox):
#
#     # https://www.geeksforgeeks.org/pyqt5-adding-action-to-combobox-with-checkable-items/
#     # https://www.geeksforgeeks.org/pyqt5-checkable-combobox-showing-checked-items-in-textview/



class Tab_classification(QWidget):
    def __init__(self):
        super(Tab_classification, self).__init__()

        # self.main_layout = QVBoxLayout(self)

        self.main_layout = QVBoxLayout(self)
        self.height, self.width,  = 100, 100
        self.name = 'Classification'
        self.frame = QFrame()
        # self.frame.setStyleSheet("QFrame {background-color: rgb(255, 255, 255);"
        #                         "border-width: 1;"
        #                         "border-radius: 3;"
        #                         "border-style: solid;"
        #                         "border-color: rgb(50,50,50)}"
        #                         )
        # self.frame.setStyleSheet("")
        self.groupBox = QGroupBox("Group Box")
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_layout.addWidget(self.frame)


        self.lay2 = QVBoxLayout(self)

        self.formLayout = QFormLayout()

        self.groupBox.setLayout(self.formLayout)

        self.create_widgets()

        self.formLayout.addRow(self.radiobutton, self.w)
        self.formLayout.addRow(self.radiobutton2, self.w2)
        self.scroll.setWidget(self.groupBox)

        self.lay2.addWidget(self.scroll)
        self.frame.setLayout(self.lay2)
        self.bottom_layout = QVBoxLayout(self)



        self.create_bottom_layout()

        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

    def create_widgets(self):
        self.w = Tab_Random_Forest_Clas()
        self.w2 = Tab_Decision_Tree_Clas()

        self.radiobutton = QRadioButton("")
        self.radiobutton.widget = self.w
        self.radiobutton.type = 'Random Forest'
        self.radiobutton.toggled.connect(self.radio_button_clicked)
        # self.radiobutton.setChecked(True)

        self.radiobutton2 = QRadioButton("")
        self.radiobutton2.widget = self.w2
        self.radiobutton2.type = 'Decision Tree'
        self.radiobutton2.toggled.connect(self.radio_button_clicked)

        self.widgets_list = [self.w, self.w2]
        self.radio_buttons_list = [self.radiobutton, self.radiobutton2]
        self.widgets_types_list = [w.type for w in self.radio_buttons_list]
        self.radiobutton.setChecked(True)

    def create_bottom_layout(self):
        self.l_combobox_metrics = Label_and_combobox_checkable('Metrics')
        self.l_combobox_metrics.addItems(class_metrics_list)

        self.bottom_layout.addWidget(self.l_combobox_metrics)


        self.l_combobox_prediction = Label_and_combobox('Prediction output')
        self.bottom_layout.addWidget(self.l_combobox_prediction)


        self.bottom_layout.setContentsMargins(5,5,5,5)

    def which_radio_button_is_on(self):
        output = [(index, button) for index, button in enumerate(self.radio_buttons_list) if button.isChecked()]
        return output[0]

    def radio_button_clicked(self):

        radioButton = self.sender()
        widget_on = radioButton.widget
        widget_type = radioButton.type

        if radioButton.isChecked():
            print('xd')
            print(widget_on, widget_type)

            for w,t in zip(self.widgets_list, self.widgets_types_list):
                print(w,t)
                if t == widget_type:
                    w.setEnabled(True)
                else:
                    w.setEnabled(False)


    def predict(self, current_widget, tab, cv_type, number):
        print('class predict')
        metrics = self.l_combobox_metrics.getText()
        metrics = list(metrics.split(', '))
        predict_label = self.l_combobox_prediction.getText()
        print(metrics)
        # print(cv_type)
        # print(predict_label)
        # def predict(self, table, Y_index, cv_type, number, metrics):

        current_widget.predict(tab,  predict_label, cv_type, number, metrics)

    def update_outputcombobox(self, col_labels):
        self.l_combobox_prediction.clear()
        self.l_combobox_prediction.addItems(col_labels)


class Tab_Regression(Tab_classification):
    def __init__(self):
        super(Tab_Regression, self).__init__()

    def create_widgets(self):
        print('add widgets tab regression')
        self.name = 'Regression'
        self.w = Tab_Decision_Tree_Reg()
        self.w2 = Tab_Random_Forest_Reg()

        self.radiobutton = QRadioButton("")
        self.radiobutton.widget = self.w
        self.radiobutton.type = 'Random Forest'
        self.radiobutton.toggled.connect(self.radio_button_clicked)
        # self.radiobutton.setChecked(True)

        self.radiobutton2 = QRadioButton("")
        self.radiobutton2.widget = self.w2
        self.radiobutton2.type = 'Decision Tree'
        self.radiobutton2.toggled.connect(self.radio_button_clicked)

        self.widgets_list = [self.w, self.w2]
        self.radio_buttons_list = [self.radiobutton, self.radiobutton2]
        self.widgets_types_list = [w.type for w in self.radio_buttons_list]
        self.radiobutton.setChecked(True)

    def create_bottom_layout(self):
        self.l_combobox_metrics = Label_and_combobox_checkable('Metrics')
        self.l_combobox_metrics.addItems(reg_metrics_list)
        self.bottom_layout.addWidget(self.l_combobox_metrics)
        self.l_combobox_prediction = Label_and_combobox('Prediction output')
        self.bottom_layout.addWidget(self.l_combobox_prediction)
        self.bottom_layout.setContentsMargins(5,5,5,5)

    def predict(self, current_widget, tab, cv_type, number):
        print('regression predict')
        metrics = self.l_combobox_metrics.getText()
        metrics = list(metrics.split(', '))
        predict_label = self.l_combobox_prediction.getText()
        print(metrics)
        # print(cv_type)
        # print(predict_label)
        # def predict(self, table, Y_index, cv_type, number, metrics):

        current_widget.predict(tab,  predict_label, cv_type, number, metrics)


class MLWidget(QWidget):
    signal_for_right_table = pyqtSignal(list)

    def __init__(self):
        print('subwindow init')
        QWidget.__init__(self)
        self.left, self.top =  300, 200
        self.width, self.height = 500, 200
        self.UI()

    def UI(self):
        print('ml widget createed')


        self.main_layout = QVBoxLayout(self)
        # self.frame_2 = QFrame(self)

        self.tabs = QTabWidget(self)
        self.tab1 = Tab_classification()
        self.tab2 = Tab_Regression()

        self.tabs.addTab(self.tab1, "Classification")
        self.tabs.addTab(self.tab2, "Regression")

        self.main_layout.addWidget(self.tabs)

        # self.bottom_layout = QVBoxLayout(self)
        # self.pushButton2 = QPushButton(self)
        # self.pushButton2.setText('tab2')
        # self.bottom_layout.addWidget(self.pushButton2)
        #
        # self.main_layout.addLayout(self.bottom_layout)

        self.frame_MLWidget_lower = QFrame()
        self.frame_MLWidget_lower.setStyleSheet(" ")

        # =============== Layout dodatkowy na sam dół =====================
        self.layout_MLWidget_lower = QGridLayout()


        self.b_predict = QPushButton(self)
        self.b_predict.setText('predict')
        self.b_predict.clicked.connect(self.predict)


        # self.layout_MLWidget_lower.addWidget(self.label222)

        cv_types_list = ['Cross Validation', 'K-Fold']
        self.l_combobox_cv_type = Label_and_combobox('Cross Validation type')
        self.l_combobox_cv_type.addItems(cv_types_list)

        self.sp = Label_and_spinbox('number', 'Vertical')

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.l_combobox_cv_type)
        self.hbox.addWidget(self.sp)
        self.layout_MLWidget_lower.addLayout(self.hbox, 0,0)

        self.layout_MLWidget_lower.addWidget(self.b_predict, 1,0)

        self.frame_MLWidget_lower.setLayout(self.layout_MLWidget_lower)
        self.main_layout.addWidget(self.frame_MLWidget_lower)

        self.number_of_tabs = self.tabs.count()
        self.list_of_tabs = [self.tabs.widget(index) for index in range(self.number_of_tabs)]
        # print(self.tabs.widget(0))

        self.show()

    # ======================= SIGNALS ==============================

    @pyqtSlot(str)
    def get_signal_for_right_table(self, message):
        print("signal_for_right_table " + message)
        self.raise_()

    @pyqtSlot()
    def emit_signal_for_right_table(self):
        parameters = self.get_parameters()
        print('emit_signal_for_right_table ', parameters)
        self.signal_for_right_table.emit(parameters)



    # ======================= METHODS ==============================

    def get_parameters(self):
        print('get parameters')

        # parameters from layout_MLWidget_lower
        cv_type = self.l_combobox_cv_type.getText()
        number = self.sp.get_value()

        # Tab and Widget, . Classification, Recision Tree
        _ , current_tab = self.which_tab_is_opened()
        current_tab_name = current_tab.name
        _, current_widget = self.which_widget_is_opened()
        current_widget_name = current_widget.name

        # parameters from Widget
        current_widget.get_parameters()

        parameters = [cv_type, number, current_tab_name, current_widget_name]
        print(parameters)
        return parameters

    def which_tab_is_opened(self):
        # this function returns index and object of current opened Tab

        current_tab_index = self.tabs.currentIndex()
        current_tab_obj = self.list_of_tabs[current_tab_index]
        return current_tab_index, current_tab_obj


    def which_widget_is_opened(self):

        current_tab_index, current_tab = self.which_tab_is_opened() # index of opened tab
        print(current_tab_index, current_tab)

        current_widgets_list = current_tab.widgets_list # list of widgets in opened tab

        rb_ind, rb_obj = current_tab.which_radio_button_is_on() # check which radio button is checked (index, object)
        print(rb_ind, rb_obj)


        current_widget_index = rb_ind
        current_widget = current_widgets_list[rb_ind]  # current widget
        print(current_widget)
        print(current_widget.name)

        return current_widget_index, current_widget

    def predict(self):
        # Emit signal with prediction results etc.
        self.emit_signal_for_right_table()

        # try:
        #     current_tab_index, current_tab = self.which_tab_is_opened()
        #     current_widget_index, current_widget = self.which_widget_is_opened()
        #
        #     cv_type = self.l_combobox_cv_type.getText()
        #     number = self.sp.get_value()
        #
        #     # jeśli trzeba coś dodać w predict dla danego tabu to 1 wybór
        #     current_tab.predict(current_widget, self.dataframe, cv_type, number)
        #     # current_tab.current_widget.predict(tab, out)
        #
        #     # check if its needed to update Right Table with results
        #
        #
        # except:
        #     pass

    def set_dataframe(self, df):
        self.dataframe = df

    def set_col_labels(self, col_labels):
        self.col_labels = col_labels

        self.update_output_combobox()
    #     self.update_tab_classification(col_labels)
    #
    # def update_tab_classification(self, col_labels):
    #     current_tab_index, current_tab = self.which_tab_is_opened()
    #
    #     if current_tab_index == 0: # classification
    #         current_tab.update_outputcombobox(col_labels)

    def update_output_combobox(self):
        print(self.list_of_tabs)
        for tab in self.list_of_tabs:
            tab.update_outputcombobox(self.col_labels)