from ignis.widgets import Widget
from ignis.services.system_tray import SystemTrayService


class Tray(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        systemTray = SystemTrayService.get_default()
