from PyQt5.QtWidgets import QTabWidget
from .Graphics import *
from SettingsQWidgets.ChildQTabWidget import *


class FrontingExpansionQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Expansion')
        self.XXRapidFrontingFramesQTabWidget = self.parent.XXRapidFrontingFramesQTabWidget
        self.expansion_dict = self.parent.XXRapidFrontingFramesQTabWidget.expansion_dict

        self.ExpansionQWidgetDict = dict()
        self.expansion_by_quart_dict = dict()
        for i in range(4):
            key = f'Quart_{i + 1}'
            try:
                expansion_list = []
                for frame_key, frame in self.expansion_dict.items():
                    expansion_list.append(frame[key]['Expansion_1'])
                    expansion_list.append(frame[key]['Expansion_2'])
                self.current_expansion_list = expansion_list
                self.ExpansionQWidgetDict[key] = Graphics(self)
                self.ExpansionQWidgetDict[key].changed.connect(
                    self.on_ExpansionQWidgetDict)
                self.expansion_by_quart_dict[key] = expansion_list
                self.addTab(self.ExpansionQWidgetDict[key], key)
            except Exception as ex:
                print(f'self.XXRapidFrontingExpansionQWidgetDict[{key}] {ex}')

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
                self.ExpansionQWidgetDict[key].set_data(expansion_list)
            except Exception as ex:
                print(f'self.XXRapidFrontingExpansionQWidgetDict[{key}] {ex}')
        self.changed.emit()
