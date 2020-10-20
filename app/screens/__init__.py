from kivy.lang import Builder
import os
import sys

if getattr(sys, 'frozen', False):
	from app.screens.mainmenu import MainMenu
	from app.screens.wikipedia import Wikipedia
	from app.screens.notebook import Notebook
	from app.screens.translation import Translation
	from app.screens.youtube import Youtube
	from app.screens.todo import ToDo
	from app.screens.modules import resource_path
else:
	from screens.mainmenu import MainMenu
	from screens.wikipedia import Wikipedia
	from screens.notebook import Notebook
	from screens.translation import Translation
	from screens.youtube import Youtube
	from screens.todo import ToDo
	from screens.modules import resource_path

Builder.load_file(resource_path(os.path.join('screens', 'mainmenu', 'mainmenu.kv')))
Builder.load_file(resource_path(os.path.join('screens', 'wikipedia', 'wikipedia.kv')))
Builder.load_file(resource_path(os.path.join('screens', 'notebook', 'notebook.kv')))
Builder.load_file(resource_path(os.path.join('screens', 'translation', 'translation.kv')))
Builder.load_file(resource_path(os.path.join('screens', 'youtube', 'youtube.kv')))
Builder.load_file(resource_path(os.path.join('screens', 'todo', 'todo.kv')))
