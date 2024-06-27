from MPLQWidgets.MatplotlibSingeAxQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.report_path = self.parent.report_path
        self.current_expansion_dict = dict(sorted(self.parent.current_expansion_dict.items()))
        self.settings_key = self.parent.current_key
        super().__init__()
        self.expansion_line_dict = dict()
        for my_key, my_expansion in self.current_expansion_dict.items():
            self.expansion_line_dict[my_key], = self.ax.plot(my_expansion['x'], my_expansion['expansion'],
                                                             label=my_key)
        self.ax.legend()

    def refresh(self):
        self.current_expansion_dict = self.parent.current_expansion_dict
        for my_key, my_expansion in self.current_expansion_dict.items():
            self.expansion_line_dict[my_key].set_data(my_expansion['x'], my_expansion['expansion'])
            # self.expansion_line_dict[my_key].set_label(self.expansion_line_dict[my_key])
        self.changed.emit()

    def save_report(self):
        self.figure.savefig(f'{self.report_path}/{self.settings_key}')
