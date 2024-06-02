from MatplotlibSingeAxQWidget import *


class GraphicsQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, motion_list, motion_approximated_list, index_to_plot_list):
        super().__init__()
        self.PlotList = []
        self.ax.set(
            title='Motion',
            xlabel='t, ns',
            ylabel='expansion, mm',
        )
        '''for i in index_to_plot_list:
            # for expansion in motion_list:
            self.PlotList.append(
                self.ax.plot(motion_list[i]['time'], motion_list[i]['expansion'], '-o',
                             label=f'w = {int(motion_list[i]["width"])} mm')[0]
            )'''
        index = index_to_plot_list[0]

        self.plot_1 = \
            self.ax.plot(motion_list[index]['time'], motion_list[index]['expansion'],
                         '-o',
                         label=f'w = {int(motion_list[index]["width"])} mm')[0]
        if index >= len(motion_approximated_list):
            index = len(motion_approximated_list) - 1
        if index < 0:
            index = 0
        self.plot_1_a = \
            self.ax.plot(motion_approximated_list[index]['t_approx'],
                         motion_approximated_list[index]['expansion_approx'])[0]
        index = index_to_plot_list[-1]

        self.plot_2 = \
            self.ax.plot(motion_list[index]['time'], motion_list[index]['expansion'],
                         '-o',
                         label=f'w = {int(motion_list[index_to_plot_list[1]]["width"])} mm')[0]
        if index >= len(motion_approximated_list):
            index = len(motion_approximated_list) - 1
        if index < 0:
            index = 0
        self.plot_2_a = \
            self.ax.plot(motion_approximated_list[index]['t_approx'],
                         motion_approximated_list[index]['expansion_approx'])[0]
        self.ax.legend()

    def set_data(self, motion_list, motion_approximated_list, index_to_plot_list):
        index = index_to_plot_list[0]
        self.plot_1.set_data(motion_list[index]['time'],
                             motion_list[index]['expansion'])
        self.plot_1.set_label(f'w = {motion_list[index]["width"]:3.1f} mm')
        if index >= len(motion_approximated_list):
            index = len(motion_approximated_list) - 1
        if index < 0:
            index = 0

        self.plot_1_a.set_data(motion_approximated_list[index]['t_approx'],
                               motion_approximated_list[index]['expansion_approx'])
        index = index_to_plot_list[-1]

        self.plot_2.set_data(motion_list[index]['time'],
                             motion_list[index]['expansion'])
        self.plot_2.set_label(f'w = {motion_list[index]["width"]:3.1f} mm')
        if index >= len(motion_approximated_list):
            index = len(motion_approximated_list) - 1
        if index < 0:
            index = 0

        self.plot_2_a.set_data(motion_approximated_list[index]['t_approx'],
                               motion_approximated_list[index]['expansion_approx'])
        self.ax.legend()

        self.changed.emit()
