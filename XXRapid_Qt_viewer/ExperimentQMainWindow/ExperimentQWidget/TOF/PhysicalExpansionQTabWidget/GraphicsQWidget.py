from Old_interface.MatplotlibSingeAxQWidget import *


class GraphicsQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, expansion_list, time_list):
        super().__init__()
        self.PlotList = []
        self.ax.set(
            title='Physical expansion',
            xlabel='width, mm',
            ylabel='expansion, mm',
        )
        for expansion in expansion_list:
            self.PlotList.append(
                self.ax.plot(expansion['Width'], expansion['expansion'], label=f'{expansion["Time"]} ns')[0]
            )
        self.ax.legend()

    def set_data(self, expansion_list, time_list):
        for i, expansion in enumerate(expansion_list):
            self.PlotList[i].set_data(expansion['Width'], expansion['expansion'])
            self.PlotList[i].set_label(f'{expansion["Time"]} ns')
        self.ax.legend()
        self.changed.emit()
