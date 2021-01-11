
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Upgraded_widgets import *
from metrics import *


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import auc, accuracy_score, roc_auc_score, roc_curve, precision_score, recall_score, f1_score, confusion_matrix, classification_report, plot_confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, cross_validate




# Parent
class Parent_ML_Widget(QWidget):
    def __init__(self, name):
        super(Parent_ML_Widget, self).__init__()

        self.name = name
        self.main_layout = QVBoxLayout(self)
        self.height, self.width, = 300, 300
        self.frame = QFrame()
        self.frame.setStyleSheet("QFrame {background-color: rgb(255, 255, 255);"
                                 "border-width: 1;"
                                 "border-radius: 3;"
                                 "border-style: solid;"
                                 "border-color: rgb(50,50,50)}"
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


class Decision_Tree_Clas_Widget(Parent_ML_Widget):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def create_layout(self):
        self.lay2 = QVBoxLayout(self)

        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        self.l_sp = Label_and_spinbox('max depth')
        self.slider = Improved_Slider(0, 100, 'Train_test_split')
        self.slider_min_samples_split = Improved_Slider(0, 50, 'min_samples_split')


        self.lay2.addWidget(self.label_name)
        self.lay2.addWidget(self.slider)
        self.lay2.addWidget(self.l_sp)
        self.lay2.addWidget(self.slider_min_samples_split)

    def predict(self, table, Y_index, cv_type, number, metrics):


        print(self.name + ' predict')

        dataframe = table
        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]
        train_test_split_value = int(self.slider.get_current_value())/100.0
        print(train_test_split_value)

        max_depth_arg, min_samples_split_arg = self.get_parameters(as_list=False)

        X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)

        # max_depth_arg = self.l_sp.get_value()
        # min_samples_split_arg = int(self.slider_min_samples_split.get_current_value())

        # print(f"train test split {train_test_split_value}, \n"
        #       f"min samples split {min_samples_split_arg}, \n "
        #       f"max depth arg {max_depth_arg}")


        clf = DecisionTreeClassifier(max_depth=max_depth_arg, min_samples_split= min_samples_split_arg)

        if cv_type == 'Cross Validation':
            scores = cross_validate(clf, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
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



class Random_Forest_Clas_Widget(Parent_ML_Widget):
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

        self.slider = Improved_Slider(0, 100, 'Train_test_split')

        self.lay2.addWidget(self.label_name)

        self.lay2.addWidget(self.slider)
        # self.lay2.addWidget(self.label_estimators)
        # self.lay2.addWidget(self.lineedit)

        # self.w = Label_and_Lineedit()
        # self.lay2.addWidget(self.w)

        self.l_sp = Label_and_spinbox('Number of estimators')
        self.lay2.addWidget(self.l_sp)

    def predict(self, table, Y_index, cv_type, number, metrics):

        print(self.name + ' predict')

        print(Y_index)
        dataframe = table

        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]

        train_test_split_value = int(self.slider.get_current_value())/100.0
        X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)

        n_estim = self.get_parameters(as_list=False)

        clf_org = RandomForestClassifier(n_estimators=n_estim,
                                     bootstrap=True,
                                     max_features='sqrt')

        if cv_type == 'Cross Validation':
            print(cv_type, number, metrics)
            # print(type(metrics))
            scores = cross_validate(clf_org, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
            # print(scores)

            self.results(scores, metrics)
            # scores_test = scores['test_score']
            # scores_train = scores['train_score']
            #
            # print('Accuracy test (mean): %0.3f' % scores_test.mean())
            # print('Accuracy train (mean): %0.3f' % scores_train.mean())

        else:

            # jednokrotna predykcja
            clf = clf_org.fit(X_train, y_train)

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


    def get_parameters(self, as_list = False, return_labels=False):
        print('get parameters from ')
        n_estim = self.l_sp.get_value()

        if as_list and return_labels:
            return [n_estim], [self.l_sp.name]
        elif not as_list:
            return n_estim
#
# # Decision_Tree_Classifier
# class Tab_Decision_Tree_Clas(QWidget):
#     def __init__(self):
#         super(Tab_Decision_Tree_Clas, self).__init__()
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
#         self.l_sp = Label_and_spinbox('max depth')
#         self.slider = Improved_Slider(0, 100, 'Train_test_split')
#         self.slider_min_samples_split = Improved_Slider(0, 50, 'min_samples_split')
#
#
#         self.lay2.addWidget(self.label_name)
#         self.lay2.addWidget(self.slider)
#         self.lay2.addWidget(self.l_sp)
#         self.lay2.addWidget(self.slider_min_samples_split)
#
#
#         self.frame.setLayout(self.lay2)
#         self.main_layout.setContentsMargins(0, 0, 0, 0)
#         self.setLayout(self.main_layout)
#
#     def predict(self, table, Y_index, cv_type, number, metrics):
#
#
#         print(self.name + ' predict')
#         print(Y_index)
#         print(table)
#         print(cv_type)
#         dataframe = table
#         print(dataframe)
#         X_data = dataframe.drop(Y_index, 1)
#         Y_data = dataframe[Y_index]
#         print('dd')
#         train_test_split_value = int(self.slider.get_current_value())/100.0
#         print(train_test_split_value)
#         X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)
#         print(':)')
#
#         max_depth_arg = self.l_sp.get_value()
#
#         min_samples_split_arg = int(self.slider_min_samples_split.get_current_value())
#
#         print(f"train test split {train_test_split_value}, \n"
#               f"min samples split {min_samples_split_arg}, \n "
#               f"max depth arg {max_depth_arg}")
#
#
#         clf = DecisionTreeClassifier(max_depth=max_depth_arg, min_samples_split= min_samples_split_arg)
#
#         if cv_type == 'Cross Validation':
#             scores = cross_validate(clf, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
#             self.results(scores, metrics)
#         else:
#             clf = clf.fit(X_train, y_train)
#             y_train_pred = clf.predict(X_train)
#
#             print("Accuracy (train): %0.3f" % accuracy_score(y_train, y_train_pred))
#
#             y_pred = clf.predict(X_test)
#             print("Accuracy (test): %0.3f" % accuracy_score(y_test, y_pred))
#
#             labels = np.unique(Y_data)
#             print('\n Classification report: \n', classification_report(y_test, y_pred, labels=labels))
#
#     def get_parameters(self):
#         print('get parameters from ')
#         # print(self.get_parameters.__name__)
#         n_estim = self.l_sp.get_value()
#         return n_estim
#
#     def results(self, scores, metrics):
#         print('results')
#         print('metrics: ', metrics)
#         print(scores)
#
#         print('wyniki')
#         for type in ['train', 'test']:
#             for metric in metrics:
#                 type_metric_name = f"{type}_{metric}"
#                 metric_value = scores[type_metric_name]
#                 metric_value_mean = np.round(metric_value.mean()*100, 3)
#                 metric_value_std = np.round(metric_value.std()*100, 3)
#                 print(f"{type_metric_name} -> mean: {metric_value_mean}, std: {metric_value_std}")
#
#
# # Random Forest
# class Tab_Random_Forest_Clas(QWidget):
#     def __init__(self):
#         super(Tab_Random_Forest_Clas, self).__init__()
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
#             # print(type(metrics))
#             scores = cross_validate(clf_org, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
#             # print(scores)
#
#             self.results(scores, metrics)
#             # scores_test = scores['test_score']
#             # scores_train = scores['train_score']
#             #
#             # print('Accuracy test (mean): %0.3f' % scores_test.mean())
#             # print('Accuracy train (mean): %0.3f' % scores_train.mean())
#
#         else:
#
#             # jednokrotna predykcja
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
#
#     def get_parameters(self):
#         print('get parameters from ')
#         # print(self.get_parameters.__name__)
#         n_estim = self.l_sp.get_value()
#         return n_estim
#
#     def results(self, scores, metrics):
#         print('results')
#         print('metrics: ', metrics)
#         print(scores)
#
#         print('wyniki')
#         for type in ['train', 'test']:
#             for metric in metrics:
#                 type_metric_name = f"{type}_{metric}"
#                 metric_value = scores[type_metric_name]
#                 metric_value_mean = np.round(metric_value.mean()*100, 3)
#                 metric_value_std = np.round(metric_value.std()*100, 3)
#                 print(f"{type_metric_name} -> mean: {metric_value_mean}, std: {metric_value_std}")