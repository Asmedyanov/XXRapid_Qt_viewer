from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal


class SettingsLineQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, name='name', default=0, comment='_', options_list=None, limit=None, step=None):
        super().__init__()
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.NameLabel = QLabel(name)
        self.QHBoxLayout.addWidget(self.NameLabel)
        if options_list is not None:
            self.QComboBox = QComboBox()
            self.QComboBox.addItems(options_list)
            try:
                self.QComboBox.setCurrentText(default)
            except:
                pass
            self.QHBoxLayout.addWidget(self.QComboBox)
            self.QComboBox.currentTextChanged.connect(self.OnQComboBoxChanged)
            self.value = self.QComboBox.currentText()

        elif limit is not None:
            self.QSpinBox = QDoubleSpinBox()
            self.QHBoxLayout.addWidget(self.QSpinBox)
            self.QSpinBox.setRange(limit[0], limit[-1])
            self.QSpinBox.setValue(float(default))
            self.QSpinBox.setSingleStep(float(step))
            self.value = self.QSpinBox.value()
            self.QSpinBox.editingFinished.connect(self.OnQSpinBoxChanged)

        else:
            self.QLineEdit = QLineEdit(f'{default}')
            self.QLineEdit.editingFinished.connect(self.OnQLineEditChanged)
            self.QHBoxLayout.addWidget(self.QLineEdit)
            try:
                self.value = float(self.QLineEdit.text())
            except Exception as ex:
                print(ex)
                self.value = self.QLineEdit.text()

        self.CommentLabel = QLabel(comment)
        self.QHBoxLayout.addWidget(self.CommentLabel)

    def OnQSpinBoxChanged(self):
        self.value = float(self.QSpinBox.value())
        self.changed.emit()

    def OnQLineEditChanged(self):
        try:
            self.value = float(self.QLineEdit.text())
        except:
            self.value = self.QLineEdit.text()
        self.changed.emit()

    def OnQComboBoxChanged(self):
        try:
            self.value = float(self.QLineEdit.text())
        except Exception as ex:
            print(ex)
            self.value = self.QLineEdit.text()
        self.changed.emit()
