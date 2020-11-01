from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.lang import Builder


class HoverFlatButton(Button, ThemableBehavior, HoverBehavior):

    canvas_opacity = NumericProperty(0)

    def on_enter(self, *args):
        self.canvas_opacity = 1 if not self.disabled else 0

    def on_leave(self, *args):
        self.canvas_opacity = 0


kv = """
<HoverFlatButton>:
    ripple_scale: 0
    canvas.after:
        Color:
            id: line_color
            rgba: app.accent_color[:-1]+[root.canvas_opacity]
        Line:
            width: 2
            rectangle: self.x+1, self.y+1, self.width-2, self.height-2
"""

Builder.load_string(kv)
