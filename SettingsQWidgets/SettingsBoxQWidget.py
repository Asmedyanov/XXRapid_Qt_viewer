from SettingsQWidgets.SettingsLineQWidget import *
from PyQt5.QtWidgets import QVBoxLayout


class SettingsBoxQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.QVBoxLayout = QVBoxLayout()
        self.setLayout(self.QVBoxLayout)
        try:
            self.User_comment = SettingsLineQWidget(name='User_comment', default=settings_dict['User_comment'])
        except Exception as ex:
            print(ex)
            self.User_comment = SettingsLineQWidget(name='User_comment', default='User_comment')
        self.User_comment.changed.connect(self.OnSettingsLineChanged)
        self.QVBoxLayout.addWidget(self.User_comment)
        self.SettingsDict = settings_dict
        self.SettingsDict['User_comment'] = self.User_comment.value

    def OnSettingsLineChanged(self):
        self.SettingsDict['User_comment'] = self.User_comment.value
        self.changed.emit()
