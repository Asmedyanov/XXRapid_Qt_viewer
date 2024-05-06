from Matplotlib_qtwidget import Matplotlib_qtwidget
import numpy as np


class Four_overlapped_frames(Matplotlib_qtwidget):
    def __init__(self):
        super().__init__()
        gs = self.figure.add_gridspec(ncols=4)
        self.ax = gs.subplots()
        for i in range(4):
            self.ax[i].set(
                title=f'Image {i + 1}'
            )

    def transverse(self):
        transpose_list = []
        for i in range(4):
            transpose_list.append(self.Overlapped_image[i].transpose())
        self.Overlapped_image = np.array(transpose_list)
        self.redraw()
        self.changed.emit()

    def redraw(self):
        extent = [-self.Overlapped_image.shape[2] * self.dx // 2,
                  self.Overlapped_image.shape[2] * self.dx // 2,
                  self.Overlapped_image.shape[1] * self.dx // 2,
                  -self.Overlapped_image.shape[1] * self.dx // 2]
        pass
        for i in range(4):
            self.ax[i].imshow(self.Overlapped_image[i], cmap='gray', extent=extent)
        self.figure.canvas.draw()

    def set_data(self, before_image_array, shot_image_array, dx):
        self.dx = dx
        overlapped = np.where(shot_image_array > before_image_array, before_image_array,
                              shot_image_array)
        mask_list = []
        for i in range(4):
            mask = np.where(before_image_array[i] <= before_image_array[i].mean(), 0, 1)
            mask_list.append(mask)
        mask = np.array(mask_list)
        overlapped = np.where(before_image_array > 1, overlapped / before_image_array, 1) * mask
        self.Overlapped_image = overlapped
        self.redraw()
        self.changed.emit()
