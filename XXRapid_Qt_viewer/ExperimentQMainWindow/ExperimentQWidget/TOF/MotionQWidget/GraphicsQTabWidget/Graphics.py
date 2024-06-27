from MPLQWidgets.MatplotlibSingeAxQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.index_to_plot_list = self.parent.index_to_plot_list
        self.motion_list = self.parent.current_motion_list
        self.motion_approximated_list = self.parent.current_motion_approx_list
        self.settings_key = self.parent.current_key
        self.report_path = self.parent.report_path
        super().__init__()
        self.PlotList = []
        self.ax.set(
            title='Motion',
            xlabel='t, ns',
            ylabel='expansion, mm',
        )

        index = self.index_to_plot_list[0]

        self.plot_1 = \
            self.ax.plot(self.motion_list[index]['time'] * 1e9, self.motion_list[index]['expansion'],
                         '-o',
                         label=f'w = {int(self.motion_list[index]["width"])} mm')[0]
        if index >= len(self.motion_approximated_list):
            index = len(self.motion_approximated_list) - 1
        if index < 0:
            index = 0
        self.plot_1_a = \
            self.ax.plot(self.motion_approximated_list[index]['t_approx'],
                         self.motion_approximated_list[index]['expansion_approx'])[0]
        index = self.index_to_plot_list[-1]

        self.plot_2 = \
            self.ax.plot(self.motion_list[index]['time'] * 1e9, self.motion_list[index]['expansion'],
                         '-o',
                         label=f'w = {int(self.motion_list[self.index_to_plot_list[1]]["width"])} mm')[0]
        if index >= len(self.motion_approximated_list):
            index = len(self.motion_approximated_list) - 1
        if index < 0:
            index = 0
        self.plot_2_a = \
            self.ax.plot(self.motion_approximated_list[index]['t_approx'],
                         self.motion_approximated_list[index]['expansion_approx'])[0]
        self.ax.legend()

    def refresh(self):
        self.index_to_plot_list = self.parent.index_to_plot_list
        self.motion_list = self.parent.current_motion_list
        self.motion_approximated_list = self.parent.current_motion_approx_list
        index = self.index_to_plot_list[0]
        self.plot_1.set_data(self.motion_list[index]['time'] * 1e9,
                             self.motion_list[index]['expansion'])
        self.plot_1.set_label(f'w = {self.motion_list[index]["width"]:3.1f} mm')
        if index >= len(self.motion_approximated_list):
            index = len(self.motion_approximated_list) - 1
        if index < 0:
            index = 0

        self.plot_1_a.set_data(self.motion_approximated_list[index]['t_approx'],
                               self.motion_approximated_list[index]['expansion_approx'])
        index = self.index_to_plot_list[-1]

        self.plot_2.set_data(self.motion_list[index]['time'] * 1e9,
                             self.motion_list[index]['expansion'])
        self.plot_2.set_label(f'w = {self.motion_list[index]["width"]:3.1f} mm')
        if index >= len(self.motion_approximated_list):
            index = len(self.motion_approximated_list) - 1
        if index < 0:
            index = 0

        self.plot_2_a.set_data(self.motion_approximated_list[index]['t_approx'],
                               self.motion_approximated_list[index]['expansion_approx'])
        self.ax.legend()

        self.changed.emit()

    def save_report(self):
        self.figure.savefig(f'{self.report_path}/{self.settings_key}')
