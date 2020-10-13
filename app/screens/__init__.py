from kivy.lang import Builder
import os
import sys
from kivymd.app import MDApp

if getattr(sys, 'frozen', False):
	from app.screens.mainmenu import MainMenu
	from app.screens.wikipedia import Wikipedia
	from app.screens.notebook import Notebook
else:
	from screens.mainmenu import MainMenu
	from screens.wikipedia import Wikipedia
	from screens.notebook import Notebook

resource_path = MDApp.get_running_app().resource_path

Builder.load_file(resource_path(os.path.join('screens', 'mainmenu', 'mainmenu.kv')))
Builder.load_file(resource_path(os.path.join('screens', 'wikipedia', 'wikipedia.kv')))
Builder.load_file(resource_path(os.path.join('screens', 'notebook', 'notebook.kv')))
