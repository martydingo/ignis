from ignis.widgets import Widget
from ignis.services.system_tray import SystemTrayService, SystemTrayItem


class Tray(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        systemTray = SystemTrayService.get_default()

        self.trayItemsContainer = Widget.Box()

        systemTray.connect(
            "added", lambda x, trayItem: self.__handleTrayUpdate__(trayItem)
        )

        self.child = [self.trayItemsContainer]

    def __handleTrayUpdate__(self, trayItem):
        trayButton = self.createTrayItem(trayItem)
        self.trayItemsContainer.append(trayButton)

    def createTrayItem(self, trayItem: SystemTrayItem):
        if trayItem.menu:
            trayItemMenu = trayItem.menu
        else:
            trayItemMenu = None

        trayItemIcon = Widget.Icon(image=trayItem.bind("icon"))

        trayItemContainer = Widget.Box(child=[trayItemIcon, trayItemMenu])

        trayItemButton = Widget.Button(
            child=trayItemContainer,
            setup=lambda self: trayItem.connect("removed", lambda x: self.unparent()),
            tooltip_text=trayItem.bind("tooltip"),
            # on_click=lambda x: trayItemMenu.popup() if trayItemMenu else None,
            on_right_click=lambda x: trayItemMenu.popup() if trayItemMenu else None,
            css_classes=["TrayItem"],
        )

        return trayItemButton
