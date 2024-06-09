from MPLQWidgets.MatplotlibSingeAxQWidget import *
import pandas as pd


class ComsolSimulationQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, parent, filename='Default_shot/Jmax.csv'):
        super().__init__()
        self.parent = parent
        self.filename = filename
        self.df = pd.read_csv(self.filename)
        self.width_list_number, self.comsol_current_density_dict = self.get_comsol_current_density_dict()
        self.ax.set(xlabel='t, ns',
                    ylabel='J$_{edge}, \\times 10^{8} A/cm^2$'
                    )
        self.j_plot_dict = dict()
        for my_key, my_value in self.comsol_current_density_dict.items():
            self.j_plot_dict[my_key], = self.ax.plot(my_value['time'] * 1e9, my_value['density'] * 1e-8, label=my_key)
        self.ax.legend()
        self.t_exp_plot_dict = dict()
        try:
            quart = 2
            self.t_exp_array = np.arange(len(self.width_list_number))
            for i, width in enumerate(self.width_list_number):
                self.t_exp_array[i] = self.parent.XXRapidTOFQTabWidget.get_explosion_time(
                    width=width,
                    quart=quart)
                self.t_exp_plot_dict[width] = self.ax.axvline(self.t_exp_array[i], linestyle=':', c='r')
        except Exception as ex:
            print(ex)

    def get_comsol_current_density_dict(self):
        comsol_current_density_dict = dict()
        time_list = self.df.columns[::2]
        width_list = self.df.columns[1::2]
        width_list_number = np.arange(len(width_list))
        for i, name in enumerate(width_list):
            t_data = self.df[time_list[i]].values
            j_data = self.df[name].values
            t_data = t_data[~np.isnan(t_data)]
            j_data = j_data[~np.isnan(j_data)]
            df = pd.DataFrame({
                'time': t_data,
                'density': j_data
            })
            try:
                width_list_number[i] = float(name.split(' ')[0])
            except Exception as ex:
                print(ex)
                width_list_number[i] = 0
            comsol_current_density_dict[name] = df
        return width_list_number, comsol_current_density_dict
