
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from globals_ import class_metrics_list, class_metrics_list_functions, reg_metrics_list, reg_metrics_list_functions


import CustomDialogWidgets
import UpgradedWidgets

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, SVC

from sklearn.metrics import auc, accuracy_score, roc_auc_score, roc_curve, precision_score, recall_score, f1_score, confusion_matrix, classification_report, plot_confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, cross_validate, KFold
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier




# Parent
class ParentMLWidget(QWidget):
    def __init__(self, name):
        super(ParentMLWidget, self).__init__()

        self.name = name
        self.main_layout = QVBoxLayout(self)
        self.height, self.width, = 300, 300
        self.frame = QFrame()

        self.frame.setStyleSheet("QFrame {"
                                "border-width: 1;"
                                "border-radius: 3;"
                                "border-style: solid;"
                                "border-color: rgb(0,0,0)}"
                                )
                                
        self.main_layout.addWidget(self.frame)
        self.create_layout()

        self.frame.setLayout(self.lay2)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.setLayout(self.main_layout)

    def create_layout(self):
        self.lay2 = QVBoxLayout()

    def give_name(self):
        self.name = ''

    def results(self, scores, metrics):
        print('results')
        print('metrics: ', metrics)
        print(scores)
        print('wyniki')
        self.results_dict = {}

        for type in ['train', 'test']:
            for metric in metrics:
                type_metric_name = f"{type}_{metric}"
                metric_value = scores[type_metric_name]
                metric_value_mean = np.round(metric_value.mean()*100, 3)
                metric_value_std = np.round(metric_value.std()*100, 3)
                print(f"{type_metric_name} -> mean: {metric_value_mean}, std: {metric_value_std}")
                self.results_dict[type_metric_name] = metric_value_mean

        print(self.results_dict)

    def get_last_results(self):
        return self.results_dict


    def predict(self, table, Y_index, tab_type, cv_type, number, metrics, pipe):

        print(self.name + ' predict')
        print('pipe ' , pipe)
        print(Y_index)

        dataframe = table

        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]

        # if predict_type == 'clf':
        #     print('pipe ', pipe)
        #     pipe.steps.append(("class", clf))
        #     print('create with pipe ', pipe)


        if cv_type == 'Cross Validation':
            scores = cross_validate(pipe, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)

        elif cv_type == 'K-Fold':
            cv = KFold(number=number)
            scores = cross_validate(pipe, X_data, Y_data, cv=cv, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)

        elif cv_type == 'One_Time_Validation':
            X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=0.25, shuffle=True, random_state=0)
            pipe.fit(X_train, y_train)

            pred_train = pipe.predict(X_train)
            pred_test = pipe.predict(X_test) 

            self.save_one_time_validation_predictions(y_test, pred_test)

            scores = {}

            if tab_type == 'Classification':
                metrics_list = class_metrics_list
                metrics_list_functions = class_metrics_list_functions

            elif tab_type == 'Regression':
                metrics_list = reg_metrics_list
                metrics_list_functions = reg_metrics_list_functions


            for name, fun in zip(metrics_list, metrics_list_functions):
                if name in metrics:
                    train_score = fun(y_train, pred_train)
                    test_score = fun(y_test, pred_test)
                                    
                    print(f"score: {name}, values: {train_score}, {test_score}")
                    scores[f"train_{name}"] = train_score
                    scores[f"test_{name}"] = test_score

            print(scores)
            self.results(scores, metrics)

    def save_one_time_validation_predictions(self, y_test, pred_test):
        self.y_test = y_test
        self.pred_test = pred_test

    def get_one_time_validation_predictions(self):
        return self.y_test, self.pred_test


