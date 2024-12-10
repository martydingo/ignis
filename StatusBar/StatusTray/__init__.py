from ignis.widgets import Widget

from .Clock import Clock
from .Tray import Tray
from .Volume import Volume


class StatusTray(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.child = [
            Tray(),
            Volume(),
            Clock(),
        ]

        self.spacing = 8
