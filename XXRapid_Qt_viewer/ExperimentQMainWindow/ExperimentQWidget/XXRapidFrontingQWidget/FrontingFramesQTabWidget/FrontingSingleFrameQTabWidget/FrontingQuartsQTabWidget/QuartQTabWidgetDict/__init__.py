from SettingsQWidgets.ChildQTabWidget import *
from .TracerQWidget import *
from .FrontsQTabWidget import *

'''from .XXRapidFrontingTracerQWidget import *
from .XXRapidFrontingFrontQWidget import *
from .SkimageOverlappedQWidget import *'''


class QuartQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, parent.current_key)
        self.camera_data = self.parent.current_camera_data
        if self.settings_key not in self.parent.expansion_dict.keys():
            self.parent.expansion_dict[self.settings_key] = dict()
        self.expansion_dict = self.parent.expansion_dict[self.settings_key]
        try:
            self.TracerQWidget = TracerQWidget(self)
            self.addTab(self.TracerQWidget, self.TracerQWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.FrontsQTabWidget = FrontsQTabWidget(self)
            self.addTab(self.FrontsQTabWidget, self.FrontsQTabWidget.settings_key)
            self.FrontsQTabWidget.changed.connect(self.on_fronts_changed)
        except Exception as ex:
            print(ex)

    def on_fronts_changed(self):
        self.changed.emit()

    def refresh(self):
        self.camera_data = self.parent.current_camera_data
        self.TracerQWidget.refresh()

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
