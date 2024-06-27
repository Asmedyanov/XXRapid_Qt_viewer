from SettingsQWidgets.ChildQTabWidget import *
from .QuartQTabWidgetDict import *


class FrontingQuartsQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Quarts')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.SeparatorQWidget = self.parent.SeparatorQWidget
        self.SeparatorQWidget.changed.connect(self.refresh)
        self.camera_data_dict = self.SeparatorQWidget.quarts_dict
        self.QuartQTabWidgetDict = dict()
        self.expansion_dict = self.parent.expansion_dict
        for my_key, my_camera_data in self.camera_data_dict.items():
            self.current_key = my_key
            self.current_camera_data = my_camera_data
            try:
                self.QuartQTabWidgetDict[my_key] = QuartQTabWidget(self)
                self.addTab(self.QuartQTabWidgetDict[my_key], my_key)
                self.QuartQTabWidgetDict[my_key].changed.connect(self.on_quart)
            except Exception as ex:
                print(ex)
        self.currentChanged.connect(self.on_current_changed)

    def on_current_changed(self):
        self.parent.quart_index = self.currentIndex()
        self.parent.currentQuartChanged.emit()

    def on_quart(self):
        self.changed.emit()

    def refresh(self):
        self.camera_data_dict = self.SeparatorQWidget.quarts_dict
        for my_key, my_camera_data in self.camera_data_dict.items():
            self.current_key = my_key
            self.current_camera_data = my_camera_data
            self.QuartQTabWidgetDict[my_key].refresh()
        self.changed.emit()

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        for quart in self.QuartQTabWidgetDict.values():
            try:
                quart.save_report()
            except Exception as ex:
                print(ex)
