from .XXRapidFrontingSeparatorQWidget import *
from .XXRapidFrontingQuartQTabWidget import *
from .FrontingQuartsQTabWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class FrontingSingleFrameQTabWidget(ChildQTabWidget):
    currentQuartChanged = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent, parent.current_key)
        self.camera_data = self.parent.current_camera_data
        self.expansion_dict = self.parent.expansion_dict
        self.quart_index = 0
        try:
            self.SeparatorQWidget = FrontingSeparatorQWidget(self)
            self.addTab(self.SeparatorQWidget, self.SeparatorQWidget.settings_key)
        except Exception as ex:
            print(f'XXRapidFrontingSeparatorQWidget {ex}')
            return
        try:
            self.FrontingQuartsQTabWidget = FrontingQuartsQTabWidget(self)
            self.addTab(self.FrontingQuartsQTabWidget, self.FrontingQuartsQTabWidget.settings_key)
            self.FrontingQuartsQTabWidget.currentChanged.connect(self.on_current_quart_changed)
            self.FrontingQuartsQTabWidget.changed.connect(self.on_quart_data_changed)
        except Exception as ex:
            print(ex)

    def on_quart_data_changed(self):
        self.changed.emit()

    def on_current_quart_changed(self):
        self.parent.quart_index = self.quart_index
        self.currentQuartChanged.emit()
        '''self.expansion_dict = dict()
        self.tabBarDoubleClicked.connect(self.on_tab_bar)
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
                self.currentQuart = self.currentIndex()
                self.XXRapidFrontingQuartQTabWidgetDict[my_key].changed.connect(self.OnXXRapidFrontingQuartQTabWidget)
            except Exception as ex:
                print(f'XXRapidFrontingQuartQTabWidgetDict[{my_key}] {ex}')'''

    def on_tab_bar(self):
        index = self.currentIndex()
        if index > 0:
            self.currentQuart = index
            self.currentQuartChanged.emit()

    def OnXXRapidFrontingQuartQTabWidget(self):
        for mykey, myQuartQWidget in self.XXRapidFrontingQuartQTabWidgetDict.items():
            self.SettingsDict[mykey] = myQuartQWidget.SettingsDict
            self.expansion_dict[mykey] = myQuartQWidget.get_expansion()
        self.changed.emit()

    def OnXXRapidFrontingSeparatorQWidget(self):
        self.SettingsDict['Separator'] = self.SeparatorQWidget.SettingsDict
        try:
            for mykey, myQuartQWidget in self.XXRapidFrontingQuartQTabWidgetDict.items():
                try:
                    myQuartQWidget.set_data(self.SeparatorQWidget.quarts_dict[mykey])
                except Exception as ex:
                    print(f'{mykey}')
        except Exception as ex:
            print(f'XXRapidFrontingQuartQTabWidgetDict {ex}')

        # self.changed.emit()

    def set_data(self, camera_data):
        self.camera_data = camera_data
        self.changed.emit()
