from XXRapidFrontingFramesQTabWidget import *
from XXRapidFrontingExpansionQTabWidget import *


class XXRapidFrontingQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, camera_data_dict, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.camera_data_dict = camera_data_dict
        self.SettingsDict = dict()
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        try:
            settings = settings_dict['Fronting_frames']
        except:
            settings = dict()
        try:
            self.XXRapidFrontingFramesQTabWidget = XXRapidFrontingFramesQTabWidget(self.camera_data_dict, settings)
            self.QHBoxLayout.addWidget(self.XXRapidFrontingFramesQTabWidget)
            self.SettingsDict['Fronting_frames'] = self.XXRapidFrontingFramesQTabWidget.SettingsDict
            self.XXRapidFrontingFramesQTabWidget.changed.connect(self.OnXXRapidFrontingFramesQTabWidget)
        except Exception as ex:
            print(f'XXRapidFrontingFramesQTabWidget {ex}')
        try:
            self.XXRapidFrontingExpansionQTabWidget = XXRapidFrontingExpansionQTabWidget(
                self.XXRapidFrontingFramesQTabWidget.expansion_dict)
            self.QHBoxLayout.addWidget(self.XXRapidFrontingExpansionQTabWidget)
        except Exception as ex:
            print(f'XXRapidFrontingExpansionQTabWidget {ex}')

    def OnXXRapidFrontingFramesQTabWidget(self):
        self.SettingsDict['Fronting_frames'] = self.XXRapidFrontingFramesQTabWidget.SettingsDict
        self.XXRapidFrontingExpansionQTabWidget.set_data(self.XXRapidFrontingFramesQTabWidget.expansion_dict)

    def set_data(self, camera_data_dict):
        self.camera_data_dict = camera_data_dict
        self.changed.emit()
        pass
