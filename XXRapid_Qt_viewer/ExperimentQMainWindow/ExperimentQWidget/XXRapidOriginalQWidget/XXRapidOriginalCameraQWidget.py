from MPLQWidgets.MatplotlibQWidget import *


class XXRapidOriginalCameraQWidget(MatplotlibQWidget):
    def __init__(self, image_before, image_shot):
        super().__init__()
        gs = self.figure.add_gridspec(ncols=2)
        self.ax = gs.subplots()
        self.ax[0].set(title='Before', xlabel='pix', ylabel='pix')
        self.ax[1].set(title='Shot', xlabel='pix', ylabel='pix')
        self.imshow_before = self.ax[0].imshow(image_before)
        self.imshow_short = self.ax[1].imshow(image_shot)
