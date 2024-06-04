from PyQt5.QtWidgets import QTabWidget
from .XXRapidFrontingTracerQWidget import *
from .XXRapidFrontingFrontQWidget import *


class XXRapidFrontingQuartQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, camera_data, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.camera_data = camera_data
        self.SettingsDict = settings_dict
        key = 'Tracer'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.XXRapidFrontingTracerQWidget = XXRapidFrontingTracerQWidget(self.camera_data, settings)
            self.addTab(self.XXRapidFrontingTracerQWidget, key)
            self.SettingsDict['Tracer'] = self.XXRapidFrontingTracerQWidget.SettingsDict
            self.XXRapidFrontingTracerQWidget.changed.connect(self.OnXXRapidFrontingTracerQWidget)
        except Exception as ex:
            print(f'XXRapidFrontingTracerQWidget {ex}')
            return

        self.XXRapidFrontingFrontQWidgetDict = dict()
        self.front_dict = dict()
        for i in range(3):
            key = f'Front_{i + 1}'
            settings = dict()
            if key in settings_dict.keys():
                settings = settings_dict[key]
            try:
                self.XXRapidFrontingFrontQWidgetDict[key] = XXRapidFrontingFrontQWidget(
                    self,
                    self.XXRapidFrontingTracerQWidget.traced_image,
                    settings)
                self.SettingsDict[key] = self.XXRapidFrontingFrontQWidgetDict[key].SettingsDict
                self.front_dict[key] = self.XXRapidFrontingFrontQWidgetDict[key].get_front_dict()
                self.addTab(self.XXRapidFrontingFrontQWidgetDict[key], key)
                self.XXRapidFrontingFrontQWidgetDict[key].changed.connect(self.OnXXRapidFrontingFrontQWidget)
            except Exception as ex:
                print(f'XXRapidFrontingFrontQWidgetDict[{key}] {ex}')

    def OnXXRapidFrontingFrontQWidget(self):
        for mykey, myfront in self.XXRapidFrontingFrontQWidgetDict.items():
            self.SettingsDict[mykey] = myfront.SettingsDict
            self.front_dict[mykey] = myfront.get_front_dict()
        self.changed.emit()

    def set_data(self, camera_data):
        self.camera_data = camera_data
        self.XXRapidFrontingTracerQWidget.set_data(self.camera_data)

    def OnXXRapidFrontingTracerQWidget(self):
        self.SettingsDict['Tracer'] = self.XXRapidFrontingTracerQWidget.SettingsDict
        for mykey, myfront in self.XXRapidFrontingFrontQWidgetDict.items():
            myfront.set_data(self.XXRapidFrontingTracerQWidget.get_traced_image())
        # self.changed.emit()

    def get_expansion(self):
        try:
            expansion_dict = {
                'Expansion_1': {
                    'shutter': self.XXRapidFrontingFrontQWidgetDict['Front_2'].shutter_order,
                    'x': self.XXRapidFrontingFrontQWidgetDict['Front_1'].x_approx,
                    'expansion': self.XXRapidFrontingFrontQWidgetDict['Front_1'].y_approx -
                                 self.XXRapidFrontingFrontQWidgetDict['Front_2'].y_approx
                },
                'Expansion_2': {
                    'shutter': self.XXRapidFrontingFrontQWidgetDict['Front_3'].shutter_order,
                    'x': self.XXRapidFrontingFrontQWidgetDict['Front_1'].x_approx,
                    'expansion': self.XXRapidFrontingFrontQWidgetDict['Front_1'].y_approx -
                                 self.XXRapidFrontingFrontQWidgetDict['Front_3'].y_approx
                }
            }
        except:
            expansion_dict = {
                'Expansion_1': {
                    'x': self.XXRapidFrontingFrontQWidgetDict['Front_1'].x_approx,
                    'expansion': self.XXRapidFrontingFrontQWidgetDict['Front_1'].x_approx * 0
                },
                'Expansion_2': {
                    'x': self.XXRapidFrontingFrontQWidgetDict['Front_1'].x_approx,
                    'expansion': self.XXRapidFrontingFrontQWidgetDict['Front_1'].x_approx * 0
                }
            }
        return expansion_dict
