import os

from .FrontingSingleFrameQTabWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class XXRapidFrontingFramesQTabWidget(ChildQTabWidget):
    currentQuartChanged = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent, 'Fronting_frames')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.camera_data_dict = self.parent.camera_data_dict
        self.FrontingSingleFrameQTabWidgetDict = dict()
        self.expansion_dict = dict()
        self.quart_index = 0
        for my_key, my_camera_data in self.camera_data_dict.items():
            self.current_key = my_key
            self.current_camera_data = my_camera_data
            try:
                self.FrontingSingleFrameQTabWidgetDict[my_key] = FrontingSingleFrameQTabWidget(self)
                self.FrontingSingleFrameQTabWidgetDict[my_key].changed.connect(self.on_frame)
                self.FrontingSingleFrameQTabWidgetDict[my_key].currentQuartChanged.connect(
                    self.on_current_quart_changed)
                self.addTab(self.FrontingSingleFrameQTabWidgetDict[my_key], my_key)
            except Exception as ex:
                print(f'XXRapidFrontingSingleFrameQTabWidgetDict[{my_key}] {ex}')

    def on_current_quart_changed(self):
        self.parent.quart_index = self.quart_index
        self.currentQuartChanged.emit()

    def on_frame(self):
        self.changed.emit()

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        for frame in self.FrontingSingleFrameQTabWidgetDict.values():
            try:
                frame.save_report()
            except Exception as ex:
                print(ex)
