from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTabWidget
from XXRapidFrontingExpansionQWidget import *


class XXRapidFrontingExpansionQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, expansion_dict):
        super().__init__()
        self.XXRapidFrontingExpansionQWidgetDict = dict()
        for i in range(4):
            key = f'Quart_{i + 1}'
            try:
                expansion_list = []
                for frame_key, frame in expansion_dict.items():
                    expansion_list.append(frame[key]['Expansion_1'])
                    expansion_list.append(frame[key]['Expansion_2'])
                self.XXRapidFrontingExpansionQWidgetDict[key] = XXRapidFrontingExpansionQWidget(expansion_list)
                self.addTab(self.XXRapidFrontingExpansionQWidgetDict[key], key)
            except Exception as ex:
                print(f'self.XXRapidFrontingExpansionQWidgetDict[{key}] {ex}')
    def set_data(self,expansion_dict):
        for i in range(4):
            key = f'Quart_{i + 1}'
            try:
                expansion_list = []
                for frame_key, frame in expansion_dict.items():
                    expansion_list.append(frame[key]['Expansion_1'])
                    expansion_list.append(frame[key]['Expansion_2'])
                self.XXRapidFrontingExpansionQWidgetDict[key].set_data(expansion_list)
            except Exception as ex:
                print(f'self.XXRapidFrontingExpansionQWidgetDict[{key}] {ex}')
