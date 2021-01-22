from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UpgradedWidgets import *
from globals_ import *


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from sklearn.metrics import auc, accuracy_score, roc_auc_score, roc_curve, precision_score, recall_score, f1_score, confusion_matrix, classification_report, plot_confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, cross_validate, KFold
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

from TabClassificationClasses import ParentMLWidget


# Tab_Linear_Reg
class TabLinearReg(ParentMLWidget):
    def __init__(self, name):
        super(TabLinearReg, self).__init__(name)

    def create_layout(self):
        self.lay2 = QVBoxLayout(self)
        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        self.l_combobox_linear_model = LabelAndCombobox('Linear Model')
        self.l_combobox_linear_model.add_items(linear_reg_models)


        # self.l_sp_alpha = Label_and_spinbox('Alpha', lay_dir='Vertical')
        # self.l_sp_alpha.set_range(0,1.0)
        # self.l_sp_alpha.set_step(0.01)
        # lay_dir
        self.slider_alpha = ImprovedSlider(0,100, 'Alpha (Ridge, Lasso, ElasticNet)')
        self.slider_alpha.set_float()

        self.slider_l1_ratio = ImprovedSlider(0, 100, 'l1_ratio (ElasticNet)')
        self.slider_l1_ratio.set_float()

        self.lay2.addWidget(self.label_name)
        self.lay2.addWidget(self.l_combobox_linear_model)
        self.lay2.addWidget(self.slider_alpha)
        self.lay2.addWidget(self.slider_l1_ratio)

        # self.lay2.addWidget(self.l_sp_alpha)

    def get_parameters(self, as_list=False, return_labels=False):
        print('get parameters from ')

        alpha = self.slider_alpha.get_current_value()
        print(alpha)
        l1_ratio = self.slider_l1_ratio.get_current_value()
        print(l1_ratio)
        print(alpha,  l1_ratio)
        if as_list and return_labels:
            return [alpha,  l1_ratio], [self.slider_alpha.name, self.slider_l1_ratio.name]
        elif not as_list:
            return alpha,  l1_ratio

    def get_model(self, type):
        # type = self.l_combobox_linear_model.getText()
        print('get model')
        print(type)
        alpha_value, l1_ratio_value = self.get_parameters(as_list=False)
        print('a l;', alpha_value, l1_ratio_value)

        if type == 'LinearRegression':
            reg = LinearRegression()
        elif type == 'Ridge':
            print(type)
            reg = Ridge(alpha= alpha_value)
        elif type == 'Lasso':
            print(type)
            reg = Lasso(alpha= alpha_value)
        elif type == 'ElasticNet':
            print(type)
            reg = ElasticNet(alpha= alpha_value, l1_ratio = l1_ratio_value)
        print(reg)
        return reg

    def predict(self, table, Y_index, cv_type, number, metrics):

        print(self.name + ' zzzz predict')

        print(Y_index)
        dataframe = table

        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]

        # # train_test_split_value = int(self.slider.get_current_value())/100.0
        # X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)

        print('zz')
        print(Y_index)

        type = self.l_combobox_linear_model.getText()
        reg_org = self.get_model(type)
        print(reg_org)

        if cv_type == 'Cross Validation':
            print(cv_type, number, metrics)
            scores = cross_validate(reg_org, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)

        elif cv_type == 'K-Fold':
            print(cv_type, number, metrics)
            cv = KFold(number=number)
            scores = cross_validate(reg_org, X_data, Y_data, cv=cv, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)

        else:
            clf = reg_org.fit(X_train, y_train)

            y_pred = clf.predict(X_test)
            y_train_pred = clf.predict(X_train)

            labels = [0,1]
            print('Test acc: ', accuracy_score(y_test, y_pred))

            # print(classification_report(y_test, y_pred, labels=labels))

            print('Train acc: ', accuracy_score(y_train, y_train_pred))
            # print(classification_report(y_train, y_train_pred, labels=labels))


            # cv = cross_val_score(clf_org, X_data, Y_data, cv=10, scoring='accuracy')
            # cv1 = cross_val_score(clf_org, X_test, y_test, cv=2, scoring='accuracy')

            print(cv)
            print(cv.mean())
            # print(cv1)

