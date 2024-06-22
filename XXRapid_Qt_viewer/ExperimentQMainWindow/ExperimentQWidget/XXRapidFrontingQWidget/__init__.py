from .FrontingFramesQTabWidget import *
from .FrontingExpansionQTabWidget import *


class XXRapidFrontingQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Fronting'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.XXRapidOriginalQWidget = self.parent.XXRapidOriginalQWidget
        self.camera_data_dict = self.XXRapidOriginalQWidget.CameraDataDict
        super().__init__()
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        try:
            self.XXRapidFrontingFramesQTabWidget = XXRapidFrontingFramesQTabWidget(self)
            self.QHBoxLayout.addWidget(self.XXRapidFrontingFramesQTabWidget, stretch=1)
        except Exception as ex:
            print(f'XXRapidFrontingFramesQTabWidget {ex}')
        try:
            self.FrontingExpansionQTabWidget = FrontingExpansionQTabWidget(self)
            self.QHBoxLayout.addWidget(self.FrontingExpansionQTabWidget)
        except Exception as ex:
            print(ex)

    def on_current_quart_changed(self):
        self.XXRapidFrontingExpansionQTabWidget.setCurrentIndex(self.XXRapidFrontingFramesQTabWidget.current_quart - 1)

    def OnXXRapidFrontingFramesQTabWidget(self):
        self.SettingsDict['Fronting_frames'] = self.XXRapidFrontingFramesQTabWidget.SettingsDict
        self.XXRapidFrontingExpansionQTabWidget.set_data(self.XXRapidFrontingFramesQTabWidget.expansion_dict)

    def set_data(self, camera_data_dict):
        self.camera_data_dict = camera_data_dict
        self.changed.emit()
        pass

    def OnXXRapidFrontingExpansionQTabWidget(self):

        self.changed.emit()

    def get_expansion_dict(self):
        # return self.FrontingFramesQTabWidget.expansion_dict
        return self.XXRapidFrontingExpansionQTabWidget.expansion_by_quart_dict

    def test_settings_key(self, key_line):
        if key_line not in self.SettingsDict.keys():
            self.SettingsDict[key_line] = dict()
