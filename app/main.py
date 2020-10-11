from kivy.config import Config
Config.set('graphics','width',1280)
Config.set('graphics','height',720)

import os
import sys
import json

from kivy.resources import resource_add_path
from tools import resource_path
resource_add_path(resource_path(os.path.join('data', 'logo')))

from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from screens import MainMenu, Wikipedia
import random

class StudentPortal(MDApp):
    title = "Student Portal"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.root = ScreenManager()
        self.mainmenu = MainMenu()
        self.wikipedia = Wikipedia()
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

    class Wikipedia:
        def __init__(self, keyword):
            self.S = requests.Session()

            self.URL = "https://en.wikipedia.org/w/api.php"

            self.PARAMS = {
                "action": "query",
                "generator": "search",
                "gsrsearch": keyword,
                "prop": "extracts|pageimages",
                "exintro": 1,
                "format": "json"
            }

            self.R = self.S.get(url=self.URL, params=self.PARAMS)
            self.DATA = self.R.json()

        def titles(self):
            titles = []
            for i in self.DATA["query"]["pages"]:
                titles.append(self.DATA["query"]["pages"][i]["title"])
            return titles

        def first_paragraphs(self):
            paragraphs = []
            for i in self.DATA["query"]["pages"]:
                paragraphs.append(self.DATA["query"]["pages"][i]["extract"])
            return paragraphs

        def photos(self):
            pictures = []
            for i in self.DATA["query"]["pages"]:
                try:
                    pictures.append(self.DATA["query"]["pages"][i]["thumbnail"]["source"])
                except:
                    pictures.append(None)
            return pictures


if __name__ == '__main__':
	StudentPortal().run()
