from ignis.widgets import Widget
from ignis.utils import Utils
import datetime


class Clock(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        clock = Widget.Label()

        self.child = [clock]

        Utils.Poll(1000, lambda _: self.__updateTime__(clock))

    def __updateTime__(self, labelWidget: Widget.Label):
        curTime = datetime.datetime.now().strftime("%H:%M:%S")
        labelWidget.set_label(curTime)