class EnsembleClassWidget(ParentMLWidget):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def create_layout(self):

        self.lay2 = QGridLayout()

        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        self.lay2.addWidget(self.label_name)

        self.l_combobox_method = UpgradedWidgets.LabelAndCombobox('Ensemble Method')
        self.l_combobox_method.add_items(['AdaBoost', 'Bagging'])


        self.l_sp_learning_rate = UpgradedWidgets.LabelAndSpinbox('learning rate', double_spinbox=True)
        self.l_sp_learning_rate.set_value(1.0)
        self.l_sp_learning_rate.set_step(0.05)

        self.l_sp_n_estimators = UpgradedWidgets.LabelAndSpinbox('n_estimators')
        self.l_sp_n_estimators.set_value(50)
        self.l_sp_n_estimators.set_step(5)
        self.l_sp_n_estimators.set_range(1,300)

        self.l_sp_max_samples = UpgradedWidgets.LabelAndSpinbox('max_samples', double_spinbox=True)
        self.l_sp_max_samples.set_value(1.0)
        self.l_sp_max_samples.set_step(0.05)

        self.l_rb_bootstrap = UpgradedWidgets.LabelAndRadioButton('bootstrap')


        self.lay2.addWidget(self.l_combobox_method, 0,0,1,2)
        self.lay2.addWidget(self.l_sp_learning_rate,1,0,1,2)
        self.lay2.addWidget(self.l_sp_n_estimators, 2,0,1,1)

        self.lay2.addWidget(self.l_sp_max_samples, 2,1,1,1)
        self.lay2.addWidget(self.l_rb_bootstrap, 3,0,1,1)

            
        self.l_combobox_method.signal_current_text_changed(self.manage_disability_of_widgets)



    def manage_disability_of_widgets(self):
        # this function is triggered by text changed signal
        kind = self.l_combobox_method.get_text()

        if kind == 'AdaBoost':
            self.l_sp_learning_rate.setEnabled(True)
            self.l_sp_max_samples.setEnabled(False)
            self.l_rb_bootstrap.setEnabled(False)

        elif kind == 'Bagging':
            self.l_sp_max_samples.setEnabled(True)
            self.l_rb_bootstrap.setEnabled(True)
            self.l_sp_learning_rate.setEnabled(False)


    def update_pipe(self, clf, pipe):
        print('update_pipe ensemble')
        kind = self.l_combobox_method.get_text()

        if kind == 'AdaBoost':
            parameters_dict = self.get_parameters(as_dict=True)

            ensemble_clf = AdaBoostClassifier(clf, **parameters_dict)

        elif kind == 'Bagging':
            parameters_dict = self.get_parameters(as_dict=True)
            print('par bagging ', parameters_dict)

            ensemble_clf = BaggingClassifier(clf, **parameters_dict)

        print('pipe ', pipe)
        pipe.steps.append(("ensemble class", ensemble_clf))

        return pipe


    def get_parameters(self, as_list = False, return_labels=False, as_dict = False):
        print('get parameters from ')

        method = self.l_combobox_method.get_text()

        n_estimators = self.l_sp_n_estimators.get_value()

        if method == 'AdaBoost':
            learning_rate = self.l_sp_learning_rate.get_value()

            if as_list and return_labels:
                return [n_estimators, learning_rate], [self.l_sp_n_estimators.name, self.l_sp_learning_rate.name]

            elif not as_list and not as_dict:
                return n_estimators, learning_rate

            elif as_dict:
                parameters_dict = {"n_estimators" : n_estimators, "learning_rate" : learning_rate }
                return parameters_dict

        elif method == 'Bagging':
            max_samples = self.l_sp_max_samples.get_value()
            bootstrap = self.l_rb_bootstrap.get_state()

            if as_list and return_labels:
                return [n_estimators, max_samples, bootstrap], [self.l_sp_n_estimators.name, self.l_sp_max_samples.name, self.l_rb_bootstrap.name]

            elif not as_list and not as_dict:
                return n_estimators, max_samples, bootstrap
#
            elif as_dict:
                parameters_dict = {"n_estimators" : n_estimators, "max_samples" : max_samples, "bootstrap":bootstrap }
                return parameters_dict