# Decision_Tree_Classifier
class TabDecisionTreeReg(ParentMLWidget):
    def __init__(self, name):
        super(TabDecisionTreeReg, self).__init__(name)

    def create_layout(self):
        self.lay2 = QVBoxLayout(self)
        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        # self.pushButton2 = QPushButton(self)
        # self.pushButton2.setText('tab1')

        self.l_combobox_criterion = LabelAndCombobox('criterion')
        self.l_combobox_criterion.add_items(decision_tree_reg_criterion_list)


        self.slider = ImprovedSlider(0, 100, 'Train_test_split')
        self.slider_min_samples_split = ImprovedSlider(0, 50, 'min_samples_split')

        self.l_sp_max_depth = LabelAndSpinbox('max depth')

        self.lay2.addWidget(self.label_name)
        self.lay2.addWidget(self.slider)
        self.lay2.addWidget(self.l_sp_max_depth)
        self.lay2.addWidget(self.l_combobox_criterion)
        self.lay2.addWidget(self.slider_min_samples_split)

    def get_parameters(self, as_list=False, return_labels=False):
        print('get parameters from ')
        # print(self.get_parameters.__name__)
        max_depth_arg = int(self.l_sp_max_depth.get_value())
        min_samples_split_arg = int(self.slider_min_samples_split.get_current_value())
        criterion = self.l_combobox_criterion.get_text()
        print(max_depth_arg,  min_samples_split_arg, criterion)
        if as_list and return_labels:
            return [max_depth_arg, min_samples_split_arg, criterion], [self.l_sp_max_depth.name, self.slider_min_samples_split.name, self.l_combobox_criterion.name]

        elif not as_list:
            return max_depth_arg, min_samples_split_arg, criterion

    def predict(self, table, Y_index, cv_type, number, metrics):

        print(self.name + ' predict')

        print(Y_index)
        dataframe = table

        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]

        train_test_split_value = int(self.slider.get_current_value())/100.0
        X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)

        max_depth_arg, min_samples_split_arg, criterion = self.get_parameters(as_list=False)

        print(Y_index, train_test_split_value, min_samples_split_arg, criterion)
        reg_org = DecisionTreeRegressor(criterion = criterion, max_depth=max_depth_arg, min_samples_split= min_samples_split_arg)

        if cv_type == 'Cross Validation':
            print(cv_type, criterion, number, metrics)
            print(type(metrics))
            scores = cross_validate(reg_org, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)

        elif cv_type == 'K-Fold':
            print(cv_type)
            cv = KFold(number=number)
            scores = cross_validate(reg_org, X_data, Y_data, cv=cv, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)

        else:
            clf = reg_org.fit(X_train, y_train)

            y_pred = clf.predict(X_test)
            y_train_pred = clf.predict(X_train)

            labels = [0,1]
            print('Test acc: ', accuracy_score(y_test, y_pred))

            # print(classification_report(y_test, y_pred, labels=labels))

            print('Train acc: ', accuracy_score(y_train, y_train_pred))
            # print(classification_report(y_train, y_train_pred, labels=labels))


            # cv = cross_val_score(clf_org, X_data, Y_data, cv=10, scoring='accuracy')
            # cv1 = cross_val_score(clf_org, X_test, y_test, cv=2, scoring='accuracy')

            print(cv)
            print(cv.mean())
            # print(cv1)


