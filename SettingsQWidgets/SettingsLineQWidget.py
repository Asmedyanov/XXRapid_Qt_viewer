from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox
from PyQt5.QtCore import pyqtSignal


class SettingsLineQWidget(QWidget):
    changed = pyqtSignal()

    # def __init__(self, name='name', default=0, comment='_', options_list=None, limit=None, step=None):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.name = 'Default'
        self.default = 0
        self.comment = '_'
        if len(args) > 0:
            self.name = args[0]
        elif 'name' in kwargs.keys():
            self.name = kwargs['name']
        if len(args) > 1:
            self.default = args[1]
        elif 'default' in kwargs.keys():
            self.default = kwargs['default']
        if len(args) > 2:
            self.comment = args[2]
        elif 'comment' in kwargs.keys():
            self.comment = kwargs['comment']
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.NameLabel = QLabel(self.name)
        self.QHBoxLayout.addWidget(self.NameLabel)
        if 'options_list' in kwargs.keys():
            self.options_list = kwargs['options_list']
            self.QComboBox = QComboBox()
            self.QComboBox.addItems(self.options_list)
            if self.default in self.options_list:
                self.QComboBox.setCurrentText(self.default)
            self.QHBoxLayout.addWidget(self.QComboBox)
            self.QComboBox.currentTextChanged.connect(self.OnQComboBoxChanged)
            self.value = self.QComboBox.currentText()

        elif 'limit' in kwargs.keys():
            self.limit = kwargs['limit']
            if type(self.default) is int:
                self.QSpinBox = QSpinBox()
            else:
                self.QSpinBox = QDoubleSpinBox()
            self.QHBoxLayout.addWidget(self.QSpinBox)
            self.QSpinBox.setRange(self.limit[0], self.limit[-1])
            self.QSpinBox.setValue(self.default)
            if 'step' in kwargs.keys():
                self.step = kwargs['step']
                self.QSpinBox.setSingleStep(self.step)
            self.value = self.QSpinBox.value()
            # self.QSpinBox.editingFinished.connect(self.OnQSpinBoxChanged)
            self.QSpinBox.editingFinished.connect(self.OnQSpinBoxChanged)

        else:
            self.QLineEdit = QLineEdit(f'{self.default}')
            self.QLineEdit.editingFinished.connect(self.OnQLineEditChanged)
            self.QHBoxLayout.addWidget(self.QLineEdit)
            self.value = self.QLineEdit.text()

        self.CommentLabel = QLabel(self.comment)
        self.QHBoxLayout.addWidget(self.CommentLabel)

    def OnQSpinBoxChanged(self):
        self.value = float(self.QSpinBox.value())
        self.changed.emit()

    def OnQLineEditChanged(self):
        '''try:
            self.value = float(self.QLineEdit.text())
        except:
            self.value = self.QLineEdit.text()'''
        self.value = self.QLineEdit.text()
        self.changed.emit()

    def OnQComboBoxChanged(self):
        self.value = self.QComboBox.currentText()
        self.changed.emit()

    def setValue(self, value):
        my_value = value
        if type(self.QSpinBox) in [QSpinBox, QDoubleSpinBox]:
            my_value = float(my_value)
            if type(self.QSpinBox) is QSpinBox:
                my_value = int(my_value)
        self.QSpinBox.setValue(my_value)
        self.value = float(self.QSpinBox.value())

        # self.OnQSpinBoxChanged()
