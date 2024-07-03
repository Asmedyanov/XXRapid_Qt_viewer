from MPLQWidgets.MatplotlibQWidget import *
import numpy as np
from io import BytesIO
from PIL import Image


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

    def save_origin_pro(self, op):
        pass
        # Save the image to a BytesIO object
        '''image = Image.fromarray(self.image_before)
        buf = BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)

        # Create a new graph window in Origin
        graph = op.new_graph(lname=f'{self.settings_key}_before')

        # Add the image to the graph layer
        layer = graph[0]
        layer.import_image(buf)

        # Save the image to a BytesIO object
        image = Image.fromarray(self.image_shot)
        buf = BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)

        # Create a new graph window in Origin
        graph = op.new_graph(lname=f'{self.settings_key}_shot')

        # Add the image to the graph layer
        layer = graph[0]
        layer.import_image(buf)'''
