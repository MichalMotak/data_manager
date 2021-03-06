from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UpgradedWidgets import *
from globals_ import *


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import  RandomForestRegressor, AdaBoostRegressor, BaggingRegressor
from sklearn.tree import  DecisionTreeRegressor

from sklearn.metrics import auc, accuracy_score, roc_auc_score, roc_curve, precision_score, recall_score, f1_score, confusion_matrix, classification_report, plot_confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, cross_validate, KFold
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

from TabClassificationClasses import ParentMLWidget, EnsembleClassWidget






class EnsembleRegWidget(EnsembleClassWidget):
    def __init__(self, name):
        super(EnsembleRegWidget, self).__init__(name)
        self.name = name

    def update_pipe(self, reg, pipe):
        print('update_pipe ensemble')

        kind = self.l_combobox_method.get_text()

        if kind == 'AdaBoost':
            parameters_dict = self.get_parameters(as_dict=True)
            ensemble_reg = AdaBoostRegressor(reg, **parameters_dict)

        elif kind == 'Bagging':
            parameters_dict = self.get_parameters(as_dict=True)

            ensemble_reg = BaggingRegressor(reg, **parameters_dict)


        print('pipe ', pipe)
        pipe.steps.append(("ensemble reg", ensemble_reg))

        return pipe


# Tab_Linear_Reg
class TabLinearReg(ParentMLWidget):
    def __init__(self, name):
        super(TabLinearReg, self).__init__(name)

    def create_layout(self):
        self.lay2 = QVBoxLayout()
        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        self.l_combobox_linear_model = LabelAndCombobox('Linear Model')
        self.l_combobox_linear_model.add_items(linear_reg_models)


        self.slider_alpha = ImprovedSlider(0,100, 'Alpha')
        self.slider_alpha.set_float()

        self.slider_l1_ratio = ImprovedSlider(0, 100, 'l1_ratio')
        self.slider_l1_ratio.set_float()

        self.lay2.addWidget(self.label_name)
        self.lay2.addWidget(self.l_combobox_linear_model)
        self.lay2.addWidget(self.slider_alpha)
        self.lay2.addWidget(self.slider_l1_ratio)


        self.l_combobox_linear_model.signal_current_text_changed(self.manage_enability_of_widgets)


    def manage_enability_of_widgets(self):
        
        type_ = self.l_combobox_linear_model.get_text()

        if type_ == 'LinearRegression':
            self.slider_alpha.setEnabled(False)
            self.slider_l1_ratio.setEnabled(False)
 
        elif type_ == 'Ridge' or type_ == 'Lasso':
            self.slider_alpha.setEnabled(True)
            self.slider_l1_ratio.setEnabled(False)
 
        elif type_ == 'ElasticNet':
            self.slider_alpha.setEnabled(True)
            self.slider_l1_ratio.setEnabled(True)
 
    def get_parameters(self, as_list=False, return_labels=False, as_dict=True):
        print('get parameters from ')

        type_ = self.l_combobox_linear_model.get_text()

        if type_ == 'LinearRegression':

            # DO ZMIANY 

            alpha = self.slider_alpha.get_current_value()
            l1_ratio = self.slider_l1_ratio.get_current_value()

            if as_list and return_labels:
                return [alpha,  l1_ratio], [self.slider_alpha.name, self.slider_l1_ratio.name]

            elif not as_list and not as_dict:
                return alpha,  l1_ratio

            elif as_dict:
                parameters = {"alpha" : alpha, "l1_ratio" : l1_ratio}
                return parameters

        elif type_ == 'Ridge' or type_ == 'Lasso':
            alpha = self.slider_alpha.get_current_value()


            if as_list and return_labels:
                return [alpha], [self.slider_alpha.name]
            elif not as_list and not as_dict:
                return alpha

            elif as_dict:
                parameters = {"alpha" : alpha}
                return parameters

        elif type_ == 'ElasticNet':
            alpha = self.slider_alpha.get_current_value()
            l1_ratio = self.slider_l1_ratio.get_current_value()

            if as_list and return_labels:
                return [alpha,  l1_ratio], [self.slider_alpha.name, self.slider_l1_ratio.name]

            elif not as_list and not as_dict:
                return alpha,  l1_ratio

            elif as_dict:
                parameters = {"alpha" : alpha, "l1_ratio" : l1_ratio}
                return parameters

    def get_reg(self):
        print('get model')

        type_ = self.l_combobox_linear_model.get_text()

        parameters = self.get_parameters(as_dict=True)


        # alpha_value, l1_ratio_value = self.get_parameters(as_list=False)
        # print(alpha_value, l1_ratio_value)

        if type_ == 'LinearRegression':
            reg = LinearRegression()
        elif type_ == 'Ridge':
            reg = Ridge(**parameters)
        elif type_ == 'Lasso':
            reg = Lasso(**parameters)
        elif type_ == 'ElasticNet':
            reg = ElasticNet(**parameters)

        return reg


    # def predict(self, table, Y_index, cv_type, number, metrics, pipe):

    #     print(self.name + ' predict')

    #     dataframe = table

    #     X_data = dataframe.drop(Y_index, 1)
    #     Y_data = dataframe[Y_index]


    #     reg = self.get_reg()
    #     print(reg)

    #     print('pipe ', pipe)
    #     pipe.steps.append(("class", reg))
    #     print('create with pipe ', pipe)

    #     if cv_type == 'Cross Validation':
    #         print(cv_type, number, metrics)
    #         scores = cross_validate(pipe, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
    #         self.results(scores, metrics)

    #     elif cv_type == 'K-Fold':
    #         print(cv_type, number, metrics)
    #         cv = KFold(number=number)
    #         scores = cross_validate(pipe, X_data, Y_data, cv=cv, scoring=metrics, return_train_score=True)
    #         self.results(scores, metrics)


