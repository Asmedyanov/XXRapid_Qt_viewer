from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from XXRapidFrontingSeparatorQWidget import *
from XXRapidFrontingQuartQTabWidget import *


class XXRapidFrontingSingleFrameQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, camera_data, settings_dict=None):
        super().__init__()
        self.camera_data = camera_data
        self.SettingsDict = dict()
        try:
            settings = settings_dict['Separator']
        except:
            settings = None
        try:
            self.XXRapidFrontingSeparatorQWidget = XXRapidFrontingSeparatorQWidget(self.camera_data, settings)
            self.addTab(self.XXRapidFrontingSeparatorQWidget, 'Separator')
            self.SettingsDict['Separator'] = self.XXRapidFrontingSeparatorQWidget.SettingsDict
            self.XXRapidFrontingSeparatorQWidget.changed.connect(self.OnXXRapidFrontingSeparatorQWidget)
        except Exception as ex:
            print(f'XXRapidFrontingSeparatorQWidget {ex}')
            return
        self.XXRapidFrontingQuartQTabWidgetDict = dict()
        for mykey, mycameradata in self.XXRapidFrontingSeparatorQWidget.quarts_dict.items():
            try:
                settings = settings_dict[mykey]
            except:
                settings = None
            try:
                self.XXRapidFrontingQuartQTabWidgetDict[mykey] = XXRapidFrontingQuartQTabWidget(mycameradata, settings)
                self.SettingsDict[mykey] = self.XXRapidFrontingQuartQTabWidgetDict[mykey].SettingsDict
                self.addTab(self.XXRapidFrontingQuartQTabWidgetDict[mykey], mykey)
                self.XXRapidFrontingQuartQTabWidgetDict[mykey].changed.connect(self.OnXXRapidFrontingQuartQTabWidget)
            except Exception as ex:
                print(f'XXRapidFrontingQuartQTabWidgetDict[{mykey}] {ex}')

    def OnXXRapidFrontingQuartQTabWidget(self):
        for mykey, myQuartQWidget in self.XXRapidFrontingQuartQTabWidgetDict.items():
            self.SettingsDict[mykey] = myQuartQWidget.SettingsDict
        self.changed.emit()

    def OnXXRapidFrontingSeparatorQWidget(self):
        self.SettingsDict['Separator'] = self.XXRapidFrontingSeparatorQWidget.SettingsDict
        for mykey, myQuartQWidget in self.XXRapidFrontingQuartQTabWidgetDict.items():
            myQuartQWidget.set_data(self.XXRapidFrontingSeparatorQWidget.quarts_dict[mykey])
        # self.changed.emit()

    def set_data(self, camera_data):
        self.camera_data = camera_data
        self.changed.emit()
