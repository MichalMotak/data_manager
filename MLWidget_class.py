from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from UpgradedWidgets import *
from globals_ import *
from TabClassificationClasses import *
from TabRegressionClasses import *

import UpgradedWidgets


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import auc, accuracy_score, roc_auc_score, roc_curve, precision_score, recall_score, f1_score, confusion_matrix, classification_report, plot_confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, cross_validate
from sklearn import pipeline 



class TabClassification(QWidget):
    def __init__(self):
        super(TabClassification, self).__init__()

        # self.main_layout = QVBoxLayout(self)

        self.main_layout = QVBoxLayout(self)
        self.name = 'Classification'
        self.frame = QFrame()

        self.groupBox = QGroupBox("")

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.create_layout()
        self.frame.setLayout(self.lay2)


        self.bottom_layout = QVBoxLayout(self)
        self.create_bottom_layout()

        self.main_layout.addWidget(self.frame)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.setLayout(self.main_layout)

    def create_layout(self):
        self.lay2 = QVBoxLayout()

        self.formLayout = QFormLayout()

        self.groupBox.setLayout(self.formLayout)

        self.create_widgets()

        self.formLayout.addRow(self.radiobutton, self.w)
        self.formLayout.addRow(self.radiobutton2, self.w2)
        self.formLayout.addRow(self.radiobutton3, self.w3)

        self.scroll.setWidget(self.groupBox)

        self.lay2.addWidget(self.scroll)

    def create_widgets(self):
        self.w = RandomForestClassWidget('Random Forest')
        self.w2 = DecisionTreeClassWidget('Decision Tree')
        self.w3 = SupportVectorMachineClassWidget('SVM')
        self.w4 = DecisionTreeClassWidget('Decision Tree')

        self.radiobutton = QRadioButton("")
        self.radiobutton.widget = self.w
        self.radiobutton.type = 'Random Forest'
        self.radiobutton.toggled.connect(self.radio_button_clicked)

        self.radiobutton2 = QRadioButton("")
        self.radiobutton2.widget = self.w2
        self.radiobutton2.type = 'Decision Tree'
        self.radiobutton2.toggled.connect(self.radio_button_clicked)

        self.radiobutton3 = QRadioButton("")
        self.radiobutton3.widget = self.w3
        self.radiobutton3.type = 'SVM'
        self.radiobutton3.toggled.connect(self.radio_button_clicked)


        self.radiobutton4 = QRadioButton("")
        self.radiobutton4.widget = self.w4
        self.radiobutton4.type = 'Decision Tree'
        self.radiobutton4.toggled.connect(self.radio_button_clicked)


        self.widgets_list = [self.w, self.w2, self.w3, self.w4]
        self.radio_buttons_list = [self.radiobutton, self.radiobutton2, self.radiobutton3, self.radiobutton4]
        self.widgets_types_list = [w.type for w in self.radio_buttons_list]
        self.radiobutton.setChecked(True)

    def create_bottom_layout(self):
        self.l_combobox_metrics = UpgradedWidgets.LabelAndComboboxCheckable('Metrics')
        self.l_combobox_metrics.add_items(class_metrics_list)
        self.l_combobox_prediction = UpgradedWidgets.LabelAndCombobox('Prediction output')

        multiclass_types_list = ['OneVsRest', 'OneVsOne']
        self.l_combobox_multiclass_type = UpgradedWidgets.LabelAndCombobox('Multiclass Classification type', lay_dir='Horizontal')
        self.l_combobox_multiclass_type.add_items(multiclass_types_list)

        self.bottom_layout.addWidget(self.l_combobox_metrics)
        self.bottom_layout.addWidget(self.l_combobox_prediction)
        self.bottom_layout.addWidget(self.l_combobox_multiclass_type)

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


    def predict(self, current_widget, tab, cv_type, number, pipe):
        print('class predict')
        metrics = self.l_combobox_metrics.get_text()
        metrics = list(metrics.split(', '))
        predict_label = self.l_combobox_prediction.get_text()
        multiclass_type = self.l_combobox_multiclass_type.get_text()
        print(metrics)

        current_widget.predict(tab, predict_label, cv_type, number, metrics, multiclass_type, pipe = pipe)

    def update_outputcombobox(self, col_labels):
        self.l_combobox_prediction.clear()
        self.l_combobox_prediction.add_items(col_labels)

    def get_parameters(self):
        print('get parameters ' + self.name)
        metrics = self.l_combobox_metrics.get_text()
        metrics = list(metrics.split(', '))
        predict_label = self.l_combobox_prediction.get_text()
        parameters = predict_label
        return parameters