class RandomForestClassWidget(ParentMLWidget):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def create_layout(self):
        self.lay2 = QVBoxLayout()


        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        self.lay2.addWidget(self.label_name)

        self.l_sp = UpgradedWidgets.LabelAndSpinbox('Number of estimators')
        self.lay2.addWidget(self.l_sp)


    def get_clf(self, table, Y_index, multiclass_type, pipe):

        dataframe = table
        Y_data = dataframe[Y_index]

        Y_data_unique = np.unique(Y_data)
        print(Y_data_unique)

        
        n_estim = self.get_parameters(as_list=False)

        if len(Y_data_unique) > 2:
            print(multiclass_type)
            if multiclass_type == 'OneVsRest':
                clf = OneVsRestClassifier(RandomForestClassifier(n_estimators=n_estim,
                                        bootstrap=True,
                                        max_features='sqrt'))

            elif multiclass_type == 'OneVsOne':
                clf = OneVsOneClassifier(RandomForestClassifier(n_estimators=n_estim,
                                        bootstrap=True,
                                        max_features='sqrt'))

        else:
            clf = RandomForestClassifier(n_estimators=n_estim,
                                        bootstrap=True,
                                        max_features='sqrt')

        return clf



    def get_parameters(self, as_list = False, return_labels=False):
        print('get parameters from ')
        n_estim = self.l_sp.get_value()

        if as_list and return_labels:
            return [n_estim], [self.l_sp.name]
        elif not as_list:
            return n_estim
#

class DecisionTreeClassWidget(ParentMLWidget):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def create_layout(self):
        self.lay2 = QVBoxLayout()

        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        self.l_sp = UpgradedWidgets.LabelAndSpinbox('max depth')
        self.slider_min_samples_split = UpgradedWidgets.ImprovedSlider(0, 50, 'min_samples_split')

        self.lay2.addWidget(self.label_name)
        self.lay2.addWidget(self.l_sp)
        self.lay2.addWidget(self.slider_min_samples_split)

    def get_clf(self, table, Y_index, multiclass_type, pipe):

        dataframe = table
        Y_data = dataframe[Y_index]

        Y_data_unique = np.unique(Y_data)
        print(Y_data_unique)

        # max_depth_arg, min_samples_split_arg = self.get_parameters(as_list=False)
        parameters_dict = self.get_parameters(as_dict=True)

        if len(Y_data_unique) > 2:
            print(multiclass_type)
            if multiclass_type == 'OneVsRest':
                clf = OneVsRestClassifier(DecisionTreeClassifier(**parameters_dict))
            
            elif multiclass_type == 'OneVsOne':
                clf = OneVsOneClassifier(DecisionTreeClassifier(**parameters_dict))
                
        elif len(Y_data_unique) == 2:
            # clf = DecisionTreeClassifier(max_depth=max_depth_arg, min_samples_split= min_samples_split_arg)
            clf = DecisionTreeClassifier(**parameters_dict)
        return clf


    def get_parameters(self, as_list=False, return_labels=False, as_dict = False):
        print('get parameters from ')

        max_depth_arg = self.l_sp.get_value()
        min_samples_split_arg = int(self.slider_min_samples_split.get_current_value())

        if as_list and return_labels:
            return [max_depth_arg, min_samples_split_arg], [self.l_sp.name, self.slider_min_samples_split.name]

        elif not as_list and not as_dict:
            return max_depth_arg, min_samples_split_arg

        elif as_dict:
            parameters_dict = {"max_depth":max_depth_arg, "min_samples_split":min_samples_split_arg}
            print('as dict ', parameters_dict)
            return parameters_dict


