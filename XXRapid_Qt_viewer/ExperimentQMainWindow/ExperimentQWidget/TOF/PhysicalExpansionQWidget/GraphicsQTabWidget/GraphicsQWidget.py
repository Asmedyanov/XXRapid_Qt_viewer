from MPLQWidgets.MatplotlibSingeAxQWidget import *


class GraphicsQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.expansion_dict = self.parent.current_expansion_data
        self.current_key = self.parent.current_key
        super().__init__()
        self.plot_dict = dict()
        self.ax.set(
            title='Physical expansion',
            xlabel='width, mm',
            ylabel='expansion, mm',
        )
        for my_shutter, my_expansion in self.expansion_dict.items():
            time = int(my_expansion['time'] * 1e9)
            self.plot_dict[my_shutter], = self.ax.plot(my_expansion['width'], my_expansion['expansion'],
                                                       label=f'{time} ns')
        self.ax.legend()

    def refresh(self):
        self.expansion_dict = self.parent.current_expansion_data
        self.current_key = self.parent.current_key
        for my_shutter, my_expansion in self.expansion_dict.items():
            time = int(my_expansion['time'] * 1e9)
            self.plot_dict[my_shutter].set_data(my_expansion['width'], my_expansion['expansion'])
            self.plot_dict[my_shutter].set_label(f'{time} ns')
        self.ax.legend()
        self.changed.emit()

    def set_data(self, expansion_list, time_list):
        for i, expansion in enumerate(expansion_list):
            self.PlotList[i].set_data(expansion['Width'], expansion['expansion'])
            self.PlotList[i].set_label(f'{expansion["Time"]} ns')
        self.ax.legend()
        self.changed.emit()
