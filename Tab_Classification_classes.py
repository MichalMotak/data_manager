
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



# Decision_Tree_Classifier
class Tab_Decision_Tree_Clas(QWidget):
    def __init__(self):
        super(Tab_Decision_Tree_Clas, self).__init__()

        self.name = 'Decision Tree'
        self.main_layout = QVBoxLayout(self)
        self.height, self.width, = 300, 300
        # self.setGeometry(0,0 , self.width, self.height)

        self.frame = QFrame()
        self.frame.setStyleSheet("QFrame {background-color: rgb(255, 255, 255);"
                                 "border-width: 1;"
                                 "border-radius: 3;"
                                 "border-style: solid;"
                                 "border-color: rgb(50,50,50)}"
                                 )
        self.main_layout.addWidget(self.frame)
        self.lay2 = QVBoxLayout(self)

        self.label_name = QLabel(self.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet(" QLabel")

        # self.pushButton2 = QPushButton(self)
        # self.pushButton2.setText('tab1')

        self.l_sp = Label_and_spinbox('max depth')


        self.slider = Improved_Slider(0, 100, 'Train_test_split')

        self.slider_min_samples_split = Improved_Slider(0, 50, 'min_samples_split')


        self.lay2.addWidget(self.label_name)

        self.lay2.addWidget(self.slider)
        self.lay2.addWidget(self.l_sp)


        self.lay2.addWidget(self.slider_min_samples_split)



        # self.lay2.addWidget(self.label_max_depth)

        self.frame.setLayout(self.lay2)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

    def predict(self, table, Y_index):


        print(self.name + ' predict')
        dataframe = table.dataframe

        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]

        train_test_split_value = int(self.slider.get_current_value())/100.0
        print(train_test_split_value)
        X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)
        print(':)')

        try:
            max_depth_arg = int(self.le_max_depth.text())
        except ValueError:
            print('przyjmuje int')

            # print('message box')
            msg = QMessageBox()
            msg.setWindowTitle('Warning Message')
            msg.setText('Przyjmuje tylko int')
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()
            return 0

        min_samples_split_arg = int(self.slider_min_samples_split.get_current_value())

        print(f"train test split {train_test_split_value}, \n"
              f"min samples split {min_samples_split_arg}, \n "
              f"max depth arg {max_depth_arg}")


        clf = DecisionTreeClassifier(max_depth=max_depth_arg, min_samples_split= min_samples_split_arg)

        clf = clf.fit(X_train, y_train)
        y_train_pred = clf.predict(X_train)

        print("Accuracy (train): %0.3f" % accuracy_score(y_train, y_train_pred))

        y_pred = clf.predict(X_test)
        print("Accuracy (test): %0.3f" % accuracy_score(y_test, y_pred))

        labels = np.unique(Y_data)
        print('\n Classification report: \n', classification_report(y_test, y_pred, labels=labels))


# Random Forest
class Tab_Random_Forest_Clas(QWidget):
    def __init__(self):
        super(Tab_Random_Forest_Clas, self).__init__()

        # self.main_layout = QVBoxLayout(self)
        self.name = 'Random Forest'
        self.main_layout = QVBoxLayout(self)
        self.height, self.width,  = 300,300
        # self.setGeometry(0,0 , self.width, self.height)

        self.frame = QFrame()
        self.frame.setStyleSheet("QFrame {background-color: rgb(255, 255, 255);"
                                "border-width: 1;"
                                "border-radius: 3;"
                                "border-style: solid;"
                                "border-color: rgb(50,50,50)}"
                                )
        self.main_layout.addWidget(self.frame)
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

        self.frame.setLayout(self.lay2)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

    def predict(self, table, Y_index, cv_type, number, metrics):

        print(self.name + ' predict')

        print(Y_index)
        dataframe = table

        X_data = dataframe.drop(Y_index, 1)
        Y_data = dataframe[Y_index]

        train_test_split_value = int(self.slider.get_current_value())/100.0
        X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=train_test_split_value, random_state=1)

        n_estim = self.l_sp.get_value()

        clf_org = RandomForestClassifier(n_estimators=n_estim,
                                     bootstrap=True,
                                     max_features='sqrt')

        if cv_type == 'Cross Validation':
            print(cv_type, number, metrics)
            print(type(metrics))
            scores = cross_validate(clf_org, X_data, Y_data, cv=number, scoring=metrics, return_train_score=True)
            print(scores)
            scores_test = scores['test_score']
            scores_train = scores['train_score']

            print('Accuracy test (mean): %0.3f' % scores_test.mean())
            print('Accuracy train (mean): %0.3f' % scores_train.mean())

        else:
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


