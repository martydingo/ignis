from ignis.widgets import Widget
from ignis.services.audio import AudioService


class Volume(Widget.EventBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.VolumeLabel = Widget.Label()
        self.VolumeIcon = Widget.Icon(pixel_size=16)

        self.audio = AudioService.get_default()
        self.audio.connect("speaker-added", lambda x, y: self.__handleAudioChange__())

        self.on_scroll_down = lambda x: self.__handleVolumeUp__()
        self.on_scroll_up = lambda x: self.__handleVolumeDown__()

        self.child = [self.VolumeIcon, self.VolumeLabel]
        self.spacing = 4

        self.audio.speaker.bind("volume", lambda x: print(x))

    def __handleAudioChange__(self):
        self.VolumeLabel.label = self.audio.speaker.bind(
            "volume", transform=lambda volumeLevel: f"{str(volumeLevel)}%"
        )
        self.VolumeIcon.image = self.audio.speaker.bind("icon_name")

    def __handleVolumeUp__(self):
        self.audio.speaker.set_volume(self.audio.speaker.volume + 1)

    def __handleVolumeDown__(self):
        self.audio.speaker.set_volume(self.audio.speaker.volume - 1)
