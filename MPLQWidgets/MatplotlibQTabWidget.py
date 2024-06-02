from MPLQWidgets.MatplotlibQWidget import *
from PyQt5.QtWidgets import QTabWidget


class MatplotlibQTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if 'dict_to_graph' in kwargs.keys():
            self.dict_to_graph = kwargs['dict_to_graph']
        elif len(args) >= 1:
            self.dict_to_graph = args[0]
        else:
            self.dict_to_graph = dict()

        self.MPLQWidgetDict = dict()
        for my_key, my_data in self.dict_to_graph.items():
            self.MPLQWidgetDict[my_key] = MatplotlibQWidget()
            self.addTab(self.MPLQWidgetDict[my_key], my_key)

    def set_data(self, *args, **kwargs):
        pass
