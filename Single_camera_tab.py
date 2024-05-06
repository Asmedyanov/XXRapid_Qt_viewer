from PyQt5.QtWidgets import QTabWidget
from Single_camera_widget import Single_camera_widget


class Single_camera_tab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.camera_dict = dict()
        for i in range(4):
            key = f'Camera_{i + 1}'
            self.camera_dict[key] = Single_camera_widget()
            self.addTab(self.camera_dict[key], key)

    def set_data(self, image_array_1, image_array_2):
        for i in range(4):
            key = f'Camera_{i + 1}'
            self.camera_dict[key].set_data(image_array_1[i],image_array_2[i])
