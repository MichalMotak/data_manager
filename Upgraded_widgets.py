from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



class Improved_Slider(QWidget):
    def __init__(self, lower_range, upper_range, name):
        super(Improved_Slider, self).__init__()

        self.main_layout = QVBoxLayout(self)
        self.lower_range = lower_range
        self.upper_range = upper_range
        self.name = name
        self.to_float = False

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(self.lower_range, self.upper_range)
        self.slider.setTickPosition(QSlider.TicksBelow)
        # self.slider.setTickInterval(10)

        self.label_name = QLabel(name)
        self.label_name.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.label_name)

        self.main_layout.addWidget(self.slider)
        # self.main_layout.setStyleSheet("")
        self.main_layout.setContentsMargins(0, 0, 0, 0)


        self.slider_hbox = QHBoxLayout()
        # self.slider_hbox.setContentsMargins(0, 0, 0, 0)
        # self.slider_hbox.setVerticalSpacing(30)
        # self.slider_hbox.addStretch()

        self.label_minimum = QLabel("Min Value : "+ str(self.lower_range))
        self.label_maximum = QLabel("Max Value : "+ str(self.upper_range))

        self.lineedit_value = QLineEdit("Current Value : ")
        self.lineedit_value.textEdited.connect(self.lineedit_value_edited)


        # self.slider.maximumChanged.connect(label_maximum.setNum)
        # self.slider_vbox.addWidget(self.slider)
        # slider_vbox.addLayout(slider_hbox)
        self.slider_hbox.addWidget(self.label_minimum)
        self.slider_hbox.addWidget(self.lineedit_value)
        self.slider_hbox.addWidget(self.label_maximum)
        self.slider.valueChanged.connect(self.slider_value_changed)


        self.main_layout.addLayout(self.slider_hbox)

        self.setLayout(self.main_layout)
        self.show()

    def slider_value_changed(self):
        print('slider value changed')
        self.current_value = self.slider.value()
        if self.to_float:
            self.current_value /= 100.0
        self.lineedit_value.setText("Current Value : "+ str(self.current_value))

    def lineedit_value_edited(self):
        print('lineedit_value_edited')
        le_value = self.lineedit_value.text()
        print(le_value)

        try:
            new_value = int(le_value.split(':')[1])
            print(new_value)
            if new_value >= self.lower_range and new_value <= self.upper_range:
                self.slider.setValue(new_value)
        except:
            return 0
        self.current_value = new_value

    def get_current_value(self):
        print('current valueeee')
        le_value = self.slider.value()
        print(le_value)
        print(self.current_value)
        return self.current_value

    def set_float(self):
        self.to_float = True
        self.label_minimum.setText("Min Value : "+ str(self.lower_range /100.0))
        self.label_maximum.setText("Min Value : "+ str(self.upper_range /100.0))


class CheckableComboBox(QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res

class Label_and_Lineedit(QWidget):
    def __init__(self, name, lay_dir = 'Horizontal', stretches = [5,5],  minimal_size = None):
        super(Label_and_Lineedit, self).__init__()

        if lay_dir == 'Horizontal':
            self.main_layout = QHBoxLayout()
        elif lay_dir == 'Vertical':
            self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(name)

        self.lineedit = QLineEdit()
        self.lineedit.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.label, stretches[0])
        # self.main_layout.addStretch(1)

        self.main_layout.addWidget(self.lineedit, stretches[1])
        # self.main_layout.addStretch(1)


        if minimal_size is not None:
            self.label.setMinimumHeight(minimal_size[0])
            self.label.setMinimumWidth(minimal_size[1])
            self.lineedit.setMinimumHeight(minimal_size[0])
            self.lineedit.setMinimumWidth(minimal_size[1])

        self.setLayout(self.main_layout)

    def get_text(self):
        return self.lineedit.text()
    
    def set_lineedit_text(self, text):
        self.lineedit.setText(text)

    def update_text(self, text):
        """This function add string after coma

        Returns:
            [type]: [description]
        """
        current_text = self.get_text()
        print(current_text)
        if current_text is '':
            self.set_lineedit_text(text)
            print('pusty')
        else:
            new_text = f"{current_text}, {text}"
            self.set_lineedit_text(new_text)

    

class Label_and_spinbox(QWidget):
    def __init__(self, name, lay_dir = 'Horizontal'):
        super(Label_and_spinbox, self).__init__()

        if lay_dir == 'Horizontal':
            self.main_layout = QHBoxLayout()
        elif lay_dir == 'Vertical':
            self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.name = name

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(self.name)

        self.sp = QSpinBox()
        self.sp.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.sp)



        self.setLayout(self.main_layout)

    def get_value(self):
        return self.sp.value()

    def set_range(self, min, max):
        self.sp.setRange(min, max)

    def set_step(self, step):
        self.sp.setSingleStep(step)

    def set_value(self, value):
        self.sp.value = value

class Label_and_combobox_checkable(QWidget):
    def __init__(self, name):
        super(Label_and_combobox_checkable, self).__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.name = name

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(name)

        self.combobox = CheckableComboBox(self)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.combobox)

        self.setLayout(self.main_layout)

    def add_items(self, items):
        self.combobox.addItems(items)
    #
    def get_text(self):
        return self.combobox.currentText()

class Label_and_combobox(QWidget):
    def __init__(self, name, lay_dir = 'Horizontal', stretches = None,  minimal_size = None):
        super(Label_and_combobox, self).__init__()
        if lay_dir == 'Horizontal':
            self.main_layout = QHBoxLayout()
        elif lay_dir == 'Vertical':
            self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.name = name

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(name)

        self.combobox = QComboBox()
    
        if minimal_size is not None:
            self.label.setMinimumHeight(minimal_size[0])
            self.label.setMinimumWidth(minimal_size[1])
            self.combobox.setMinimumHeight(minimal_size[0])
            self.combobox.setMinimumWidth(minimal_size[1])

        if stretches is not None:
            self.main_layout.addWidget(self.label, stretches[0])
            self.main_layout.addWidget(self.combobox, stretches[1])
        else:
            self.main_layout.addWidget(self.label)
            self.main_layout.addWidget(self.combobox)

        self.setLayout(self.main_layout)

    def add_items(self, items):
        self.combobox.addItems(items)

    def get_text(self):
        return self.combobox.currentText()

    def clear(self):
        self.combobox.clear()