# Decision_Tree_Classifier
class TabRandomForestReg(ParentMLWidget):
    def __init__(self, name):
        super(TabRandomForestReg, self).__init__(name)

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

        self.slider = ImprovedSlider(0, 100, 'Train_test_split')

        self.lay2.addWidget(self.label_name)
        self.lay2.addWidget(self.slider)
        # self.lay2.addWidget(self.label_estimators)
        # self.lay2.addWidget(self.lineedit)

        # self.w = Label_and_Lineedit()
        # self.lay2.addWidget(self.w)

        self.l_sp = LabelAndSpinbox('Number of estimators')
        self.l_sp_max_depth = LabelAndSpinbox('max depth')

        self.lay2.addWidget(self.l_sp)
        self.lay2.addWidget(self.l_sp_max_depth)


    def get_parameters(self, as_list=False, return_labels=False):
        print('get parameters from ')
        # print(self.get_parameters.__name__)
        num_of_estimators =self.l_sp.get_value()
        max_depth = self.l_sp_max_depth.get_value()
        min_samples_split_arg = int(self.slider.get_current_value())

        print(num_of_estimators, max_depth, min_samples_split_arg)
        if as_list and return_labels:
            return [num_of_estimators, max_depth, min_samples_split_arg], [self.l_sp.name,self.l_sp_max_depth.name, self.slider.name]

        elif not as_list:
            return num_of_estimators,max_depth, min_samples_split_arg

    def predict(self, table, Y_index, cv_type, number, metrics):

        print(self.name + ' predict')
        print(Y_index)
        dataframe = table

        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]

        train_test_split_value = int(self.slider.get_current_value())/100.0
        X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)

        n_estim, max_depth, min_samples_split_arg = self.get_parameters(as_list=False)
        print('zzz')
        print('xd ', n_estim, max_depth, min_samples_split_arg)

        reg_org = RandomForestRegressor(n_estimators=n_estim,
                                         min_samples_split = min_samples_split_arg,
                                         max_depth = max_depth,
                                         bootstrap=True,
                                         max_features='sqrt')

        print(cv_type)
        if cv_type == 'Cross Validation':
            print(cv_type, number, metrics)
            print(type(metrics))
            scores = cross_validate(reg_org, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
            print(scores)
            self.results(scores, metrics)

        elif cv_type == 'K-Fold':
            print(cv_type)
            cv = KFold(number=number)
            scores = cross_validate(reg_org, X_data, Y_data, cv=cv, scoring=metrics, return_train_score=True)
            self.results(scores, metrics)

        else:
            clf = reg_org.fit(X_train, y_train)

            y_pred = clf.predict(X_test)
            y_train_pred = clf.predict(X_train)

            labels = [0,1]
            print('Test acc: ', accuracy_score(y_test, y_pred))

            # print(classification_report(y_test, y_pred, labels=labels))

            print('Train acc: ', accuracy_score(y_train, y_train_pred))
            # print(classification_report(y_train, y_train_pred, labels=labels))


            # cv = cross_val_score(clf_org, X_data, Y_data, cv=10, scoring='accuracy')
            # cv1 = cross_val_score(clf_org, X_test, y_test, cv=2, scoring='accuracy')

            print(cv)
            print(cv.mean())
            # print(cv1)


            # print('Accuracy (std): %0.3f' % scores_acc.std())




# # Decision_Tree_Classifier
# class Tab_Decision_Tree_Reg(QWidget):
#     def __init__(self):
#         super(Tab_Decision_Tree_Reg, self).__init__()
#
#         self.name = 'Decision Tree'
#         self.main_layout = QVBoxLayout(self)
#         self.height, self.width, = 300, 300
#         # self.setGeometry(0,0 , self.width, self.height)
#
#         self.frame = QFrame()
#         self.frame.setStyleSheet("QFrame {background-color: rgb(255, 255, 255);"
#                                  "border-width: 1;"
#                                  "border-radius: 3;"
#                                  "border-style: solid;"
#                                  "border-color: rgb(50,50,50)}"
#                                  )
#         self.main_layout.addWidget(self.frame)
#         self.lay2 = QVBoxLayout(self)
#
#         self.label_name = QLabel(self.name)
#         self.label_name.setAlignment(Qt.AlignCenter)
#         self.label_name.setStyleSheet(" QLabel")
#
#         # self.pushButton2 = QPushButton(self)
#         # self.pushButton2.setText('tab1')
#
#         self.l_combobox_criterion = Label_and_combobox('criterion')
#         self.l_combobox_criterion.addItems(decision_tree_reg_criterion_list)
#
#
#         self.slider = Improved_Slider(0, 100, 'Train_test_split')
#         self.slider_min_samples_split = Improved_Slider(0, 50, 'min_samples_split')
#
#         self.l_sp_max_depth = Label_and_spinbox('max depth')
#
#         self.lay2.addWidget(self.label_name)
#         self.lay2.addWidget(self.slider)
#         self.lay2.addWidget(self.l_sp_max_depth)
#         self.lay2.addWidget(self.l_combobox_criterion)
#         self.lay2.addWidget(self.slider_min_samples_split)
#
#
#         self.frame.setLayout(self.lay2)
#
#         self.main_layout.setContentsMargins(0, 0, 0, 0)
#         self.setLayout(self.main_layout)
#
#     def predict(self, table, Y_index, cv_type, number, metrics):
#
#         print(self.name + ' predict')
#
#         print(Y_index)
#         dataframe = table
#
#         X_data = dataframe.drop(Y_index, 1)
#         Y_data = dataframe[Y_index]
#
#         train_test_split_value = int(self.slider.get_current_value())/100.0
#         X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)
#
#         min_samples_split_arg = int(self.slider_min_samples_split.get_current_value())
#         criterion = self.l_combobox_criterion.getText()
#
#         print(Y_index, train_test_split_value, min_samples_split_arg)
#
#         try:
#             max_depth_arg = int(self.l_sp_max_depth.get_value())
#         except ValueError:
#             print('przyjmuje int')
#
#             # print('message box')
#             msg = QMessageBox()
#             msg.setWindowTitle('Warning Message')
#             msg.setText('Przyjmuje tylko int')
#             msg.setIcon(QMessageBox.Warning)
#             x = msg.exec_()
#             return 0
#
#         clf_org = RandomForestRegressor(criterion = criterion, max_depth=max_depth_arg, min_samples_split= min_samples_split_arg)
#
#         if cv_type == 'Cross Validation':
#             print(cv_type, criterion, number, metrics)
#             print(type(metrics))
#             scores = cross_validate(clf_org, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
#             print(scores)
#             scores_test = scores['test_score']
#             scores_train = scores['train_score']
#
#             print('Accuracy test (mean): %0.3f' % scores_test.mean())
#             print('Accuracy train (mean): %0.3f' % scores_train.mean())
#
#         else:
#             clf = clf_org.fit(X_train, y_train)
#
#             y_pred = clf.predict(X_test)
#             y_train_pred = clf.predict(X_train)
#
#             labels = [0,1]
#             print('Test acc: ', accuracy_score(y_test, y_pred))
#
#             # print(classification_report(y_test, y_pred, labels=labels))
#
#             print('Train acc: ', accuracy_score(y_train, y_train_pred))
#             # print(classification_report(y_train, y_train_pred, labels=labels))
#
#
#             # cv = cross_val_score(clf_org, X_data, Y_data, cv=10, scoring='accuracy')
#             # cv1 = cross_val_score(clf_org, X_test, y_test, cv=2, scoring='accuracy')
#
#             print(cv)
#             print(cv.mean())
#             # print(cv1)
# # Random Forest
# class Tab_Random_Forest_Reg(QWidget):
#     def __init__(self):
#         super(Tab_Random_Forest_Reg, self).__init__()
#
#         # self.main_layout = QVBoxLayout(self)
#         self.name = 'Random Forest'
#         self.main_layout = QVBoxLayout(self)
#         self.height, self.width,  = 300,300
#         # self.setGeometry(0,0 , self.width, self.height)
#
#         self.frame = QFrame()
#         self.frame.setStyleSheet("QFrame {background-color: rgb(255, 255, 255);"
#                                 "border-width: 1;"
#                                 "border-radius: 3;"
#                                 "border-style: solid;"
#                                 "border-color: rgb(50,50,50)}"
#                                 )
#         self.main_layout.addWidget(self.frame)
#         self.lay2 = QVBoxLayout(self)
#
#
#         self.label_name = QLabel(self.name)
#         self.label_name.setAlignment(Qt.AlignCenter)
#         self.label_name.setStyleSheet(" QLabel")
#
#         # self.label_estimators = QLabel('Number of estimators')
#         # self.label_estimators.setAlignment(Qt.AlignCenter)
#         # self.label_estimators.setStyleSheet(" QLabel")
#         # self.lineedit = QLineEdit(self)
#         #
#
#         self.slider = Improved_Slider(0, 100, 'Train_test_split')
#
#         self.lay2.addWidget(self.label_name)
#
#         self.lay2.addWidget(self.slider)
#         # self.lay2.addWidget(self.label_estimators)
#         # self.lay2.addWidget(self.lineedit)
#
#         # self.w = Label_and_Lineedit()
#         # self.lay2.addWidget(self.w)
#
#         self.l_sp = Label_and_spinbox('Number of estimators')
#         self.lay2.addWidget(self.l_sp)
#
#         self.frame.setLayout(self.lay2)
#         self.main_layout.setContentsMargins(0, 0, 0, 0)
#         self.setLayout(self.main_layout)
#
#     def predict(self, table, Y_index, cv_type, number, metrics):
#
#         print(self.name + ' predict')
#
#         print(Y_index)
#         dataframe = table
#
#         X_data = dataframe.drop(Y_index, 1)
#         Y_data = dataframe[Y_index]
#
#         train_test_split_value = int(self.slider.get_current_value())/100.0
#         X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)
#
#         n_estim = self.l_sp.get_value()
#
#         clf_org = RandomForestClassifier(n_estimators=n_estim,
#                                      bootstrap=True,
#                                      max_features='sqrt')
#
#         if cv_type == 'Cross Validation':
#             print(cv_type, number, metrics)
#             print(type(metrics))
#             scores = cross_validate(clf_org, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
#             print(scores)
#             scores_test = scores['test_score']
#             scores_train = scores['train_score']
#
#             print('Accuracy test (mean): %0.3f' % scores_test.mean())
#             print('Accuracy train (mean): %0.3f' % scores_train.mean())
#
#         else:
#             clf = clf_org.fit(X_train, y_train)
#
#             y_pred = clf.predict(X_test)
#             y_train_pred = clf.predict(X_train)
#
#             labels = [0,1]
#             print('Test acc: ', accuracy_score(y_test, y_pred))
#
#             # print(classification_report(y_test, y_pred, labels=labels))
#
#             print('Train acc: ', accuracy_score(y_train, y_train_pred))
#             # print(classification_report(y_train, y_train_pred, labels=labels))
#
#
#             # cv = cross_val_score(clf_org, X_data, Y_data, cv=10, scoring='accuracy')
#             # cv1 = cross_val_score(clf_org, X_test, y_test, cv=2, scoring='accuracy')
#
#             print(cv)
#             print(cv.mean())
#             # print(cv1)
#
#
#             # print('Accuracy (std): %0.3f' % scores_acc.std())

