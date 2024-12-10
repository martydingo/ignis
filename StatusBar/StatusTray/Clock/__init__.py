from ignis.widgets import Widget
from ignis.utils import Utils
import datetime


class Clock(Widget.EventBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clock = Widget.Label()
        self.child = [self.clock]
        self.mode = "time"

        Utils.Poll(1000, lambda _: self.__updateTime__())

        self.__setLabel__()

        self.on_click = lambda x: self.__handleModeChange__()

    def __updateTime__(self):
        self.curTime = datetime.datetime.now()
        self.__setLabel__()

    def __handleModeChange__(self):
        if self.mode == "time":
            self.mode = "date"
        else:
            self.mode = "time"
        self.__setLabel__()

    def __setLabel__(self):
        match self.mode:
            case "time":
                self.clock.set_label(self.curTime.strftime("%I:%M %p"))
            case "date":
                dayOfMonth = self.curTime.strftime("%d")
                match list(dayOfMonth)[-1]:
                    case 1:
                        dayOfMonth = f"{str(dayOfMonth)}st"
                    case 2:
                        dayOfMonth = f"{str(dayOfMonth)}nd"
                    case 3:
                        dayOfMonth = f"{str(dayOfMonth)}rd"
                    case _:
                        dayOfMonth = f"{str(dayOfMonth)}th"

                self.clock.set_label(
                    f"{self.curTime.strftime("%A %B")} {dayOfMonth} {self.curTime.strftime("%Y")}"
                )
