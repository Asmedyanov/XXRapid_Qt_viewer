from scipy import ndimage
from skimage.filters.rank import threshold

from .Settings import *
from MPLQWidgets.SettingsMPLQWidget import *
from MPLQWidgets.MatplotlibSingeAxQWidget import *
import numpy as np
from scipy.ndimage import binary_fill_holes, binary_hit_or_miss, rotate
from skimage import filters, morphology, segmentation
import skimage


class XXRapidOverlappedCameraQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = self.parent.current_key
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=Settings(self)
        )
        self.camera_data = self.parent.current_camera_data
        # self.MPLQWidget.ax.set(title=f'{self.settings_key}, mm')
        self.dx = 1.0 / self.SettingsBox.ScaleSettingLine.value
        self.degree = self.SettingsBox.RotationSettingLine.value
        self.sigma_before = self.SettingsBox.SigmaBeforeLine.value
        self.sigma_shot = self.SettingsBox.SigmaShotLine.value
        self.sigma_overlapped = self.SettingsBox.SigmaOverlappedLine.value
        self.mask_threshold = self.SettingsBox.MaskThresholdSettingLine.value
        self.OverlappedImage, self.extent = self.get_overlapped_image

        self.imshow = self.MPLQWidget.ax.imshow(self.OverlappedImage, extent=self.extent)

    @property
    def get_extent(self):
        extent = [-self.OverlappedImage.shape[1] * self.dx // 2,
                  self.OverlappedImage.shape[1] * self.dx // 2,
                  self.OverlappedImage.shape[0] * self.dx // 2,
                  -self.OverlappedImage.shape[0] * self.dx // 2]
        return extent

    def get_mask(self, before_image):
        thresh = np.where(
            before_image > 1e-2 * np.max(before_image[np.nonzero(before_image)]) * self.mask_threshold, 1, 0
        )
        labeled_array, num_features = ndimage.label(thresh)

        # Compute the sizes of all components
        component_sizes = ndimage.sum(thresh, labeled_array, range(1, num_features + 1))

        # Find the label of the largest component
        largest_component_label = np.argmax(component_sizes) + 1

        # Calculate the centroid of the largest component
        centroid = ndimage.center_of_mass(thresh, labeled_array, largest_component_label)

        # Extract the coordinates of the largest component's pixels
        component_coords = np.argwhere(labeled_array == largest_component_label)

        # Compute the Euclidean distance of each point from the centroid
        distances = np.sqrt((component_coords[:, 0] - centroid[0]) ** 2 + (component_coords[:, 1] - centroid[1]) ** 2)
        line_thresh = component_coords[:, 0].max()

        # The radius is the maximum distance
        radius = np.max(distances)
        mask = np.zeros_like(thresh)
        for i in range(thresh.shape[0]):
            for j in range(thresh.shape[1]):
                if (i - centroid[0]) ** 2 + (j - centroid[1]) ** 2 < radius ** 2:
                    if i < line_thresh:
                        mask[i, j] = 1
        edges = {
            'top': np.argwhere(mask)[:, 1].min(),
            'bottom': np.argwhere(mask)[:, 1].max(),
            'left': np.argwhere(mask)[:, 0].min(),
            'right': np.argwhere(mask)[:, 0].max(),
        }

        return mask, edges

    @property
    def get_overlapped_image(self):
        """

        :return:
        """
        before_image = filters.gaussian(self.camera_data['before'],
                                        sigma=self.sigma_before)
        before_image = rotate(before_image, self.degree)
        shot_image = filters.gaussian(self.camera_data['shot'],
                                      sigma=self.sigma_shot)
        shot_image = rotate(shot_image, self.degree)
        mask, edges = self.get_mask(before_image)

        '''shadow_image = np.where(shot_image < before_image,
                                # + before_image.std(),
                                shot_image,
                                before_image)  # + before_image.std())'''

        overlapped_image = np.where(before_image <= 0, 0,
                                    shot_image / before_image) * mask
        overlapped_image = filters.gaussian(overlapped_image, sigma=self.sigma_overlapped)
        # overlapped_image = rotate(overlapped_image, self.degree, reshape=False)
        overlapped_image = overlapped_image[
                           edges['left']:edges['right'],
                           edges['top']: edges['bottom']
                           ]
        w = edges['right']-edges['left']
        h = edges['bottom']-edges['top']
        c_x = 0.5*(edges['right']+edges['left']-before_image.shape[0])
        c_y = 0.5*(edges['bottom']+edges['top']-before_image.shape[1])
        extent = [(c_y-0.5*h) * self.dx,
                  (c_y+0.5*h) * self.dx,
                  (c_x + 0.5 * w) * self.dx,
                  (c_x - 0.5 * w) * self.dx]


        return overlapped_image, extent

    def on_settings_box(self):
        self.dx = 1.0 / self.SettingsBox.ScaleSettingLine.value
        self.degree = self.SettingsBox.RotationSettingLine.value
        self.sigma_before = self.SettingsBox.SigmaBeforeLine.value
        self.sigma_shot = self.SettingsBox.SigmaShotLine.value
        self.sigma_overlapped = self.SettingsBox.SigmaOverlappedLine.value
        self.mask_threshold = self.SettingsBox.MaskThresholdSettingLine.value
        self.OverlappedImage, self.extent = self.get_overlapped_image
        self.imshow.set_extent(self.extent)
        self.imshow.set_data(self.OverlappedImage)
        super().on_settings_box()

    def save_report(self):
        self.MPLQWidget.figure.savefig(f'{self.parent.report_path}/{self.settings_key}_full.png')
        fig_w, fig_h = self.MPLQWidget.figure.get_size_inches()
        new_w = 6.0  # inch
        new_h = fig_h * new_w / fig_w
        self.MPLQWidget.figure.set_size_inches(new_w, new_h)
        self.MPLQWidget.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')
        self.MPLQWidget.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.svg')
        self.MPLQWidget.figure.set_size_inches(fig_w, fig_h)
        # self.imshow.imsave(f'{self.parent.report_path}/{self.settings_key}_im.png')
