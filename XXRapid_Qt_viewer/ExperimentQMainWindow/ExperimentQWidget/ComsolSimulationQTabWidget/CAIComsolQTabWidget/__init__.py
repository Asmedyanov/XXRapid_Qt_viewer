import pandas as pd
from .Graphics import *

from SettingsQWidgets.ChildQTabWidget import *


class CAIComsolQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'CAI_Comsol')
        self.ComsolCurrentQTabWidget = self.parent.ComsolCurrentQTabWidget
        self.CAI_dict = self.ComsolCurrentQTabWidget.CAI_dict
        self.Graphics_dict = dict()
        for my_key, my_dict in self.CAI_dict.items():
            self.current_key = my_key
            self.current_dict = my_dict
            try:
                self.Graphics_dict[my_key] = Graphics(self)
                self.addTab(self.Graphics_dict[my_key], my_key)
            except Exception as ex:
                print(ex)
