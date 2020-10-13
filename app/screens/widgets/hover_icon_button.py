from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivy.properties import NumericProperty
from kivy.lang import Builder


class HoverIconButton(MDIconButton, ThemableBehavior, HoverBehavior):

    canvas_opacity = NumericProperty(0)

    def on_enter(self, *args):
        self.canvas_opacity = 1

    def on_leave(self, *args):
        self.canvas_opacity = 0


kv = """

#:import Window kivy.core.window.Window

<HoverIconButton>:
    ripple_scale: 0
    canvas.before:
        Color:
            id: line_color
            rgba: .5, .7, .5, root.canvas_opacity
        Line:
            width: 2
            rectangle: self.x-dp((Window.height/720)*2), self.y-dp((Window.height/720)*2), self.width+dp((Window.height/720)*4), self.height+dp((Window.height/720)*4)

"""

Builder.load_string(kv)