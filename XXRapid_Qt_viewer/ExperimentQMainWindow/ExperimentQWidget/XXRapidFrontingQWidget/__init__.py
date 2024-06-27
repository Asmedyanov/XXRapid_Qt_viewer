from .FrontingFramesQTabWidget import *
from .FrontingExpansionQTabWidget import *


class XXRapidFrontingQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Fronting'
        self.parent.test_settings_key(self.settings_key)
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.XXRapidOriginalQWidget = self.parent.XXRapidOriginalQWidget
        self.camera_data_dict = self.XXRapidOriginalQWidget.CameraDataDict
        self.quart_index = 0
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
            self.FrontingExpansionQTabWidget.changed.connect(self.on_expansion_changed)
        except Exception as ex:
            print(ex)

    def on_expansion_changed(self):
        if self.parent.auto_refresh:
            self.changed.emit()
        else:
            self.parent.statusBar.showMessage(f'Fronting is changed. Please rebuild')

    def on_current_quart_changed(self):
        self.XXRapidFrontingExpansionQTabWidget.setCurrentIndex(self.XXRapidFrontingFramesQTabWidget.current_quart - 1)

    def test_settings_key(self, key_line):
        if key_line not in self.SettingsDict.keys():
            self.SettingsDict[key_line] = dict()

    def save_report(self):
        try:
            self.XXRapidFrontingFramesQTabWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.FrontingExpansionQTabWidget.save_report()
        except Exception as ex:
            print(ex)
