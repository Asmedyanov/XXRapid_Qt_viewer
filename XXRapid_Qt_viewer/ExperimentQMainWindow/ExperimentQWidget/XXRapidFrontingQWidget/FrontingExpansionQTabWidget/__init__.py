from PyQt5.QtWidgets import QTabWidget
from .Graphics import *
from SettingsQWidgets.ChildQTabWidget import *


class FrontingExpansionQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Expansion')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.XXRapidFrontingFramesQTabWidget = self.parent.XXRapidFrontingFramesQTabWidget
        self.XXRapidFrontingFramesQTabWidget.changed.connect(self.on_fronts)
        self.XXRapidFrontingFramesQTabWidget.currentQuartChanged.connect(self.on_current_quart_changed)
        self.expansion_dict = self.parent.XXRapidFrontingFramesQTabWidget.expansion_dict

        self.GraphicsDict = dict()
        self.expansion_by_quart_dict = dict()
        for my_key, my_expansion_dict in self.expansion_dict.items():
            self.current_key = my_key
            self.current_expansion_dict = my_expansion_dict
            try:
                self.GraphicsDict[my_key] = Graphics(self)
                self.addTab(self.GraphicsDict[my_key], my_key)
            except Exception as ex:
                print(ex)
        try:
            self.GraphicsDict[list(self.GraphicsDict.keys())[-1]].changed.connect(self.on_graphics)
        except Exception as ex:
            print(ex)

    def on_current_quart_changed(self):
        self.setCurrentIndex(self.parent.quart_index)

    def on_fronts(self):
        self.expansion_dict = self.parent.XXRapidFrontingFramesQTabWidget.expansion_dict
        self.refresh()

    def refresh(self):
        for my_key, my_expansion_dict in self.expansion_dict.items():
            self.current_key = my_key
            self.current_expansion_dict = my_expansion_dict
            try:
                self.GraphicsDict[my_key].refresh()
            except Exception as ex:
                print(ex)

    def on_graphics(self):
        self.changed.emit()

    def save_report(self):
        os.makedirs(self.report_path,exist_ok=True)
        for graphics in self.GraphicsDict.values():
            try:
                graphics.save_report()
            except Exception as ex:
                print(ex)