class TabRegression(TabClassification):
    def __init__(self):
        super(TabRegression, self).__init__()

    def create_widgets(self):
        print('add widgets tab regression')
        self.name = 'Regression'
        self.w = TabDecisionTreeReg('Decision Tree')
        self.w2 = TabRandomForestReg('Random Forest')
        self.w3 = TabLinearReg('Linear Models')

        self.radiobutton = QRadioButton("")
        self.radiobutton.widget = self.w
        self.radiobutton.type = 'Random Forest'
        self.radiobutton.toggled.connect(self.radio_button_clicked)

        self.radiobutton2 = QRadioButton("")
        self.radiobutton2.widget = self.w2
        self.radiobutton2.type = 'Decision Tree'
        self.radiobutton2.toggled.connect(self.radio_button_clicked)

        self.radiobutton3 = QRadioButton("")
        self.radiobutton3.widget = self.w3
        self.radiobutton3.type = 'Linear'
        self.radiobutton3.toggled.connect(self.radio_button_clicked)

        self.widgets_list = [self.w, self.w2, self.w3]
        self.radio_buttons_list = [self.radiobutton, self.radiobutton2, self.radiobutton3]
        self.widgets_types_list = [w.type for w in self.radio_buttons_list]
        self.radiobutton.setChecked(True)


    def create_layout(self):
        self.lay2 = QVBoxLayout()

        self.formLayout = QFormLayout()

        self.groupBox.setLayout(self.formLayout)

        self.create_widgets()

        self.formLayout.addRow(self.radiobutton, self.w)
        self.formLayout.addRow(self.radiobutton2, self.w2)
        self.formLayout.addRow(self.radiobutton3, self.w3)
        self.scroll.setWidget(self.groupBox)

        self.lay2.addWidget(self.scroll)

    def create_bottom_layout(self):
        self.l_combobox_metrics = LabelAndComboboxCheckable('Metrics')
        self.l_combobox_metrics.add_items(reg_metrics_list)
        self.bottom_layout.addWidget(self.l_combobox_metrics)
        self.l_combobox_prediction = LabelAndCombobox('Prediction output')
        self.bottom_layout.addWidget(self.l_combobox_prediction)
        self.bottom_layout.setContentsMargins(5,5,5,5)

    def predict(self, current_widget, tab, cv_type, number, pipe):
        print('regression predict')
        metrics = self.l_combobox_metrics.get_text()
        metrics = list(metrics.split(', '))
        predict_label = self.l_combobox_prediction.get_text()
        print(metrics)

        current_widget.predict(tab, predict_label, cv_type, number, metrics, pipe = pipe)


