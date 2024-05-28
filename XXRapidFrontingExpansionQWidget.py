from MatplotlibSingeAxQWidget import *


class XXRapidFrontingExpansionQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, expansion_list):
        super().__init__()
        self.expansion_line_list = []
        for expansion in expansion_list:
            self.expansion_line_list.append(
                self.ax.plot(expansion['x'], expansion['expansion'])[0]
            )

    def set_data(self, expansion_list):
        for i, expansion in enumerate(expansion_list):
            self.expansion_line_list[i].set_data(
                expansion['x'], expansion['expansion']
            )
        self.changed.emit()