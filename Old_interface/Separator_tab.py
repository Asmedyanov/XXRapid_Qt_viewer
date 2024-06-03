from MatplotlibQWidget import MatplotlibQWidget

class Separator_widget(MatplotlibQWidget):

    def __init__(self):
        super().__init__()
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(linestyle='dotted')
        self.cid_1 = self.figure.canvas.mpl_connect('button_press_event', self.On_mouse_click)

    def On_mouse_click(self, event):
        self.center_x, self.center_y = int(event.xdata), int(event.ydata)
        self.Horizont.set_data([0, self.image_width - 1], [self.center_y, self.center_y])
        self.Vertical.set_data([self.center_x, self.center_x], [0, self.image_hight - 1])
        self.figure.canvas.draw()
        self.changed.emit()

    def set_data(self, array_1, dx, base_dict=None):
        self.ax.imshow(array_1, cmap='gray')
        if base_dict is None:
            self.center_x = array_1.shape[1] // 2
            self.center_y = array_1.shape[0] // 2
        else:
            print('i took from file')
            self.center_x = int(base_dict['center_x'])
            self.center_y = int(base_dict['center_y'])
        self.image_width = array_1.shape[1]
        self.image_hight = array_1.shape[0]
        try:
            self.Horizont.set_data([0, self.image_width - 1], [self.center_y, self.center_y])
            self.Vertical.set_data([self.center_x, self.center_x], [0, self.image_hight - 1])
        except:
            self.Horizont, = self.ax.plot([0, self.image_width - 1], [self.center_y, self.center_y])
            self.Vertical, = self.ax.plot([self.center_x, self.center_x], [0, self.image_hight - 1])
        self.figure.canvas.draw()

    def get_data_dict(self):
        ret = {
            'center_x': self.center_x,
            'center_y': self.center_y,
        }
        return ret
