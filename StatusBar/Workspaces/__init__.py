from ignis.widgets import Widget
from ignis.services.hyprland import HyprlandService
from ignis.variable import Variable

from .WorkspaceIcons import WorkspaceIcons

import json


class Workspaces(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.hyprland = HyprlandService.get_default()

        self.workspaceButtons = Variable({})

        self.handleWorkspaceUpdate()

        self.hyprland.connect("notify", lambda x, y: self.handleWorkspaceUpdate())

    def handleWorkspaceUpdate(self):
        self.updateWorkspaceButtons()
        self.updateWorkspaceButtonLabels()

        workspaceChildren = []
        for workspaceId, workspaceButton in sorted(self.workspaceButtons.value.items()):
            workspaceChildren.append(workspaceButton)
        self.child = workspaceChildren

    def updateWorkspaceButtons(self):
        for workspace in self.hyprland.workspaces:
            self.workspaceButtons.value.update({workspace["id"]: Widget.Button()})

        for workspaceId, workspaceButton in self.workspaceButtons.value.items():
            match = False
            for workspace in self.hyprland.workspaces:
                if workspaceId == workspace["id"]:
                    match = True
            if match == False:
                self.workspaceButtons.value[workspaceId] = {}

    def updateWorkspaceButtonLabels(self):
        for workspaceId, workspaceButton in self.workspaceButtons.value.items():
            if type(workspaceButton) == dict:
                pass
            else:
                labelBox = Widget.Box(spacing=4)
                labelBoxChildren = [Widget.Label(label=f"{workspaceId} |")]
                currentClients = json.loads(self.hyprland.send_command("j/clients"))
                for client in currentClients:
                    if client["workspace"]["id"] == workspaceId:
                        if WorkspaceIcons[client["class"]]:
                            labelBoxChildren.append(
                                Widget.Label(
                                    label=WorkspaceIcons[client["class"]] + " "
                                )
                            )
                        else:
                            labelBoxChildren.append(Widget.Label(label=client["class"]))
                labelBox.child = labelBoxChildren
                workspaceButton.child = labelBox
