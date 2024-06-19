from SettingsQWidgets.SettingsBoxQWidget import *
from MPLQWidgets.MatplotlibQWidget import *


class SettingsMPLQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        if 'MPLQWidget' in kwargs.keys():
            self.MPLQWidget = kwargs['MPLQWidget']
        elif len(args) >= 1:
            self.MPLQWidget = args[0]
        else:
            self.MPLQWidget = MatplotlibQWidget()
        self.QHBoxLayout.addWidget(self.MPLQWidget, stretch=1)

        if 'settings_box' in kwargs.keys():
            self.SettingsBox = kwargs['settings_box']
        elif len(args) >= 2:
            self.SettingsBox = args[1]
        else:
            self.SettingsBox = SettingsBoxQWidget()
        self.QHBoxLayout.addWidget(self.SettingsBox)
        self.SettingsBox.changed.connect(self.on_settings_box)
        self.SettingsDict = self.SettingsBox.SettingsDict

    def on_settings_box(self):
        self.MPLQWidget.changed.emit()
        self.changed.emit()

    def set_data(self, *args, **kwargs):
        self.MPLQWidget.set_data(**kwargs)
        pass

    def save_report(self, folder_name='./'):
        self.MPLQWidget.save_report(folder_name)
