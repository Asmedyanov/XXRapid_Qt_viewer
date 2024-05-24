from PyQt5.QtWidgets import QWidget, QVBoxLayout
from SettingsLineQWidget import *
from PyQt5.QtCore import pyqtSignal


class WaveformTimingPointSettingsQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, settings_dict=None):
        super().__init__()

        self.QVBoxLayout = QVBoxLayout()
        self.setLayout(self.QVBoxLayout)
        self.SettingsDict = dict()
        if settings_dict is None:

            self.TimeSettingsQWidget = SettingsLineQWidget(
                name='Time',
                limit=[-1e6, 1e6],
                step=1.0,
                comment='ns'
            )
        else:
            self.TimeSettingsQWidget = SettingsLineQWidget(
                name='Time',
                default=settings_dict['Time'],
                limit=[-1e6, 1e6],
                step=1.0,
                comment='ns'
            )
        self.SettingsDict['Time'] = self.TimeSettingsQWidget.value

        self.TimeSettingsQWidget.changed.connect(self.OnTimeSettingsQWidget)
        self.QVBoxLayout.addWidget(self.TimeSettingsQWidget)

    def OnTimeSettingsQWidget(self):
        self.SettingsDict['Time'] = self.TimeSettingsQWidget.value
        self.changed.emit()
