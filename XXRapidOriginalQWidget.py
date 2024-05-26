from PyQt5.QtWidgets import QTabWidget

class XXRapidOriginalQWidget(QTabWidget):
    def __init__(self,before_name='Default_shot/before.rtv',shot_name='Default_shot/shot57.rtv'):
        super().__init__()
        self.XXRapidOriginalCameraQWidgetDict = dict()
