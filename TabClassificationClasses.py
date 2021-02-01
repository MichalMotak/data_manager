
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UpgradedWidgets import *
from globals_ import *
import CustomDialogWidgets


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
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
        self.setLayout(self.main_layout)

    def create_layout(self):
        self.lay2 = QVBoxLayout(self)

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

    # def predict_cross_validation(self, clf):


    # def predict_Kfold(self):






class RandomForestClassWidget(ParentMLWidget):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def create_layout(self):
        self.lay2 = QVBoxLayout(self)


        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        # self.label_estimators = QLabel('Number of estimators')
        # self.label_estimators.setAlignment(Qt.AlignCenter)
        # self.label_estimators.setStyleSheet(" QLabel")
        # self.lineedit = QLineEdit(self)
        #

        self.lay2.addWidget(self.label_name)

        # self.lay2.addWidget(self.label_estimators)
        # self.lay2.addWidget(self.lineedit)

        # self.w = Label_and_Lineedit()
        # self.lay2.addWidget(self.w)

        self.l_sp = LabelAndSpinbox('Number of estimators')
        self.lay2.addWidget(self.l_sp)

    def predict(self, table, Y_index, cv_type, number, metrics, multiclass_type, pipe):

        print(self.name + ' predict')
        print('pipe ' , pipe)
        print(Y_index)
        dataframe = table

        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]

        Y_data_unique = np.unique(Y_data)
        print(Y_data_unique)
        # train_test_split_value = int(self.slider.get_current_value())/100.0
        # X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)

        n_estim = self.get_parameters(as_list=False)

        if len(Y_data_unique) > 1:
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

        print('pipe ', pipe)
        pipe.steps.append(("class", clf))
        print('create with pipe ', pipe)



        if cv_type == 'Cross Validation':
            print(cv_type, number, metrics)
            scores = cross_validate(pipe, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)

        elif cv_type == 'K-Fold':
            print(cv_type)
            cv = KFold(number=number)
            scores = cross_validate(pipe, X_data, Y_data, cv=cv, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)
            
        # elif cv_type == 'train_test_split':
        #     X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)
        #     # jednokrotna predykcja
        #     clf = clf.fit(X_train, y_train)

        #     y_pred = clf.predict(X_test)
        #     y_train_pred = clf.predict(X_train)

        #     labels = [0,1]
        #     print('Test acc: ', accuracy_score(y_test, y_pred))

        #     # print(classification_report(y_test, y_pred, labels=labels))

        #     print('Train acc: ', accuracy_score(y_train, y_train_pred))
        #     # print(classification_report(y_train, y_train_pred, labels=labels))


        #     # cv = cross_val_score(clf_org, X_data, Y_data, cv=10, scoring='accuracy')
        #     # cv1 = cross_val_score(clf_org, X_test, y_test, cv=2, scoring='accuracy')

        #     print(cv)
        #     print(cv.mean())
        #     # print(cv1)


            # print('Accuracy (std): %0.3f' % scores_acc.std())


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
        self.lay2 = QVBoxLayout(self)

        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        self.l_sp = LabelAndSpinbox('max depth')
        self.slider_min_samples_split = ImprovedSlider(0, 50, 'min_samples_split')


        self.lay2.addWidget(self.label_name)
        self.lay2.addWidget(self.l_sp)
        self.lay2.addWidget(self.slider_min_samples_split)

    def predict(self, table, Y_index, cv_type, number, metrics, multiclass_type, pipe):


        print(self.name + ' predict')

        dataframe = table
        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]
        Y_data_unique = np.unique(Y_data)
        print(Y_data_unique)

        max_depth_arg, min_samples_split_arg = self.get_parameters(as_list=False)


        # max_depth_arg = self.l_sp.get_value()
        # min_samples_split_arg = int(self.slider_min_samples_split.get_current_value())

        # print(f"train test split {train_test_split_value}, \n"
        #       f"min samples split {min_samples_split_arg}, \n "
        #       f"max depth arg {max_depth_arg}")


        if len(Y_data_unique) > 1:
            print(multiclass_type)
            if multiclass_type == 'OneVsRest':
                clf = OneVsRestClassifier(DecisionTreeClassifier(max_depth=max_depth_arg, min_samples_split= min_samples_split_arg))
            elif multiclass_type == 'OneVsOne':
                clf = OneVsOneClassifier(DecisionTreeClassifier(max_depth=max_depth_arg, min_samples_split= min_samples_split_arg))
                
        elif len(Y_data_unique) == 0:
            clf = DecisionTreeClassifier(max_depth=max_depth_arg, min_samples_split= min_samples_split_arg)


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

        else:
            clf = clf.fit(X_train, y_train)
            y_train_pred = clf.predict(X_train)

            print("Accuracy (train): %0.3f" % accuracy_score(y_train, y_train_pred))

            y_pred = clf.predict(X_test)
            print("Accuracy (test): %0.3f" % accuracy_score(y_test, y_pred))

            labels = np.unique(Y_data)
            print('\n Classification report: \n', classification_report(y_test, y_pred, labels=labels))

    def get_parameters(self, as_list=False, return_labels=False):
        print('get parameters from ')
        # print(self.get_parameters.__name__)
        max_depth_arg = self.l_sp.get_value()
        min_samples_split_arg = int(self.slider_min_samples_split.get_current_value())

        if as_list and return_labels:
            return [max_depth_arg, min_samples_split_arg], [self.l_sp.name, self.slider_min_samples_split.name]

        elif not as_list:
            return max_depth_arg, min_samples_split_arg


