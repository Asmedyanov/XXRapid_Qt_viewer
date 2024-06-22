from MPLQWidgets.MatplotlibSingeAxQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.expansion_list = self.parent.current_expansion_list
        super().__init__()
        self.expansion_line_list = []
        for expansion in self.expansion_list:
            self.expansion_line_list.append(
                self.ax.plot(expansion['x'], expansion['expansion'], label=f'shutter {expansion["shutter"]}')[0]
            )
        self.ax.legend()

    def refresh(self):
        self.expansion_list = self.parent.current_expansion_list
        for i, expansion in enumerate(self.expansion_list):
            self.expansion_line_list[i].set_data(
                expansion['x'], expansion['expansion']
            )
            self.expansion_line_list[i].set_label(f'shutter {expansion["shutter"]}')
        self.changed.emit()
