from .SettingsBoxQWidget import *


class SettingsQWidget2(QWidget):
    changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        if (len(args) == 0) and (len(kwargs) == 0):
            self.SettingsBox = SettingsBoxQWidget()
            self.MainWidget = QWidget()
        elif len(args) == 2:
            self.MainWidget = args[0]
            self.SettingsBox = args[1]
        else:
            self.MainWidget = kwargs['main_widget']
            self.SettingsBox = kwargs['settings_box']
        self.QHBoxLayout.addWidget(self.MainWidget, stretch=1)
        self.QHBoxLayout.addWidget(self.SettingsBox)
        self.SettingsDict = self.SettingsBox.SettingsDict
        self.SettingsBox.changed.connect(self.on_settings_box)

    def on_settings_box(self):
        self.SettingsDict = self.SettingsBox.SettingsDict
        self.changed.emit()
