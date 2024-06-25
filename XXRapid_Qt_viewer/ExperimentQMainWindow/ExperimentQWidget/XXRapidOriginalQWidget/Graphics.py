from MPLQWidgets.MatplotlibQWidget import *


class Graphics(MatplotlibQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = self.parent.current_key
        self.camera_data = self.parent.current_camera_data
        self.image_before = self.camera_data['before']
        self.image_shot = self.camera_data['shot']
        super().__init__()
        gs = self.figure.add_gridspec(ncols=2)
        self.ax = gs.subplots()
        self.ax[0].set(title='Before, pix')
        self.ax[1].set(title='Shot, pix')
        self.ax[0].grid(ls=':')
        self.ax[1].grid(ls=':')
        self.imshow_before = self.ax[0].imshow(self.image_before)
        self.imshow_short = self.ax[1].imshow(self.image_shot)

    def save_report(self):
        self.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')
