from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import pyqtSignal


class MySettingsQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, name='name', default=0, comment='_', options_list=None):
        super().__init__()
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.NameLabel = QLabel(name)
        self.QHBoxLayout.addWidget(self.NameLabel)
        if options_list is None:
            self.QLineEdit = QLineEdit(f'{default}')
            self.QLineEdit.editingFinished.connect(self.OnQLineEditChanged)
            self.QHBoxLayout.addWidget(self.QLineEdit)
            self.value = float(self.QLineEdit.text())
        else:
            self.QComboBox = QComboBox()
            self.QComboBox.addItems(options_list)
            try:
                self.QComboBox.setCurrentText(default)
            except:
                pass
            self.QHBoxLayout.addWidget(self.QComboBox)
            self.QComboBox.currentTextChanged.connect(self.OnQComboBoxChanged)
            self.value = self.QComboBox.currentText()
        self.CommentLabel = QLabel(comment)
        self.QHBoxLayout.addWidget(self.CommentLabel)

    def OnQLineEditChanged(self):
        self.value = float(self.QLineEdit.text())
        self.changed.emit()

    def OnQComboBoxChanged(self):
        self.value = self.QComboBox.currentText()
        self.changed.emit()
