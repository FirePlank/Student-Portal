from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from ..widgets.custom_scroll import CustomScroll


class About(MDScreen):
    pass


class AboutCard(MDGridLayout):
    pass


Builder.load_file('about.kv')
