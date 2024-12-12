from ignis.widgets import Widget
from .StatusTray import StatusTray
from .Workspaces import Workspaces
from .MusicTray import MusicTray

import os
from ignis.app import IgnisApp


class StatusBar:
    def __init__(self):
        os.system(
            "/nix/store/wb64hycr7wy5bb07dqx82h4ay94j2kc8-system-path/bin/pkill cava"
        )
        app = IgnisApp.get_default()

        centerBox = Widget.CenterBox(
            name="StatusBar",
            vertical=False,
            start_widget=MusicTray(),
            center_widget=Workspaces(),
            end_widget=StatusTray(),
        )

        Widget.Window(
            namespace="StatusBar",
            child=centerBox,
            anchor=["left", "top", "right"],
            exclusivity="exclusive",
            layer="top",
            kb_mode="none",
        )

        app.apply_css(os.path.expanduser("~/.config/ignis/StatusBar/style.scss"))
