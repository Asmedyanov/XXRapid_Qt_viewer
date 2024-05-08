from Matplotlib_qtwidget import Matplotlib_qtwidget
import numpy as np
from scipy.ndimage import gaussian_filter


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
        for i in range(4):
            self.ax[i].imshow(self.Overlapped_image[i], cmap='gray', extent=extent)
        self.figure.canvas.draw()

    def set_data(self, before_image_array, shot_image_array, dx):
        self.dx = dx
        overlapped_list = []
        for i in range(before_image_array.shape[0]):
            before_image = gaussian_filter(before_image_array[i], sigma=1)
            shot_image = gaussian_filter(shot_image_array[i], sigma=1)
            overlapped = np.where(shot_image > before_image, 1, shot_image/before_image)
            mask = np.where(before_image <= before_image.mean(), 0, 1)
            overlapped = overlapped * mask
            overlapped =gaussian_filter(overlapped,sigma=1)
            overlapped_list.append(overlapped)
        '''overlapped = np.where(shot_image_array > before_image_array, before_image_array,
                              shot_image_array)
        mask_list = []
        for i in range(4):
            mask = np.where(before_image_array[i] <= before_image_array[i].mean(), 0, 1)
            mask_list.append(mask)
        mask = np.array(mask_list)
        overlapped = np.where(before_image_array > 0, overlapped / before_image_array, 0) * mask
        self.Overlapped_image = overlapped'''
        self.Overlapped_image = np.array(overlapped_list)
        self.redraw()
        self.changed.emit()
