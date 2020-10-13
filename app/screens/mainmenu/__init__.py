from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivy.properties import NumericProperty


class MainMenu(MDScreen):
    pass


class CustomIconButton(MDIconButton, ThemableBehavior, HoverBehavior):

    canvas_opacity = NumericProperty(0)

    def on_enter(self, *args):
        self.canvas_opacity = 1

    def on_leave(self, *args):
        self.canvas_opacity = 0
