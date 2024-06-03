from MatplotlibQWidget import MatplotlibQWidget


class Quart_plots_widget(MatplotlibQWidget):
    def __init__(self):
        super().__init__()
        gs = self.figure.add_gridspec(ncols=4)
        self.ax = gs.subplots()
        self.plot_by_quarts = dict()
        for i in [1, 2, 3, 4]:
            key = f'Quart_{i}'
            self.ax[i - 1].set(title=key)
            self.plot_by_quarts[key] = []
