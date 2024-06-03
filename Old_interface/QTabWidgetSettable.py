from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal


class QTabWidgetSettable(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SettingsDict = self.getSettingsDict()
        self.changed.connect(self.OnChanged)
        self.currentChanged.connect(self.OnChanged)

    def getSettingsDict(self):
        SettingsDict = dict()
        '''for kid in self.children():
            try:
                print(f'{kid}')
                SettingsDict[f'{kid.__str__()}'] = kid.getSettingsDict()
            except Exception as ex:
                print(ex)'''
        return SettingsDict

    def OnChanged(self):
        self.SettingsDict = self.getSettingsDict()
