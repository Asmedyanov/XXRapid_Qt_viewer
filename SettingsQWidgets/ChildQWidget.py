from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal


class ChildQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, parent, settings_key='default'):
        self.parent = parent
        self.settings_key = settings_key
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        super().__init__()

    def test_settings_key(self, key_line):
        if key_line not in self.SettingsDict.keys():
            self.SettingsDict[key_line] = dict()
