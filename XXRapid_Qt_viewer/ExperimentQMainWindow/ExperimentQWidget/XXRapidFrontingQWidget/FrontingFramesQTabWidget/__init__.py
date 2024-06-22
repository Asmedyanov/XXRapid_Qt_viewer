from .FrontingSingleFrameQTabWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class XXRapidFrontingFramesQTabWidget(ChildQTabWidget):
    currentQuartChanged = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent, 'Fronting_frames')
        self.camera_data_dict = self.parent.camera_data_dict
        self.XXRapidFrontingSingleFrameQTabWidgetDict = dict()
        self.expansion_dict = dict()
        for my_key, my_camera_data in self.camera_data_dict.items():
            try:
                self.current_key = my_key
                self.current_camera_data = my_camera_data
                self.XXRapidFrontingSingleFrameQTabWidgetDict[my_key] = FrontingSingleFrameQTabWidget(self)
                self.addTab(self.XXRapidFrontingSingleFrameQTabWidgetDict[my_key], my_key)
            except Exception as ex:
                print(f'XXRapidFrontingSingleFrameQTabWidgetDict[{my_key}] {ex}')

    def on_currentQuartChanged(self):
        self.current_quart = self.currentWidget().currentQuart
        self.currentQuartChanged.emit()

    def OnXXRapidFrontingSingleFrameQTabWidgetDict(self):
        for mykey, mycamera, in self.XXRapidFrontingSingleFrameQTabWidgetDict.items():
            self.SettingsDict[mykey] = mycamera.SettingsDict
            self.expansion_dict[mykey] = mycamera.expansion_dict
        self.changed.emit()

    def set_data(self, camera_data_dict):
        self.camera_data_dict = camera_data_dict
        for mykey, mycamera, in self.XXRapidFrontingSingleFrameQTabWidgetDict.items():
            mycamera.set_data(self.camera_data_dict[mykey])
        self.changed.emit()
