from XXRapidFrontingSeparatorQWidget import *
from XXRapidFrontingQuartQTabWidget import *


class XXRapidFrontingSingleFrameQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, camera_data, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.camera_data = camera_data
        self.SettingsDict = settings_dict
        try:
            settings = settings_dict['Separator']
        except:
            settings = dict()
        try:
            self.XXRapidFrontingSeparatorQWidget = XXRapidFrontingSeparatorQWidget(self.camera_data, settings)
            self.addTab(self.XXRapidFrontingSeparatorQWidget, 'Separator')
            self.SettingsDict['Separator'] = self.XXRapidFrontingSeparatorQWidget.SettingsDict
            self.XXRapidFrontingSeparatorQWidget.changed.connect(self.OnXXRapidFrontingSeparatorQWidget)
        except Exception as ex:
            print(f'XXRapidFrontingSeparatorQWidget {ex}')
            return
        self.XXRapidFrontingQuartQTabWidgetDict = dict()
        self.expansion_dict = dict()
        for my_key, my_camera_data in self.XXRapidFrontingSeparatorQWidget.quarts_dict.items():
            try:
                settings = settings_dict[my_key]
            except:
                settings = dict()
            try:
                self.XXRapidFrontingQuartQTabWidgetDict[my_key] = XXRapidFrontingQuartQTabWidget(my_camera_data,
                                                                                                 settings)
                self.SettingsDict[my_key] = self.XXRapidFrontingQuartQTabWidgetDict[my_key].SettingsDict
                self.expansion_dict[my_key] = self.XXRapidFrontingQuartQTabWidgetDict[my_key].get_expansion()
                self.addTab(self.XXRapidFrontingQuartQTabWidgetDict[my_key], my_key)
                self.XXRapidFrontingQuartQTabWidgetDict[my_key].changed.connect(self.OnXXRapidFrontingQuartQTabWidget)
            except Exception as ex:
                print(f'XXRapidFrontingQuartQTabWidgetDict[{my_key}] {ex}')

    def OnXXRapidFrontingQuartQTabWidget(self):
        for mykey, myQuartQWidget in self.XXRapidFrontingQuartQTabWidgetDict.items():
            self.SettingsDict[mykey] = myQuartQWidget.SettingsDict
            self.expansion_dict[mykey] = myQuartQWidget.get_expansion()
        self.changed.emit()

    def OnXXRapidFrontingSeparatorQWidget(self):
        self.SettingsDict['Separator'] = self.XXRapidFrontingSeparatorQWidget.SettingsDict
        try:
            for mykey, myQuartQWidget in self.XXRapidFrontingQuartQTabWidgetDict.items():
                try:
                    myQuartQWidget.set_data(self.XXRapidFrontingSeparatorQWidget.quarts_dict[mykey])
                except Exception as ex:
                    print(f'{mykey}')
        except Exception as ex:
            print(f'XXRapidFrontingQuartQTabWidgetDict {ex}')

        # self.changed.emit()

    def set_data(self, camera_data):
        self.camera_data = camera_data
        self.changed.emit()
