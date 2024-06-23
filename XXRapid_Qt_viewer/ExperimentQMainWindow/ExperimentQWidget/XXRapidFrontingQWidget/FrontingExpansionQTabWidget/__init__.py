from PyQt5.QtWidgets import QTabWidget
from .Graphics import *
from SettingsQWidgets.ChildQTabWidget import *


class FrontingExpansionQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Expansion')
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

    def on_ExpansionQWidgetDict(self):
        pass
        # self.changed.emit()

    def set_data(self, expansion_dict):
        for i in range(4):
            key = f'Quart_{i + 1}'
            try:
                expansion_list = []
                for frame_key, frame in expansion_dict.items():
                    expansion_list.append(frame[key]['Expansion_1'])
                    expansion_list.append(frame[key]['Expansion_2'])
                self.GraphicsDict[key].set_data(expansion_list)
            except Exception as ex:
                print(f'self.XXRapidFrontingExpansionQWidgetDict[{key}] {ex}')
        self.changed.emit()
