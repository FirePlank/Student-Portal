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
from kivy.animation import Animation
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
resource_add_path(resource_path(os.path.join('screens', 'settings')))
resource_add_path(resource_path(os.path.join('screens', 'about')))


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
            from app.screens import mainmenu, wikipedia, notebook, translation, youtube, todo, books, settings, about
        else:
            from screens import mainmenu, wikipedia, notebook, translation, youtube, todo, books, settings, about

        self.root = ScreenManager()
        self.mainmenu = mainmenu.MainMenu()
        self.wikipedia = wikipedia.Wikipedia()
        self.notebook = notebook.Notebook()
        self.translation = translation.Translation()
        self.youtube = youtube.Youtube()
        self.todo = todo.ToDo()
        self.books = books.Books()
        self.settings = settings.Settings()
        self.about = about.About()
        self.screens = {
            'mainmenu': self.mainmenu,
            'wikipedia': self.wikipedia,
            'notebook': self.notebook,
            'translation': self.translation,
            'youtube': self.youtube,
            'todo': self.todo,
            'books': self.books,
            'settings': self.settings,
            'about': self.about
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
            Animation.cancel_all(self)
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
            Animation.cancel_all(self)
        except:
            pass
        self.bg_color = [71/255, 93/255, 102/255, 1]
        self.tile_color = [133/255, 144/255, 149/255, 1]
        self.raised_button_color = [144/255, 159/255, 165/255, 1]
        self.title_text_color = [1, 1, 1, 1]
        self.accent_color = [0.5, 0.7, 0.5, 1]

    def color_theme_party(self):
        self.color_theme = 'party'
        self.bg_color = list(utils.get_random_color())
        self.tile_color = list(utils.get_random_color())
        self.raised_button_color = list(utils.get_random_color())
        self.text_color = list(utils.get_random_color())
        self.title_text_color = list(utils.get_random_color())
        self.accent_color = list(utils.get_random_color())
        def update_bg_anim(self):
            self.bg_color_animation = Animation(bg_color=utils.get_random_color(), duration=4.)
            self.bg_color_animation.bind(on_complete=lambda idk, a=self: update_bg_anim(a))
            self.bg_color_animation.start(self)
        update_bg_anim(self)
        def update_tile_anim(self):
            self.tile_color_animation = Animation(tile_color=utils.get_random_color(), duration=4.)
            self.tile_color_animation.bind(on_complete=lambda idk, a=self: update_tile_anim(a))
            self.tile_color_animation.start(self)
        update_tile_anim(self)
        def update_raised_button_anim(self):
            self.raised_button_color_animation = Animation(raised_button_color=utils.get_random_color(), duration=4.)
            self.raised_button_color_animation.bind(on_complete=lambda idk, a=self: update_raised_button_anim(a))
            self.raised_button_color_animation.start(self)
        update_raised_button_anim(self)
        def update_text_anim(self):
            self.text_color_animation = Animation(text_color=utils.get_random_color(), duration=4.)
            self.text_color_animation.bind(on_complete=lambda idk, a=self: update_text_anim(a))
            self.text_color_animation.start(self)
        update_text_anim(self)
        def update_title_text_anim(self):
            self.title_text_color_animation = Animation(title_text_color=utils.get_random_color(), duration=4.)
            self.title_text_color_animation.bind(on_complete=lambda idk, a=self: update_title_text_anim(a))
            self.title_text_color_animation.start(self)
        update_title_text_anim(self)
        def update_accent_anim(self):
            self.accent_color_animation = Animation(accent_color=utils.get_random_color(), duration=4.)
            self.accent_color_animation.bind(on_complete=lambda idk, a=self: update_accent_anim(a))
            self.accent_color_animation.start(self)
        update_accent_anim(self)


if __name__ == '__main__':
    StudentPortal().run()
