import sys
import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ["KIVY_NO_CONSOLELOG"] = '1'


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    return os.path.join(base_path, relative_path)


from kivy.config import Config

Config.set('graphics', 'window_state', 'hidden')
Config.set('graphics', 'width', 1280)
Config.set('graphics', 'height', 720)
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('kivy', 'window_icon', os.path.abspath(resource_path('icon.ico')))
Config.set('kivy', 'exit_on_escape', '0')

from kivy.core.window import Window
from kivy.clock import Clock
from kivy import utils
from kivy.animation import Animation
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager, SlideTransition, WipeTransition, FadeTransition, FallOutTransition, NoTransition
from kivymd.app import MDApp

Window.minimum_width, Window.minimum_height = (720, 480)

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
    icon = 'icon.ico'
    use_kivy_settings = False
    color_theme = 'dark'
    bg_color = ListProperty([29 / 255, 29 / 255, 29 / 255, 1])
    tile_color = ListProperty([40 / 255, 40 / 255, 40 / 255, 1])
    raised_button_color = ListProperty([52 / 255, 52 / 255, 52 / 255, 1])
    text_color = ListProperty([1, 1, 1, 1])
    title_text_color = ListProperty([1, 1, 1, 1])
    accent_color = ListProperty([0.5, 0.7, 0.5, 1])
    app_font = StringProperty(
        resource_path(
            os.path.join(
                'data',
                'fonts',
                'Code2000',
                'CODE2000.ttf')))
    cursor_width = NumericProperty(3)
    home_icon = StringProperty('home')
    home_icon_tooltip = StringProperty('Back')
    add_icon = StringProperty('plus-circle-outline')
    add_icon_tooltip = StringProperty('Create new')
    search_icon = StringProperty('magnify')
    search_icon_tooltip = StringProperty('Search')

    def open_settings(self, *largs):
        self.mainmenu.ids.settings_button.trigger_action()

    def build(self):
        self.themes = {
            'dark': self.color_theme_dark,
            'light': self.color_theme_light,
            'rgb': self.color_theme_rgb,
            'custom': None
        }

        self.transitions = {
            'slide': SlideTransition,
            'wipe': WipeTransition,
            'fade': FadeTransition,
            'fall out': FallOutTransition,
            'none': NoTransition
        }

        if getattr(sys, 'frozen', False):
            from app.screens import mainmenu, wikipedia, notebook, translation, youtube, todo, books, settings, about
        else:
            from screens import mainmenu, wikipedia, notebook, translation, youtube, todo, books, settings, about

        self.user_settings = settings.SettingsBackend().show_settings()

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
        self.themes['custom'] = self.settings.color_theme_custom
        self.root.switch_to(self.mainmenu)
        try:
            self.root.transition = self.transitions.get(
                self.user_settings.get('page_transition'))()
        except BaseException:
            self.root.transition = SlideTransition()
        self.themes.get(self.user_settings.get('theme'))()

        Window.show()

        return self.root

    def switch_screen(self, screen_name, direction='left'):
        self.root.transition.direction = direction
        self.root.switch_to(self.screens.get(screen_name))

    def color_theme_dark(self):
        self.color_theme = 'dark'
        try:
            Animation.cancel_all(self)
        except BaseException:
            pass
        self.bg_color = [29 / 255, 29 / 255, 29 / 255, 1]
        self.tile_color = [40 / 255, 40 / 255, 40 / 255, 1]
        self.raised_button_color = [52 / 255, 52 / 255, 52 / 255, 1]
        self.text_color = [1, 1, 1, 1]
        self.title_text_color = [1, 1, 1, 1]
        self.accent_color = [0.5, 0.7, 0.5, 1]

    def color_theme_light(self):
        self.color_theme = 'light'
        try:
            Animation.cancel_all(self)
        except BaseException:
            pass
        self.bg_color = [0.989, 0.989, 0.989, 1.0]
        self.tile_color = [0.94, 0.94, 0.94, 1.0]
        self.raised_button_color = [0.823, 0.823, 0.823, 1.0]
        self.text_color = [0.0, 0.0, 0.0, 1.0]
        self.title_text_color = [0.0, 0.0, 0.0, 1.0]
        self.accent_color = [0.212, 0.099, 1.0, 1.0]

    def color_theme_rgb(self):
        self.color_theme = 'rgb'

        def update_bg_anim(self):
            self.bg_color_animation = Animation(
                bg_color=utils.get_random_color(), duration=4.)
            self.bg_color_animation.bind(
                on_complete=lambda idk,
                a=self: update_bg_anim(a))
            self.bg_color_animation.start(self)
        update_bg_anim(self)

        def update_tile_anim(self):
            self.tile_color_animation = Animation(
                tile_color=utils.get_random_color(), duration=4.)
            self.tile_color_animation.bind(
                on_complete=lambda idk, a=self: update_tile_anim(a))
            self.tile_color_animation.start(self)
        update_tile_anim(self)

        def update_raised_button_anim(self):
            self.raised_button_color_animation = Animation(
                raised_button_color=utils.get_random_color(), duration=4.)
            self.raised_button_color_animation.bind(
                on_complete=lambda idk, a=self: update_raised_button_anim(a))
            self.raised_button_color_animation.start(self)
        update_raised_button_anim(self)

        def update_text_anim(self):
            self.text_color_animation = Animation(
                text_color=utils.get_random_color(), duration=4.)
            self.text_color_animation.bind(
                on_complete=lambda idk, a=self: update_text_anim(a))
            self.text_color_animation.start(self)
        update_text_anim(self)

        def update_title_text_anim(self):
            self.title_text_color_animation = Animation(
                title_text_color=utils.get_random_color(), duration=4.)
            self.title_text_color_animation.bind(
                on_complete=lambda idk, a=self: update_title_text_anim(a))
            self.title_text_color_animation.start(self)
        update_title_text_anim(self)

        def update_accent_anim(self):
            self.accent_color_animation = Animation(
                accent_color=utils.get_random_color(), duration=4.)
            self.accent_color_animation.bind(
                on_complete=lambda idk, a=self: update_accent_anim(a))
            self.accent_color_animation.start(self)
        update_accent_anim(self)

    def color_theme_custom(self, user_settings):
        self.color_theme = 'custom'
        try:
            Animation.cancel_all(self)
        except BaseException:
            pass
        self.bg_color = user_settings.get('bg_color') if len(
            user_settings.get('bg_color')) == 4 else [
            29 / 255, 29 / 255, 29 / 255, 1]
        self.tile_color = user_settings.get('tile_color') if len(
            user_settings.get('tile_color')) == 4 else [
            40 / 255, 40 / 255, 40 / 255, 1]
        self.raised_button_color = user_settings.get('raised_button_color') if len(
            user_settings.get('raised_button_color')) == 4 else [
            52 / 255, 52 / 255, 52 / 255, 1]
        self.text_color = user_settings.get('text_color') if len(
            user_settings.get('text_color')) == 4 else [1, 1, 1, 1]
        self.title_text_color = user_settings.get('title_text_color') if len(
            user_settings.get('title_text_color')) == 4 else [1, 1, 1, 1]
        self.accent_color = user_settings.get('accent_color') if len(
            user_settings.get('accent_color')) == 4 else [0.5, 0.7, 0.5, 1]

    def transition_changed(self, user_settings):
        try:
            self.root.transition = self.transitions.get(
                user_settings.get('page_transition'))()
        except BaseException:
            self.root.transition = SlideTransition()


if __name__ == '__main__':
    StudentPortal().run()
