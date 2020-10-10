from kivy.config import Config
Config.set('graphics','width',1280)
Config.set('graphics','height',720)

import os
import sys
import json

from kivy.resources import resource_add_path
from app.tools import resource_path
resource_add_path(resource_path(os.path.join('data', 'logo')))

from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from app.screens import MainMenu

class StudentPortal(MDApp):
    title = "Student Portal"
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.root = ScreenManager()
        self.mainmenu = MainMenu()
        self.root.switch_to(self.mainmenu)
        return self.root


if __name__ == '__main__':
	StudentPortal().run()
