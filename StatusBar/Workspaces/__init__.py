from ignis.widgets import Widget
from ignis.services.hyprland import HyprlandService
from ignis.variable import Variable

from .WorkspaceIcons import WorkspaceIcons

import json


class Workspaces(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Workspaces"
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
            css_classes = ["WorkspaceButton"]
            if self.hyprland.active_workspace["id"] == workspace["id"]:
                css_classes.append("active")
            self.workspaceButtons.value.update(
                {
                    workspace["id"]: Widget.Button(
                        name=f"WorkspaceButton-{str(workspace["id"])}",
                        css_classes=css_classes,
                        on_click=lambda event: self.handleWorkspaceButtonClick(event),
                    )
                }
            )

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
                labelBox = Widget.Box()
                labelBoxChildren = [
                    Widget.Label(
                        css_classes=["WorkspaceButtonLabelID"], label=f"{workspaceId} |"
                    )
                ]
                currentClients = json.loads(self.hyprland.send_command("j/clients"))
                for client in currentClients:
                    if client["workspace"]["id"] == workspaceId:
                        try:
                            labelBoxChildren.append(
                                Widget.Label(
                                    label=WorkspaceIcons[client["class"]] + " "
                                )
                            )
                        except KeyError:
                            labelBoxChildren.append(Widget.Label(label=client["class"]))
                labelBox.child = labelBoxChildren
                workspaceButton.child = labelBox

    def handleWorkspaceButtonClick(self, event):
        callingWorkspaceId = event.name.split("-")[-1]
        self.hyprland.switch_to_workspace(callingWorkspaceId)
