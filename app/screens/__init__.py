from tools import resource_path
from kivy.lang import Builder
import os

from screens.mainmenu import MainMenu
from screens.wikipedia import Wikipedia

Builder.load_file(resource_path(os.path.join('screens', 'mainmenu', 'mainmenu.kv')))
Builder.load_file(resource_path(os.path.join('screens', 'wikipedia', 'wikipedia.kv')))