# Decision_Tree_Classifier
class TabDecisionTreeReg(ParentMLWidget):
    def __init__(self, name):
        super(TabDecisionTreeReg, self).__init__(name)

    def create_layout(self):
        self.lay2 = QVBoxLayout()
        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        self.l_combobox_criterion = LabelAndCombobox('criterion')
        self.l_combobox_criterion.add_items(decision_tree_reg_criterion_list)


        self.slider_min_samples_split = ImprovedSlider(0, 50, 'min_samples_split')

        self.l_sp_max_depth = LabelAndSpinbox('max depth')

        self.lay2.addWidget(self.label_name)
        self.lay2.addWidget(self.l_sp_max_depth)
        self.lay2.addWidget(self.l_combobox_criterion)
        self.lay2.addWidget(self.slider_min_samples_split)

    def get_parameters(self, as_list=False, return_labels=False, as_dict = True):
        print('get parameters from ')
        # print(self.get_parameters.__name__)
        max_depth_arg = int(self.l_sp_max_depth.get_value())
        min_samples_split_arg = int(self.slider_min_samples_split.get_current_value())
        criterion = self.l_combobox_criterion.get_text()


        if as_list and return_labels:
            return [max_depth_arg, min_samples_split_arg, criterion], [self.l_sp_max_depth.name, self.slider_min_samples_split.name, self.l_combobox_criterion.name]

        elif not as_list and not as_dict:
            return max_depth_arg, min_samples_split_arg, criterion

        elif as_dict:
            parameters_dict = {"max_depth": max_depth_arg, "min_samples_split": min_samples_split_arg, "criterion": criterion}
            return parameters_dict

    def get_reg(self):

        parameters_dict = self.get_parameters(as_dict=True)

        reg = DecisionTreeRegressor(**parameters_dict)

        return reg


    # def predict(self, table, Y_index, cv_type, number, metrics, pipe):

    #     print(self.name + ' predict')

    #     print(Y_index)
    #     dataframe = table

    #     X_data = dataframe.drop(Y_index, 1)
    #     Y_data = dataframe[Y_index]

    #     # max_depth_arg, min_samples_split_arg, criterion = self.get_parameters(as_list=False)
    #     reg = self.get_reg()

    #     print('pipe ', pipe)
    #     pipe.steps.append(("class", reg))
    #     print('create with pipe ', pipe)

    #     if cv_type == 'Cross Validation':
    #         print(type(metrics))
    #         scores = cross_validate(pipe, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
    #         self.results(scores, metrics)

    #     elif cv_type == 'K-Fold':
    #         print(cv_type)
    #         cv = KFold(number=number)
    #         scores = cross_validate(pipe, X_data, Y_data, cv=cv, scoring=metrics, return_train_score=True)
    #         self.results(scores, metrics)



# Decision_Tree_Classifier
class TabRandomForestReg(ParentMLWidget):
    def __init__(self, name):
        super(TabRandomForestReg, self).__init__(name)

    def create_layout(self):

        self.lay2 = QVBoxLayout()
        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        self.slider = ImprovedSlider(0, 100, 'min_samples_split')

        self.l_sp = LabelAndSpinbox('Number of estimators')
        self.l_sp_max_depth = LabelAndSpinbox('max depth')

        self.lay2.addWidget(self.label_name)
        self.lay2.addWidget(self.slider)
        self.lay2.addWidget(self.l_sp)
        self.lay2.addWidget(self.l_sp_max_depth)


    def get_parameters(self, as_list=False, return_labels=False, as_dict=True):
        print('get parameters from ')
        # print(self.get_parameters.__name__)
        num_of_estimators =self.l_sp.get_value()
        max_depth = self.l_sp_max_depth.get_value()
        min_samples_split_arg = int(self.slider.get_current_value())

        if as_list and return_labels:
            return [num_of_estimators, max_depth, min_samples_split_arg], [self.l_sp.name,self.l_sp_max_depth.name, self.slider.name]

        elif not as_list and not as_dict:
            return num_of_estimators,max_depth, min_samples_split_arg
        
        elif as_dict:
            parameters_dict = {"max_depth": max_depth, "min_samples_split": min_samples_split_arg, "n_estimators": num_of_estimators}
            return parameters_dict

    def get_reg(self):
        parameters_dict = self.get_parameters(as_dict=True)

        reg = RandomForestRegressor(**parameters_dict)

        return reg

    # def predict(self, table, Y_index, cv_type, number, metrics, pipe):

    #     print(self.name + ' predict')
    #     print(Y_index)
    #     dataframe = table

    #     X_data = dataframe.drop(Y_index, 1)
    #     Y_data = dataframe[Y_index]


    #     reg = self.get_reg()


    #     print('pipe ', pipe)
    #     pipe.steps.append(("class", reg))
    #     print('create with pipe ', pipe)

    #     print(cv_type)
    #     if cv_type == 'Cross Validation':
    #         print(cv_type, number, metrics)
    #         print(type(metrics))
    #         scores = cross_validate(pipe, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
    #         print(scores)
    #         self.results(scores, metrics)

    #     elif cv_type == 'K-Fold':
    #         print(cv_type)
    #         cv = KFold(number=number)
    #         scores = cross_validate(pipe, X_data, Y_data, cv=cv, scoring=metrics, return_train_score=True)
    #         self.results(scores, metrics)