class SupportVectorMachineClassWidget(ParentMLWidget):
    def __init__(self, name):
        super().__init__(name)
        self.name = name



    def create_layout(self):
        self.lay2 = QGridLayout(self)

        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)

        self.l_combobox_kernel = LabelAndCombobox('kernel', stretches=[2,2], lay_dir = 'Horizontal', minimal_size=[20,20])
        self.l_combobox_kernel.add_items(['linear', 'poly', 'rbf', 'sigmoid'])

        self.l_sp_C = LabelAndSpinbox('C', stretches=[2,2], lay_dir = 'Horizontal', minimal_size=[20,20], double_spinbox=True)
        self.l_sp_C.set_value(1.0)
        self.l_sp_C.set_step(0.1) 


        self.l_le_tol = LabelAndLineedit('tol', stretches=[2,4], lay_dir = 'Horizontal', minimal_size=[20,20])
        # self.l_le_tol.set_lineedit_text('1e-4')
        self.l_le_tol.set_lineedit_text('0.0001')

        self.label_linear = QLabel('Linear')
        self.label_linear.setAlignment(Qt.AlignCenter)
        self.label_linear.setMinimumHeight(20)
        self.label_linear.setMinimumWidth(20)


        self.l_combobox_linear_penalty = LabelAndCombobox('penalty', stretches=[3,3], lay_dir = 'Horizontal', minimal_size=[20,60])
        self.l_combobox_linear_penalty.add_items(['l1', 'l2'])
        self.l_combobox_linear_penalty.set_current_index(1)

        self.l_combobox_linear_loss = LabelAndCombobox('loss', stretches=[3,3], lay_dir = 'Horizontal', minimal_size=[20,40])
        self.l_combobox_linear_loss.add_items(['hinge', 'squared_hinge'])
        self.l_combobox_linear_loss.set_current_index(1)


        self.l_rb_linear_dual = LabelAndRadioButton('dual', stretches=[3,3], lay_dir = 'Horizontal', minimal_size=[20,40])
        self.l_rb_linear_dual.set_state(True)

        # self.l_sp = LabelAndSpinbox('max depth')
        # self.slider = ImprovedSlider(0, 100, 'Train_test_split')
        # self.slider_min_samples_split = ImprovedSlider(0, 50, 'min_samples_split')

        self.label_poly = QLabel('poly')
        self.label_poly.setAlignment(Qt.AlignCenter)
        self.label_poly.setMinimumHeight(20)
        self.label_poly.setMinimumWidth(30)


        self.l_sp_poly_degree = LabelAndSpinbox('degree', stretches=[3,3], lay_dir = 'Horizontal', minimal_size=[20,30])
        self.l_sp_poly_degree.set_value(3)
        self.l_sp_poly_degree.set_step(1) 

        self.l_combobox_poly_gamma = LabelAndCombobox('gamma', stretches=[2,5], lay_dir = 'Horizontal', minimal_size=[20,40])
        self.l_combobox_poly_gamma.add_items(['scale', 'auto'])
        self.l_combobox_poly_gamma.set_current_index(0)


        # self.label_rbf = QLabel('rbf - C, gamma, tol')
        # self.label_rbf.setAlignment(Qt.AlignCenter)
        # self.label_rbf.setMinimumHeight(20)
        # self.label_rbf.setMinimumWidth(30)



        # self.label_sigmoid = QLabel('sigmoid - C, gamma, tol')
        # self.label_sigmoid.setAlignment(Qt.AlignCenter)
        # self.label_sigmoid.setMinimumHeight(20)
        # self.label_sigmoid.setMinimumWidth(30)



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


        # self.lay2.addWidget(self.label_rbf, 8, 0, 1, 2)


        # self.lay2.addWidget(self.label_sigmoid, 9, 0, 1, 2)

        self.l_combobox_kernel.signal_current_text_changed(self.manage_disability_of_widgets)


    def manage_disability_of_widgets(self):
        # this function is triggered by text changed signal

        # index = self.lay2.count()
        # print(index)
        # myWidget_list = []
        # while(index >= 0):
        #     myWidget_list.append(self.lay2.itemAt(index))
        #     index -=1
        # print(myWidget_list)
        self.l_combobox_linear_penalty.setEnabled(True)
        self.l_sp_poly_degree.setEnabled(True)
        self.l_combobox_linear_loss.setEnabled(True)
        self.l_rb_linear_dual.setEnabled(True)
        self.l_combobox_linear_penalty.setEnabled(True)
        self.l_combobox_poly_gamma.setEnabled(True)

        kernel = self.l_combobox_kernel.get_text()

        if kernel == 'rbf' or kernel =='sigmoid':
            self.l_combobox_linear_penalty.setEnabled(False)
            self.l_sp_poly_degree.setEnabled(False)
            self.l_combobox_linear_loss.setEnabled(False)
            self.l_rb_linear_dual.setEnabled(False)

        elif kernel == 'poly':
            self.l_combobox_linear_penalty.setEnabled(False)
            self.l_combobox_linear_loss.setEnabled(False)
            self.l_rb_linear_dual.setEnabled(False)

        elif kernel == 'linear':
            self.l_sp_poly_degree.setEnabled(False)
            self.l_combobox_poly_gamma.setEnabled(False)


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


    def predict(self, table, Y_index, cv_type, number, metrics,multiclass_type, pipe):


        print(self.name + ' predict')

        kernel = self.l_combobox_kernel.get_text()

        dataframe = table
        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]
        Y_data_unique = np.unique(Y_data)
        # train_test_split_value = int(self.slider.get_current_value())/100.0
        # print(train_test_split_value)
        print('1')
        pars = self.get_parameters(as_dict=True)
        print('xd')
        # X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)

        # max_depth_arg = self.l_sp.get_value()
        # min_samples_split_arg = int(self.slider_min_samples_split.get_current_value())

        # print(f"train test split {train_test_split_value}, \n"
        #       f"min samples split {min_samples_split_arg}, \n "
        #       f"max depth arg {max_depth_arg}")
        print(pars)

        if kernel == 'linear':
            clf = LinearSVC(**pars)
        else:
            clf = SVC(**pars)
        print(clf)

        if len(Y_data_unique) > 1:
            print(multiclass_type)

            if multiclass_type == 'OneVsRest':
                clf = OneVsRestClassifier(clf)
            elif multiclass_type == 'OneVsOne':
                clf = OneVsOneClassifier(clf)
                
        elif len(Y_data_unique) == 0:
            pass


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

        # else:
        #     clf = clf.fit(X_train, y_train)
        #     y_train_pred = clf.predict(X_train)

        #     print("Accuracy (train): %0.3f" % accuracy_score(y_train, y_train_pred))

        #     y_pred = clf.predict(X_test)
        #     print("Accuracy (test): %0.3f" % accuracy_score(y_test, y_pred))

        #     labels = np.unique(Y_data)
        #     print('\n Classification report: \n', classification_report(y_test, y_pred, labels=labels))


