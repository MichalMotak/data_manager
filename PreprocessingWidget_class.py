from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import numpy as np
import pandas as pd


class PreprocessingWidget(QWidget):

    def __init__(self):
        print('PreprocessingWidget init')
        super(PreprocessingWidget, self).__init__()


        # self.main_layout = QVBoxLayout(self)
        self.main_layout = QGridLayout(self)


        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('Preprocessing')

        self.main_layout.addWidget(self.label)




        self.setLayout(self.main_layout)