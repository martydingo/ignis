from ignis.widgets import Widget
from .MusicLevels import MusicLevels
from .MusicMeta import MusicMeta


class MusicTray(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.child = [MusicLevels(), MusicMeta()]
