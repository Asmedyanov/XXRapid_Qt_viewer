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
            self.QHBoxLayout.addWidget(self.XXRapidFrontingFramesQTabWidget, stretch=1)
            self.SettingsDict['Fronting_frames'] = self.XXRapidFrontingFramesQTabWidget.SettingsDict
            self.XXRapidFrontingFramesQTabWidget.changed.connect(self.OnXXRapidFrontingFramesQTabWidget)
            self.XXRapidFrontingFramesQTabWidget.currentQuartChanged.connect(self.on_current_quart_changed)
        except Exception as ex:
            print(f'XXRapidFrontingFramesQTabWidget {ex}')
        try:
            self.XXRapidFrontingExpansionQTabWidget = XXRapidFrontingExpansionQTabWidget(
                self.XXRapidFrontingFramesQTabWidget.expansion_dict)
            self.XXRapidFrontingExpansionQTabWidget.changed.connect(self.OnXXRapidFrontingExpansionQTabWidget)
            self.QHBoxLayout.addWidget(self.XXRapidFrontingExpansionQTabWidget)
        except Exception as ex:
            print(f'XXRapidFrontingExpansionQTabWidget {ex}')

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
        return self.XXRapidFrontingFramesQTabWidget.expansion_dict
