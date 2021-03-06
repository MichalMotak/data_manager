from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import numpy as np
import pandas as pd

import UpgradedWidgets
import CustomDialogWidgets

from sklearn import pipeline 
from sklearn import impute 
from sklearn import preprocessing

from sklearn.decomposition import PCA 


class PreprocessingWidget(QWidget):
    signal_for_table = pyqtSignal(pd.core.frame.DataFrame)
    signal_for_ml_widget = pyqtSignal(pipeline.Pipeline)

    signal_for_PlotWidget = pyqtSignal(list)

    def __init__(self):
        print('PreprocessingWidget init')
        super(PreprocessingWidget, self).__init__()

        # self.main_layout = QVBoxLayout(self)
        self.main_layout = QGridLayout(self)


        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('Preprocessing')

        # Missing Data

        # df.dropna()
        self.pb_dropna = QPushButton()
        self.pb_dropna.setText('drop NA')
        self.pb_dropna.clicked.connect(self.drop_na)

        self.pb_fillna = QPushButton()
        self.pb_fillna.setText('fill NA')
        self.pb_fillna.clicked.connect(self.fill_na)

        self.l_combobox_fillna_method = UpgradedWidgets.LabelAndCombobox('fillna method')
        self.l_combobox_fillna_method.add_items(['Mean', 'Median', 'Interpolate', 'Constant value'])


        # self.l_rb_PCA = UpgradedWidgets.LabelAndRadioButton('PCA')
        self.l_sb_fillna_value = UpgradedWidgets.LabelAndSpinbox('fillna constant value', double_spinbox=True)
        self.l_sb_fillna_value.set_step(0.01)



        self.pushButton = QPushButton()
        self.pushButton.setText('one hot encoder')
        self.pushButton.clicked.connect(self.one_hot_encoder)

        # self.l_rb_ = UpgradedWidgets.LabelAndRadioButton('one hot encoder')
        self.l_combobox_labels = UpgradedWidgets.LabelAndComboboxCheckable('One Hot Labels', lay_dir = 'Horizontal')


        self.l_combobox_scaler = UpgradedWidgets.LabelAndCombobox('scaler')
        self.l_combobox_scaler.add_items(['Standard', 'MinMax'])

        self.l_rb_PCA = UpgradedWidgets.LabelAndRadioButton('PCA')
        self.l_sb_components = UpgradedWidgets.LabelAndSpinbox('number of components', double_spinbox=True)
        self.l_sb_components.set_step(0.01)
        self.l_sb_components.setToolTip('Float in range [0,1] or Int')



        # self.l_combobox_PCA_labels = UpgradedWidgets.LabelAndCombobox('Predict label for PCA plot')



        self.l_rb_pipeline = UpgradedWidgets.LabelAndRadioButton('create pipeline')


        # self.pb_pipeline = QPushButton()
        # self.pb_pipeline.setText('create pipeline')
        # self.pb_pipeline.clicked.connect(self.create_pipeline)


        self.main_layout.addWidget(self.label)


        self.main_layout.addWidget(self.pb_dropna)
        self.main_layout.addWidget(self.l_combobox_fillna_method)
        self.main_layout.addWidget(self.l_sb_fillna_value)
        self.main_layout.addWidget(self.pb_fillna)


        self.main_layout.addWidget(self.l_combobox_labels)
        self.main_layout.addWidget(self.pushButton)
        self.main_layout.addWidget(self.l_combobox_scaler)


        self.main_layout.addWidget(self.l_rb_PCA)
        self.main_layout.addWidget(self.l_sb_components)

        # self.main_layout.addWidget(self.l_combobox_PCA_labels)


        self.main_layout.addWidget(self.l_rb_pipeline)


        self.setLayout(self.main_layout)




    def set_dataframe(self, df):
        self.dataframe = df

    def set_col_labels(self, col_labels):
        self.col_labels = col_labels
        # self.update_output_combobox()

    def update_output_combobox(self, col_labels):
        self.l_combobox_labels.clear_items()
        self.l_combobox_labels.add_items(col_labels)


    #     self.l_combobox_PCA_labels.clear()
    #     self.l_combobox_PCA_labels.add_items(col_labels)

    def show_information_about_missing_values(self):
        #df.isna().any()
        #df.isna().sum()
        pass

    def drop_na(self):
        print('drop na')

        new_df = self.dataframe.dropna()

        self.emit_signal_for_table(new_df)

    def fill_na(self):
        method = self.l_combobox_fillna_method.get_text()

        if method == 'Default':
            return 0

        elif method == 'Mean':
            new_df = self.dataframe.fillna(self.dataframe.mean())

        elif method == 'Median':
            new_df = self.dataframe.fillna(self.dataframe.median())

        elif method == 'Interpolate':
            new_df = self.dataframe.interpolate()

        elif method == 'Constant value':
            value = self.l_sb_fillna_value.get_value()
            new_df = self.dataframe.fillna(value)



        # dff.where(pd.notna(dff), dff.mean(), axis="columns")
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html

        self.emit_signal_for_table(new_df)

    def button(self):
        print('x')

        impute_ = impute.SimpleImputer()

        scaler = preprocessing.StandardScaler()
        scaler2 = preprocessing.MinMaxScaler()

        pipe = pipeline.Pipeline([('impute', impute_), ('scaler', scaler), ('scaler2', scaler2)])

        X_data = self.dataframe.values

        new = pipe.fit_transform(X_data)
        print(new)
        print(type(new))

        self.emit_signal_for_table(new)

        # print(new)


    def one_hot_encoder(self):
        print('one_hot_encoder')
        labels = self.l_combobox_labels.get_text()
        labels = list(labels.split(', '))
        print(labels)
        print(type(labels))
        # self.emit_signal_for_preprocessing_widget([1,2,3])

        new_df = pd.get_dummies(data = self.dataframe, prefix = labels, prefix_sep='_',
               columns = labels,
               drop_first = True,
               dtype='int8')
        self.emit_signal_for_table(new_df)


    def get_scalers_objects(self):
        print('get_scalers_objects')
        scaler_name = self.l_combobox_scaler.get_text()

        if scaler_name == 'Standard':
            scaler = preprocessing.StandardScaler()
        elif scaler_name == 'MinMax':
            scaler = preprocessing.MinMaxScaler()
        return scaler

    def get_imputer(self):
        imputer = impute.SimpleImputer()
        return imputer



    def pipe(self):

        if self.l_rb_pipeline.get_state():

            imputer = impute.SimpleImputer()
            scaler = self.get_scalers_objects()

            print('scaler : ', scaler)
            print('imputer : ', imputer)

            if self.l_rb_PCA.get_state():
                n_comp = self.l_sb_components.get_value()
                print('n_comp: ', n_comp)

                if (n_comp >= 0.0 and n_comp <= 1.0) or n_comp.is_integer():
                    if n_comp.is_integer():
                        n_comp = int(n_comp)
                    pca = PCA(n_components=n_comp)
                    pipe = pipeline.Pipeline( [('imputer', imputer), ('scaler', scaler), ('PCA', pca)] )
                else:
                    d = CustomDialogWidgets.CustomMessageBoxWarning('n_components must be Float in range [0,1] or Int')
                    return 0

            else:
                pipe = pipeline.Pipeline( [('imputer', imputer), ('scaler', scaler)] )

            self.emit_signal_for_ml_widget(pipe)

        else:
            imputer = impute.SimpleImputer()
            pipe = pipeline.Pipeline([('imputer', imputer)])
            self.emit_signal_for_ml_widget(pipe)

    @pyqtSlot()
    def emit_signal_for_table(self, df):
        print('emit_signal_for_table ', df)
        self.signal_for_table.emit(df)
    
    @pyqtSlot(pd.core.frame.DataFrame)
    def get_signal_from_table(self, dataframe):
        print("signal_for_table ")
        print(dataframe.shape)
 
        self.set_dataframe(dataframe)
        self.update_output_combobox(col_labels = list(dataframe.columns))
        self.raise_()

    @pyqtSlot()
    def emit_signal_for_ml_widget(self, pipe):
        print('emit_signal_ml_widget ', pipe)
        self.signal_for_ml_widget.emit(pipe)

    @pyqtSlot()
    def get_signal_from_preprocessing_widget(self):
        print('signal_from_preprocessing_widget')
        # self.signal_for_ml_widget.emit(x)
        self.pipe()
        self.raise_()



    # Emit PCA PLOT FOR Plot WIDGET

    @pyqtSlot()
    def emit_signal_for_PlotWidget(self, list):
        print('emit_signal_for_plot_widget ', list)
        self.signal_for_PlotWidget.emit(list)