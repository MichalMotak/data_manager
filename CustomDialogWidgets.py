from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CustomDialog(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        print('custom dialog init')
        self.setWindowTitle('custom dialog')

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        # self.show()
        self.exec_()


class CustomMessageBoxWarning(QMessageBox):
    def __init__(self, text):
        super(CustomMessageBoxWarning, self).__init__()
        print('custom message box init')

        self.text = text

        self.setIcon(QMessageBox.Warning)
        self.setText(self.text)
        self.setWindowTitle('Warning')
        self.setStandardButtons(QMessageBox.Close)

        self.exec_()


class CustomMessageBoxInformation(QMessageBox):
    def __init__(self, text):
        super(CustomMessageBoxInformation, self).__init__()
        print('custom message box init')
        self.text = text

        self.setIcon(QMessageBox.Information)
        self.setText(self.text)
        self.setWindowTitle('Information')
        self.setStandardButtons(QMessageBox.Close)

        self.exec_()