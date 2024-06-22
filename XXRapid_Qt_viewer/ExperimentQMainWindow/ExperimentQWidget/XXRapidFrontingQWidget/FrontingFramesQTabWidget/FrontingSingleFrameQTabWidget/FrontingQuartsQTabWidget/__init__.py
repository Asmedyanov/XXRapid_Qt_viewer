from SettingsQWidgets.ChildQTabWidget import *
from .QuartQTabWidgetDict import *


class FrontingQuartsQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Quarts')
        self.SeparatorQWidget = self.parent.SeparatorQWidget
        self.SeparatorQWidget.changed.connect(self.refresh)
        self.camera_data_dict = self.SeparatorQWidget.quarts_dict
        self.QuartQTabWidgetDict = dict()
        for my_key, my_camera_data in self.camera_data_dict.items():
            self.current_key = my_key
            self.current_camera_data = my_camera_data
            try:
                self.QuartQTabWidgetDict[my_key] = QuartQTabWidget(self)
                self.addTab(self.QuartQTabWidgetDict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def refresh(self):
        self.camera_data_dict = self.SeparatorQWidget.quarts_dict
        for my_key, my_camera_data in self.camera_data_dict.items():
            self.current_key = my_key
            self.current_camera_data = my_camera_data
            self.QuartQTabWidgetDict[my_key].refresh()
        self.changed.emit()
