from MPLQWidgets.SettingsMPLQWidget import *
from MPLQWidgets.MatplotlibSingeAxQWidget import *
from .Settings import *
from scipy import ndimage, misc
from scipy.ndimage import binary_fill_holes, binary_hit_or_miss
from skimage import filters


class XXRapidRotationQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Rotation'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.XXRapidOriginalQWidget = self.parent.XXRapidOriginalQWidget
        self.camera_dict = self.XXRapidOriginalQWidget.CameraDataDict
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=Settings(self)
        )
        self.angle_dict = self.get_angle_dict()
        self.rotated_image = self.get_rotated_image()

        self.imshow = self.MPLQWidget.ax.imshow(self.rotated_image)

    def get_angle_dict(self):
        angle_dict = {}
        for my_key, my_widget in self.SettingsBox.frame_dict.items():
            angle_dict[my_key] = my_widget.value
        return angle_dict

    def get_rotated_image(self):
        rotated_image = np.zeros(self.camera_dict['Camera_1']['before'].shape)
        # for my_key, my_angle in self.angle_dict.items():
        for i in [1, 2, 3, 4]:
            my_key = f'Camera_{i}'
            original_image = self.camera_dict[my_key]['before']
            original_image = filters.gaussian(original_image,
                                              sigma=1.0)
            thresh = np.where(
                original_image > 10e-2 * np.max(original_image[np.nonzero(original_image)]), 1, 0)
            fill = binary_fill_holes(thresh)*i
            rotated_image += ndimage.rotate(fill, self.angle_dict[my_key], reshape=False)
        return rotated_image

    def on_settings_box(self):
        self.angle_dict = self.get_angle_dict()
        self.rotated_image = self.get_rotated_image()
        self.imshow.set_data(self.rotated_image)
        super().on_settings_box()