class MLWidget(QWidget):
    signal_for_results_table = pyqtSignal(tuple)
    signal_for_preprocessing_widget = pyqtSignal()

    def __init__(self):
        print('subwindow init')
        QWidget.__init__(self)

        self.UI()

    def UI(self):
        print('ml widget createed')
        self.main_layout = QVBoxLayout(self)

        # =============== Creating QTabWidget ===============

        self.tabs = QTabWidget(self)
        self.tab1 = TabClassification()
        self.tab2 = TabRegression()
        self.tabs.addTab(self.tab1, "Classification")
        self.tabs.addTab(self.tab2, "Regression")


        # =============== Bottom Frame and Layout ===============

        # self.frame_MLWidget_lower = QFrame()
        # self.frame_MLWidget_lower.setStyleSheet(" ")
        self.layout_MLWidget_lower = QGridLayout()

        # =============== Bottom Frame and Layout Widgets ===============

        self.b_predict = QPushButton(self)
        self.b_predict.setText('predict')
        self.b_predict.clicked.connect(self.predict)


        cv_types_list = ['Cross Validation', 'K-Fold']
        self.l_combobox_cv_type = UpgradedWidgets.LabelAndCombobox('Validation type', lay_dir='Vertical')
        self.l_combobox_cv_type.add_items(cv_types_list)

        self.sp_number = UpgradedWidgets.LabelAndSpinbox('Number', lay_dir='Vertical')

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.l_combobox_cv_type)
        self.hbox.addWidget(self.sp_number)

        self.layout_MLWidget_lower.addLayout(self.hbox, 0, 0)
        self.layout_MLWidget_lower.addWidget(self.b_predict, 1, 0)
        # self.frame_MLWidget_lower.setLayout(self.layout_MLWidget_lower)


        # =============== Main Layout adding Widgets  ===============
        self.main_layout.addWidget(self.tabs)
        self.main_layout.addLayout(self.layout_MLWidget_lower)
 
        # =============== Class Constans  ===============
        self.pipeline = None
        self.number_of_tabs = self.tabs.count()
        self.list_of_tabs = [self.tabs.widget(index) for index in range(self.number_of_tabs)]



    # =============== SIGNALS ===============

    @pyqtSlot(str)
    def get_signal_from_results_table(self, message):
        print("signal_from_preprocess_table " + message)
        self.raise_()

    @pyqtSlot()
    def emit_signal_for_results_table(self):
        """ Emit signal for Results Table. Get parameters from get_parameters() and send them.
        """
        parameters = self.get_parameters()
        # print('emit_signal_for_right_table ', parameters)
        self.signal_for_results_table.emit(parameters)


    @pyqtSlot(pd.core.frame.DataFrame)
    def get_signal_from_table(self, df):
        """ Receive dataframe from TableWidget. Call set_col_labels() and set_dataframe() 
        Args:
            df ([pd.core.frame.DataFrame]): [description]
        """
        # print("signal_from_table ", df)
        self.set_col_labels(list(df.columns))
        self.set_dataframe(df)
        self.raise_()


    @pyqtSlot()
    def emit_signal_for_preprocessing_widget(self):
        """ Emit signal for Preprocessing Widget to receive signal.
        """
        print("signal_for_preprocessing widget ")
        self.signal_for_preprocessing_widget.emit()

    
    @pyqtSlot(pipeline.Pipeline)
    def get_signal_from_preprocessing_widget(self, pipeline):
        """ Receive pipeline from Preprocessing Widget and set attribute self.pipeline
        Args:
            pipeline ([sklearn.pipeline.Pipeline]): receive pipeline from Preprocessing Widget
        """

        # print("signal_from_preprocessing widget ", pipeline)
        self.pipeline = pipeline
        self.raise_()


    # ======================= METHODS ==============================

    def get_parameters(self):
        print('get parameters')

        # parameters from layout_MLWidget_lower
        cv_type = self.l_combobox_cv_type.get_text()
        number = self.sp.get_value()

        # Tab and Widget, . Classification, Recision Tree
        _ , current_tab = self.which_tab_is_opened()
        current_tab_name = current_tab.name
        _, current_widget = self.which_widget_is_opened()
        current_widget_name = current_widget.name

        lens = []

        parameters = [current_tab_name, current_widget_name, cv_type, number]
        parameters_labels = ['Algorithm Type', 'Algoritm name', 'CV type', 'CV number par']
        lens.append(len(parameters_labels)+1)

        # parameters from Tab
        tab_par = current_tab.get_parameters()
        parameters_labels.append('Precition')
        parameters.append(tab_par)
        print('tab par: ', tab_par)

        # parameters from Widget
        widget_par, widget_labels = current_widget.get_parameters(as_list=True, return_labels = True)
        parameters_labels.extend(widget_labels)
        parameters.extend(widget_par)
        print('widget par :', widget_par)

        # scores from Widget
        scores_dict = current_widget.get_last_results()
        print('d')
        scores_keys = list(scores_dict.keys())
        scores_values = list(scores_dict.values())
        print(scores_dict)
        # print(scores_keys)
        # print(scores_values)
        parameters_labels.extend(scores_keys)
        parameters.extend(scores_values)

        print(parameters)

        lens.append(len(widget_labels))
        lens.append(len(scores_keys))
        # lens = [len(parameters_labels)+1, len(widget_labels), len(scores_keys)]
        print('lens : ', lens)

        return (parameters, parameters_labels, lens)

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

        try:
            _, current_tab = self.which_tab_is_opened()
            _, current_widget = self.which_widget_is_opened()

            cv_type = self.l_combobox_cv_type.get_text()
            number = self.sp.get_value()


            # jeśli trzeba coś dodać w predict dla danego tabu to 1 wybór
            print('przed pred')


            self.emit_signal_for_preprocessing_widget() # signal to get self.pipeline
            current_tab.predict(current_widget, self.dataframe, cv_type, number, self.pipeline)
            print(' po predykcji current tabu')
            # current_tab.current_widget.predict(tab, out)

            # check if its needed to update Right Table with results
            self.emit_signal_for_right_table()

        except Exception as e:
            print(e)



    def set_dataframe(self, df):
        self.dataframe = df

    def set_col_labels(self, col_labels):
        self.col_labels = col_labels
        self.update_output_combobox()

    def update_output_combobox(self):
        print(self.list_of_tabs)
        for tab in self.list_of_tabs:
            tab.update_outputcombobox(self.col_labels)