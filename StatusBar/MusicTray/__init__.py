from ignis.widgets import Widget
from .MusicLevels import MusicLevels


class MusicTray(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.child = [MusicLevels()]
