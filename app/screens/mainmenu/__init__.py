from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivy.properties import NumericProperty
from ..widgets.hover_icon_button import HoverIconButton
from kivy.lang import Builder


class MainMenu(MDScreen):
    pass


class CustomIconButton(HoverIconButton):
    pass


Builder.load_file('mainmenu.kv')
