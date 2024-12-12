from ignis.widgets import Widget
from ignis.services.mpris import MprisService, MprisPlayer
import math


class MusicMeta(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mpris: MprisService = MprisService.get_default()
        self.mpris.connect("player_added", self.__handleMprisChange__)

    def __handleMprisChange__(
        self, mprisService: MprisService, mprisPlayer: MprisPlayer
    ):
        if self.__assessMprisPlayer__(mprisPlayer) == True:
            mprisWidget = self.createMprisWidget(mprisPlayer)
            self.child = [mprisWidget]

    def __assessMprisPlayer__(self, mprisPlayer):
        if mprisPlayer.desktop_entry == "io.github.mavit.slimpris2":
            if mprisPlayer.title == None:
                return False

        if (
            mprisPlayer.playback_status != "Paused"
            and mprisPlayer.playback_status != "Playing"
        ):
            return False

        return True

    def createMprisWidget(self, mprisPlayer):
        mediaLabelTitle = Widget.Label(halign="center", label=mprisPlayer.bind("title"))

        mediaLabelArtist = Widget.Label(label=mprisPlayer.bind("artist"))
        mediaLabelDelimiter = Widget.Label(label=" ~ ")
        mediaLabelAlbum = Widget.Label(label=mprisPlayer.bind("album"))

        mediaLabelContainerArtistAlbum = Widget.Box(
            css_classes=["mediaLabelContainerArtistAlbum"],
            halign="center",
            child=[mediaLabelArtist, mediaLabelDelimiter, mediaLabelAlbum],
        )

        mediaSliderScale = Widget.Scale(
            halign="baseline_fill",
            css_classes=["MusicMetaScale"],
            width_request=len(mprisPlayer.title) * 5,
            height_request=1,
            max=mprisPlayer.bind("length"),
            value=mprisPlayer.bind("position"),
        )

        mediaSliderPositionLabel = Widget.Label(
            halign="start",
            css_classes=["MediaPositionLabel"],
            label=mprisPlayer.bind(
                "position",
                transform=lambda position: f"{"0" if round(math.floor(position/60)) < 10 else ""}{str(round(math.floor(position/60)))}:{"0" if round(math.floor(position%60)) < 10 else ""}{str(position%60)}",
            ),
        )

        mediaSliderDelimiterLabel = Widget.Label(
            halign="start", css_classes=["MediaPositionLabel"], label=" / "
        )
        mediaSliderLengthLabel = Widget.Label(
            halign="start",
            css_classes=["MediaPositionLabel"],
            label=mprisPlayer.bind(
                "length",
                transform=lambda length: f"{"0" if round(math.floor(length/60)) < 10 else ""}{str(round(math.floor(length/60)))}:{"0" if round(math.floor(length%60)) < 10 else ""}{str(length%60)}",
            ),
        )
        mediaSliderLabels = Widget.Box(
            # halign="start",
            # halign="center",
            child=[
                mediaSliderPositionLabel,
                mediaSliderDelimiterLabel,
                mediaSliderLengthLabel,
            ],
        )

        mediaSlider = Widget.Box(
            # vertical=True,
            # style="margin: 4px 0px;",
            halign="baseline_center",
            valign="fill",
            child=[mediaSliderLabels, mediaSliderScale],
        )

        mediaCoverArtPicture = Widget.Picture(
            halign="fill",
            valign="start",
            content_fit="cover",
            css_classes=["MusicMetaCoverArt"],
            image=mprisPlayer.bind("art_url"),
            # width=128,
        )

        mprisMetaWidget = Widget.Box(
            valign="fill",
            css_classes=["MusicMeta"],
            vertical=True,
            child=[mediaLabelTitle, mediaLabelContainerArtistAlbum, mediaSlider],
        )

        mprisWidget = Widget.Overlay(
            css_classes=["MusicMetaOverlay"],
            # halign="baseline_center",
            child=mediaCoverArtPicture,
            overlays=[mprisMetaWidget],
        )

        return mprisWidget
