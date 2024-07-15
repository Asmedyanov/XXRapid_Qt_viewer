from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class PowerEnergyQWidget(MatplotlibSingeAxTwinxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Energy_per_mass'
        super().__init__()
        self.ax.set(xlabel='t, us', ylabel='$Energy density rate,\\times 10^{10}  W/g$')
        self.ax_2.set(ylabel='$Energy density,\\times 10^4  J/g$')
        self.mass = self.parent.mass
        self.PowerQWidget = self.parent.WaveformQTabWidget.PowerQWidget
        self.df_power = self.PowerQWidget.df_power.copy()
        self.df_power['Units'] /= self.mass
        self.EnergyQWidget = self.parent.WaveformQTabWidget.EnergyQWidget
        self.df_energy = self.EnergyQWidget.df_energy.copy()
        self.df_energy['Units'] /= self.mass
        self.power_plot, = self.ax.plot(self.df_power['time'] * 1e6, self.df_power['Units'] * 1e-10)
        self.energy_plot, = self.ax_2.plot(self.df_energy['time'] * 1e6, self.df_energy['Units'] * 1e-4, 'r')

    def refresh(self):
        self.mass = self.parent.mass
        self.df_power = self.PowerQWidget.df_power.copy()
        self.df_power['Units'] /= self.mass
        self.df_energy = self.EnergyQWidget.df_energy.copy()
        self.df_energy['Units'] /= self.mass
        self.power_plot.set_data(self.df_power['time']*1e6 , self.df_power['Units']* 1e-10)
        self.energy_plot.set_data(self.df_energy['time']*1e6 , self.df_energy['Units']* 1e-4)
        self.changed.emit()

    def save_report(self, folder_name=None):
        self.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')

    def save_origin_pro(self, op):
        workbook = op.new_book(lname='Energy per mass')
        graph = op.new_graph(template='Energy_per_mass', lname='Energy per mass')
        sheet = workbook.add_sheet(name='Power')
        sheet.from_dict({
            'time, us': self.df_power['time'].values,
            'Power, GW/g': self.df_power['Units'].values,
        })

        plot_power = graph[0].add_plot(sheet, colx=0, coly=1, type='line')
        graph[0].rescale()
        graph[0].set_xlim(begin=0, end=self.df_power['time'].max())
        graph[0].set_ylim(begin=0, end=self.df_power['Units'].max())

        sheet = workbook.add_sheet(name='Energy')
        sheet.from_dict({
            'time, us': self.df_energy['time'].values,
            'Energy, J/g': self.df_energy['Units'].values,
        })
        plot_energy = graph[1].add_plot(sheet, colx=0, coly=1, type='line')
        graph[1].rescale()
        graph[1].set_xlim(begin=0, end=self.df_energy['time'].max())
        graph[1].set_ylim(begin=0, end=self.df_energy['Units'].max())
