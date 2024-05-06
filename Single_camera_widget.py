from Matplotlib_qtwidget import Matplotlib_qtwidget


class Single_camera_widget(Matplotlib_qtwidget):
    def __init__(self):
        super().__init__()
        # Create a Matplotlib figure and axis
        gs = self.figure.add_gridspec(ncols=2)
        self.ax = gs.subplots()

        self.ax[0].grid(linestyle='dotted')
        self.ax[1].grid(linestyle='dotted')
        self.ax[0].set(
            title='before',
        )
        self.ax[1].set(
            title='shot',
            yticklabels=[]
        )

    def set_data(self, image_1, image_2):
        self.ax[0].imshow(image_1)
        self.ax[1].imshow(image_2)
        self.figure.canvas.draw()
