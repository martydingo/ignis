from ignis.widgets import Widget
from ignis.utils import exec_sh_async, FileMonitor, Poll
from ignis.variable import Variable
import os
from gi.repository import Gtk


class MusicLevels(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing = 0
        # self.homogenous = False
        # self.vexpand = True
        # self.hexpand = True
        self.valign = "baseline"
        self.halign = "start"
        # self.style = "background-color: red;"

        self.cavaLevels = Variable([])
        self.cava = exec_sh_async(
            "/nix/store/ziam35zx2b1rg3bq71j6b7agdcg6fpag-home-manager-path/bin/cava -p cava-config"
        )

        self.processCavaOutput()
        self.setupLevelBars()

        Poll(100, lambda x: self.__handleCavaUpdate__())

    def setupLevelBars(self):
        self.levelBars = Variable({})
        index = 0
        for cavaLevel in self.cavaLevels.value:
            self.levelBars.value.update(
                {
                    index: Gtk.LevelBar(
                        width_request=4,
                        height_request=16,
                        max_value=1000,
                        min_value=0,
                        orientation="vertical",
                        inverted=True,
                        # height=1,
                        # content_fit="scale_down",
                    )
                }
            )
            index = index + 1

    def __handleCavaUpdate__(self):
        self.processCavaOutput()
        self.updateLevelBars()

        cavaBars = []
        for cavaBarIndex, cavaBar in self.levelBars.value.items():
            cavaBars.append(cavaBar)
        self.child = cavaBars

    def processCavaOutput(self):
        with open("/tmp/cava-output", mode="r", buffering=-1) as cavaFile:
            self.cavaLevels.value = cavaFile.readline().split(";")[:-1]

    def updateLevelBars(self):
        index = 0
        for cavaLevel in self.cavaLevels.value:
            if cavaLevel != "":
                try:
                    levelHeight = int(cavaLevel)
                    self.levelBars.value[index].set_value(levelHeight)
                    index = index + 1
                except KeyError:
                    pass
