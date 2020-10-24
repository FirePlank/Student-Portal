import os
import sys

from kivy.config import Config
Config.set('graphics', 'width', 1280)
Config.set('graphics', 'height', 720)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

import kivy
kivy.require('2.0.0')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.resources import resource_add_path
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.core.window import Window
from kivy import utils
from kivy.clock import Clock
Window.minimum_width, Window.minimum_height = (720, 480)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    return os.path.join(base_path, relative_path)

resource_add_path(resource_path(os.path.join('data', 'logo')))
resource_add_path(resource_path(os.path.join('data', 'fonts')))
resource_add_path(resource_path(os.path.join('data', 'database')))
resource_add_path(resource_path(os.path.join('screens', 'wikipedia')))
resource_add_path(resource_path(os.path.join('screens', 'mainmenu')))
resource_add_path(resource_path(os.path.join('screens', 'notebook')))
resource_add_path(resource_path(os.path.join('screens', 'translation')))
resource_add_path(resource_path(os.path.join('screens', 'youtube')))
resource_add_path(resource_path(os.path.join('screens', 'todo')))
resource_add_path(resource_path(os.path.join('screens', 'books')))


class StudentPortal(MDApp):

    title = "Student Portal"
    color_theme = 'normal'
    bg_color = ListProperty([71/255, 93/255, 102/255, 1])
    tile_color = ListProperty([133/255, 144/255, 149/255, 1])
    raised_button_color = ListProperty([144/255, 159/255, 165/255, 1])
    text_color = ListProperty([0, 0, 0, 1])
    title_text_color = ListProperty([1, 1, 1, 1])
    accent_color = ListProperty([0.5, 0.7, 0.5, 1])
    app_font = StringProperty(resource_path(os.path.join('data', 'fonts', 'Code2000', 'CODE2000.ttf')))
    cursor_width = NumericProperty(3)

    def build(self):
        if getattr(sys, 'frozen', False):
            from app.screens import mainmenu, wikipedia, notebook, translation, youtube, todo, books
        else:
            from screens import mainmenu, wikipedia, notebook, translation, youtube, todo, books

        self.root = ScreenManager()
        self.mainmenu = mainmenu.MainMenu()
        self.wikipedia = wikipedia.Wikipedia()
        self.notebook = notebook.Notebook()
        self.translation = translation.Translation()
        self.youtube = youtube.Youtube()
        self.todo = todo.ToDo()
        self.books = books.Books()
        self.screens = {
            'mainmenu': self.mainmenu,
            'wikipedia': self.wikipedia,
            'notebook': self.notebook,
            'translation': self.translation,
            'youtube': self.youtube,
            'todo': self.todo,
            'books': self.books
        }
        self.root.switch_to(self.mainmenu)
        self.unlock_dark_mode()
        return self.root

    def switch_screen(self, screen_name, direction='left'):
        self.root.transition.direction = direction
        self.root.switch_to(self.screens.get(screen_name))

    def unlock_dark_mode(self):
        self.color_theme = 'dark'
        try:
            self.party_update.cancel()
        except:
            pass
        self.bg_color = [29/255, 29/255, 29/255, 1]
        self.tile_color = [40/255, 40/255, 40/255, 1]
        self.raised_button_color = [52/255, 52/255, 52/255, 1]
        self.text_color = [1, 1, 1, 1]
        self.title_text_color = [1, 1, 1, 1]
        self.accent_color = [0.5, 0.7, 0.5, 1]

    def color_theme_normal(self):
        self.color_theme = 'normal'
        try:
            self.party_update.cancel()
        except:
            pass
        self.bg_color = [71/255, 93/255, 102/255, 1]
        self.tile_color = [133/255, 144/255, 149/255, 1]
        self.raised_button_color = [144/255, 159/255, 165/255, 1]
        self.title_text_color = [1, 1, 1, 1]
        self.accent_color = [0.5, 0.7, 0.5, 1]

    def color_theme_party(self):
        self.color_theme = 'party'
        try:
            self.party_update.cancel()
        except:
            pass
        def update_colors(self):
            self.bg_color = list(utils.get_random_color(alpha=0.6))
            self.tile_color = list(utils.get_random_color(alpha=0.6))
            self.raised_button_color = list(utils.get_random_color(alpha=0.6))
            self.text_color = list(utils.get_random_color(alpha=0.6))
            self.title_text_color = list(utils.get_random_color(alpha=0.6))
            self.accent_color = list(utils.get_random_color(alpha=0.6))
        self.party_update = Clock.schedule_interval(lambda dt, a=self: update_colors(a), 0.2)


if __name__ == '__main__':
    StudentPortal().run()
