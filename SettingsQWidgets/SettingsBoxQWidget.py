from .SettingsLineQWidget import *
from PyQt5.QtWidgets import QVBoxLayout


class SettingsBoxQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.SettingsDict = settings_dict
        self.QVBoxLayout = QVBoxLayout()
        self.setLayout(self.QVBoxLayout)
        key = 'User_comment'
        default = self.test_key(key, key)
        self.User_comment = SettingsLineQWidget(name=key, default=default)
        self.SettingsDict[key] = self.User_comment.value
        self.User_comment.changed.connect(self.on_settings_line_changed)
        self.QVBoxLayout.addWidget(self.User_comment)

    def test_key(self, key_line, default_line='default'):
        default = default_line
        if key_line in self.SettingsDict.keys():
            default = self.SettingsDict[key_line]
            if type(default_line) in [float, int]:
                default = float(default)
                if type(default_line) is float:
                    return default
                return int(default)
        return default

    def on_settings_line_changed(self):
        self.SettingsDict['User_comment'] = self.User_comment.value
        self.changed.emit()
