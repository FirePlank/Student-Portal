from kivy.config import Config
Config.set('graphics','width',1280)
Config.set('graphics','height',720)

import os
import sys
import json

from kivy.resources import resource_add_path
from tools import resource_path
resource_add_path(resource_path(os.path.join('data', 'logo')))
resource_add_path(resource_path(os.path.join('data', 'fonts')))

from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from screens import mainmenu, wikipedia
import random

class StudentPortal(MDApp):
    title = "Student Portal"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.root = ScreenManager()
        self.mainmenu = mainmenu.MainMenu()
        self.wikipedia = wikipedia.Wikipedia()
        self.screens = {
            'mainmenu': self.mainmenu,
            'wikipedia': self.wikipedia,
        }
        self.root.switch_to(self.mainmenu)
        return self.root

    def switch_screen(self, screen_name, direction='left'):
        self.root.transition.direction = direction
        self.root.switch_to(self.screens.get(screen_name))

    def search_wikipedia(self, query):
        return(str(random.randint(0,10))) # return result, should be string


if __name__ == '__main__':
	StudentPortal().run()