class SupportVectorMachineClassWidget(ParentMLWidget):
    def __init__(self, name):
        super().__init__(name)
        self.name = name



    def create_layout(self):
        self.lay2 = QGridLayout()

        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)

        self.l_combobox_kernel = UpgradedWidgets.LabelAndCombobox('kernel', stretches=[2,2], lay_dir = 'Horizontal', minimal_size=[20,20])
        self.l_combobox_kernel.add_items(['linear', 'poly', 'rbf', 'sigmoid'])

        self.l_sp_C = UpgradedWidgets.LabelAndSpinbox('C', stretches=[2,2], lay_dir = 'Horizontal', minimal_size=[20,20], double_spinbox=True)
        self.l_sp_C.set_value(1.0)
        self.l_sp_C.set_step(0.1) 

        self.l_le_tol = UpgradedWidgets.LabelAndLineedit('tol', stretches=[2,4], lay_dir = 'Horizontal', minimal_size=[20,20])
        # self.l_le_tol.set_lineedit_text('1e-4')
        self.l_le_tol.set_lineedit_text('0.0001')

        self.label_linear = QLabel('Linear')
        self.label_linear.setAlignment(Qt.AlignCenter)
        self.label_linear.setMinimumHeight(20)
        self.label_linear.setMinimumWidth(20)


        self.l_combobox_linear_penalty = UpgradedWidgets.LabelAndCombobox('penalty', stretches=[3,3], lay_dir = 'Horizontal', minimal_size=[20,60])
        self.l_combobox_linear_penalty.add_items(['l1', 'l2'])
        self.l_combobox_linear_penalty.set_current_index(1)

        self.l_combobox_linear_loss = UpgradedWidgets.LabelAndCombobox('loss', stretches=[3,3], lay_dir = 'Horizontal', minimal_size=[20,40])
        self.l_combobox_linear_loss.add_items(['hinge', 'squared_hinge'])
        self.l_combobox_linear_loss.set_current_index(1)


        self.l_rb_linear_dual = UpgradedWidgets.LabelAndRadioButton('dual', stretches=[3,3], lay_dir = 'Horizontal', minimal_size=[20,40])
        self.l_rb_linear_dual.set_state(True)


        self.label_poly = QLabel('poly')
        self.label_poly.setAlignment(Qt.AlignCenter)
        self.label_poly.setMinimumHeight(20)
        self.label_poly.setMinimumWidth(30)


        self.l_sp_poly_degree = UpgradedWidgets.LabelAndSpinbox('degree', stretches=[3,3], lay_dir = 'Horizontal', minimal_size=[20,30])
        self.l_sp_poly_degree.set_value(3)
        self.l_sp_poly_degree.set_step(1) 

        self.l_combobox_poly_gamma = UpgradedWidgets.LabelAndCombobox('gamma', stretches=[2,5], lay_dir = 'Horizontal', minimal_size=[20,40])
        self.l_combobox_poly_gamma.add_items(['scale', 'auto'])
        self.l_combobox_poly_gamma.set_current_index(0)



        self.lay2.addWidget(self.label_name, 0, 0, 1, 3)

        self.lay2.addWidget(self.l_combobox_kernel, 1, 0, 1, 3)
        self.lay2.addWidget(self.l_le_tol, 2, 0)
        self.lay2.addWidget(self.l_sp_C, 2, 1)


        self.lay2.addWidget(self.label_linear, 3, 0, 1, 3)
        self.lay2.addWidget(self.l_combobox_linear_penalty, 4, 0)
        self.lay2.addWidget(self.l_combobox_linear_loss, 5, 0, 1, 3)
        self.lay2.addWidget(self.l_rb_linear_dual, 4, 1)


        self.lay2.addWidget(self.label_poly, 6, 0, 1, 3)
        self.lay2.addWidget(self.l_combobox_poly_gamma, 7, 0)
        self.lay2.addWidget(self.l_sp_poly_degree, 7, 1)

        self.enable_widgets_linear = [self.l_combobox_linear_penalty, self.l_combobox_linear_loss, self.l_rb_linear_dual]
        self.enable_widgets_poly = [self.l_combobox_poly_gamma, self.l_sp_poly_degree]
        self.enable_widgets_rbf = [self.l_combobox_poly_gamma]
        self.enable_widgets_sigmoid = [self.l_combobox_poly_gamma]

        self.all_widgets_list = list(set(self.enable_widgets_linear + self.enable_widgets_poly+self.enable_widgets_rbf ))
        
        self.l_combobox_kernel.signal_current_text_changed(self.manage_disability_of_widgets)



    def manage_disability_of_widgets(self):
        # this function is triggered by text changed signal

        kernel = self.l_combobox_kernel.get_text()

        if kernel == 'rbf' or kernel =='sigmoid':
            [widget.setEnabled(True) if widget in self.enable_widgets_rbf else widget.setEnabled(False) for widget in self.all_widgets_list]

        elif kernel == 'poly':
            [widget.setEnabled(True) if widget in self.enable_widgets_poly else widget.setEnabled(False) for widget in self.all_widgets_list]


        elif kernel == 'linear':
            [widget.setEnabled(True) if widget in self.enable_widgets_linear else widget.setEnabled(False) for widget in self.all_widgets_list]


    def get_parameters(self, as_list=False, return_labels=False, as_dict = False):

        print('get parameters from ')

        kernel = self.l_combobox_kernel.get_text()
        print(kernel)
        C = self.l_sp_C.get_value()
        gamma = self.l_combobox_poly_gamma.get_text()
        try:
            tol = float(self.l_le_tol.get_text())
        except Exception as e:
            d = CustomDialogWidgets.CustomMessageBoxWarning(str(e))
        print(C, gamma, tol)

        if kernel == 'linear':
            penalty = self.l_combobox_linear_penalty.get_text()
            loss = self.l_combobox_linear_loss.get_text()
            dual = self.l_rb_linear_dual.get_state()

            parameters = [C, tol, penalty, loss, dual ]
            print(parameters)
            print(self.l_sp_C.name)
            print(self.l_le_tol.name)
            print(self.l_combobox_linear_penalty.name)
            print(self.l_combobox_linear_loss.name)
            print(self.l_rb_linear_dual.name)

            parameters_names = [self.l_sp_C.name, self.l_le_tol.name , self.l_combobox_linear_penalty.name,
                                self.l_combobox_linear_loss.name, self.l_rb_linear_dual.name]
            print(parameters_names)
            parameters_dict = {"C":C, "tol":tol, "penalty":penalty,"loss":loss,"dual":dual}
            print(parameters_dict)


        elif kernel == 'poly':
            degree = self.l_sp_poly_degree.get_value()
            print(degree)
            parameters = [C, gamma, tol, degree]
            parameters_names = [self.l_sp_C.name, self.l_combobox_poly_gamma.name, self.l_le_tol.name , self.l_sp_poly_degree.name ]
            parameters_dict = {"C":C, "gamma":gamma, "tol":tol, "degree":degree}

        elif kernel == 'rbf' or kernel == 'sigmoid':

            parameters = [C, gamma, tol ]
            parameters_names = [self.l_sp_C.name, self.l_combobox_poly_gamma.name, self.l_le_tol.name]
            parameters_dict = {"C":C, "gamma":gamma, "tol":tol}


        print(parameters)
        print(parameters_names)
        print(parameters_dict)
        if as_list and return_labels:
            return parameters, parameters_names

        if as_dict:
            return parameters_dict

    def get_clf(self, table, Y_index, multiclass_type, pipe):

        kernel = self.l_combobox_kernel.get_text()

        dataframe = table
        Y_data = dataframe[Y_index]

        Y_data_unique = np.unique(Y_data)
        print(Y_data_unique)

        pars = self.get_parameters(as_dict=True)


        if kernel == 'linear':
            clf = LinearSVC(**pars)
        else:
            clf = SVC(**pars)
        print(clf)

        if len(Y_data_unique) > 2:
            print(multiclass_type)

            if multiclass_type == 'OneVsRest':
                clf = OneVsRestClassifier(clf)
            elif multiclass_type == 'OneVsOne':
                clf = OneVsOneClassifier(clf)
                
        elif len(Y_data_unique) == 2:
            pass

        return clf


    def predict(self, table, Y_index, cv_type, number, metrics, pipe, clf=None, predict_type = None):

        print(self.name + ' predict')

        dataframe = table
        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]
        Y_data_unique = np.unique(Y_data)


        if predict_type == 'clf':
            print('pipe ', pipe)
            pipe.steps.append(("class", clf))
            print('create with pipe ', pipe)


        if cv_type == 'Cross Validation':
            scores = cross_validate(pipe, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)

        elif cv_type == 'K-Fold':
            cv = KFold(number=number)
            scores = cross_validate(pipe, X_data, Y_data, cv=cv, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)

