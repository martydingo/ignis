from ignis.widgets import Widget


class Tray(Widget.Box):
    def __init__(self, **kwargs):
        super.__init__(**kwargs)

    self.label(label="Hello")
