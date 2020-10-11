from app.tools import resource_path
from kivy.lang import Builder
import os

from .mainmenu import MainMenu
from .wikipedia import Wikipedia

Builder.load_file(resource_path(os.path.join('screens', 'kv', 'mainmenu.kv')))
Builder.load_file(resource_path(os.path.join('screens', 'kv', 'wikipedia.kv')))
