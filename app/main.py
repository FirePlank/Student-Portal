# --- APP ---
from kivy.config import Config
Config.set('graphics','width',1280)
Config.set('graphics','height',720)
from kivy.core.window import Window
Window.clearcolor = (71/255, 93/255, 102/255, 1)
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, WipeTransition

# --- TOOLS ---
import os
import sys
import json
from kivy.resources import resource_add_path


class StudentPortal(MDApp):

    title = "Student Portal"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        if getattr(sys, 'frozen', False):
            from app.screens import mainmenu, wikipedia
        else:
            from screens import mainmenu, wikipedia
        resource_add_path(self.resource_path(os.path.join('data', 'logo')))
        resource_add_path(self.resource_path(os.path.join('data', 'fonts')))
        resource_add_path(self.resource_path(os.path.join('data', 'database')))
        resource_add_path(self.resource_path(os.path.join('screens', 'wikipedia')))
        resource_add_path(self.resource_path(os.path.join('screens', 'mainmenu')))
        self.root = ScreenManager(transition=WipeTransition())
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
        if getattr(sys, 'frozen', False):
            from app.screens import wikipedia
        else:
            from screens import wikipedia
        wiki = wikipedia.WikipediaBackend(query)
        summary = wiki.summary()
        return(summary) # return result, should be string

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    StudentPortal().run()
