from .Graphics import *
import pandas as pd
from SettingsQWidgets.ChildQTabWidget import *


class ComsolCurrentQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Current_density')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.folder_path = self.parent.folder_path
        self.folder_list = self.parent.folder_list
        self.TOFResultQTabWidget = self.parent.TOFResultQTabWidget
        self.file_name = self.get_file_name()
        try:
            self.comsol_current_df = pd.read_csv(self.file_name)
        except Exception as ex:
            print(ex)
            return
        self.tof_dict = self.TOFResultQTabWidget.velocity_dict
        self.TOFResultQTabWidget.changed.connect(self.refresh)
        self.CAI_dict = dict()
        self.Graphics_dict = dict()
        for my_key, my_df in self.tof_dict.items():
            self.current_key = my_key
            self.current_df = my_df
            self.CAI_dict[my_key] = dict()
            try:
                self.Graphics_dict[my_key] = Graphics(self)
                self.addTab(self.Graphics_dict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def refresh(self):
        self.tof_dict = self.TOFResultQTabWidget.velocity_dict
        for my_key, my_df in self.tof_dict.items():
            self.current_key = my_key
            self.current_df = my_df
            try:
                self.Graphics_dict[my_key].refresh()
            except Exception as ex:
                print(ex)
        self.changed.emit()

    def get_file_name(self):
        files_list = [name for name in self.folder_list if
                      name.startswith('Jmax') and name.endswith('csv')]
        return f'{self.folder_path}/{files_list[-1]}'

    def on_settings_box(self):
        try:
            quart = int(self.SettingsBox.Quart_line.value)
            df_list = list(self.comsol_current_density_dict.values())
            for i, width in enumerate(self.width_list_number):
                self.t_exp_array[i] = self.parent.XXRapidTOFQTabWidget.get_explosion_time(
                    width=width,
                    quart=quart)
                j_df = df_list[i]
                j_df = j_df.loc[j_df['time'] * 1e9 < self.t_exp_array[i]]
                self.j_exp_array[i] = j_df['density'].values[-1]
                self.h_exp_array[i] = j_df['action'].values.sum()
                self.t_exp_plot_dict[width].set_xdata(self.t_exp_array[i])
        except Exception as ex:
            print(ex)
        super().on_settings_box()

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
                'density': j_data,
                'action': j_data ** 2 * np.gradient(t_data)
            })
            try:
                width_list_number[i] = float(name.split(' ')[0])
            except Exception as ex:
                print(ex)
                width_list_number[i] = 0
            comsol_current_density_dict[name] = df
        return width_list_number, comsol_current_density_dict

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        for graphics in self.Graphics_dict.values():
            try:
                graphics.save_report()
            except Exception as ex:
                print(ex)
