from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivy.properties import NumericProperty, StringProperty
from ..widgets.hover_icon_button import HoverIconButton
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock


class MainMenu(MDScreen):
    pass


class CustomIconButton(HoverIconButton):
    pass


Builder.load_file('mainmenu.kv')
