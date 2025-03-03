from ignis.widgets import Widget
from .StatusTray import StatusTray
from .Workspaces import Workspaces


class StatusBar:
    def __init__(self):
        centerBox = Widget.CenterBox(
            vertical=False,
            start_widget=Widget.Label(label="start"),
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
