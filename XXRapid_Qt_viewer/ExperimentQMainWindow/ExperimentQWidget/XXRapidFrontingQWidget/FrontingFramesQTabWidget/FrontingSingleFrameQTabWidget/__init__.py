import os

from .XXRapidFrontingSeparatorQWidget import *
from .XXRapidFrontingQuartQTabWidget import *
from .FrontingQuartsQTabWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class FrontingSingleFrameQTabWidget(ChildQTabWidget):
    currentQuartChanged = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent, parent.current_key)
        self.camera_data = self.parent.current_camera_data
        self.expansion_dict = self.parent.expansion_dict
        self.quart_index = 0
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        try:
            self.SeparatorQWidget = FrontingSeparatorQWidget(self)
            self.addTab(self.SeparatorQWidget, self.SeparatorQWidget.settings_key)
        except Exception as ex:
            print(f'XXRapidFrontingSeparatorQWidget {ex}')
            return
        try:
            self.FrontingQuartsQTabWidget = FrontingQuartsQTabWidget(self)
            self.addTab(self.FrontingQuartsQTabWidget, self.FrontingQuartsQTabWidget.settings_key)
            self.FrontingQuartsQTabWidget.currentChanged.connect(self.on_current_quart_changed)
            self.FrontingQuartsQTabWidget.changed.connect(self.on_quart_data_changed)
        except Exception as ex:
            print(ex)

    def on_quart_data_changed(self):
        self.changed.emit()

    def on_current_quart_changed(self):
        self.parent.quart_index = self.quart_index
        self.currentQuartChanged.emit()

    def on_tab_bar(self):
        index = self.currentIndex()
        if index > 0:
            self.currentQuart = index
            self.currentQuartChanged.emit()

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        try:
            self.SeparatorQWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.FrontingQuartsQTabWidget.save_report()
        except Exception as ex:
            print(ex)
