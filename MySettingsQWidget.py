from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox


class MySettingsQWidget(QWidget):
    def __init__(self, name='name', default=0, comment='_', options_list=None):
        super().__init__()
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.NameLabel = QLabel(name)
        self.QHBoxLayout.addWidget(self.NameLabel)
        if options_list is None:
            self.QLineEdit = QLineEdit(f'{default}')
            self.QHBoxLayout.addWidget(self.QLineEdit)
            self.value = float(default)
        else:
            self.QComboBox = QComboBox()
            self.QComboBox.addItems(options_list)
            self.QHBoxLayout.addWidget(self.QComboBox)
            self.value = self.QComboBox.currentText()
        self.CommentLabel = QLabel(comment)
        self.QHBoxLayout.addWidget(self.CommentLabel)
