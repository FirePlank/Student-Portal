from kivy.lang import Builder
import os
import sys
if getattr(sys, 'frozen', False):
	from app.screens.mainmenu import MainMenu
	from app.screens.wikipedia import Wikipedia
else:
	from screens.mainmenu import MainMenu
	from screens.wikipedia import Wikipedia

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Builder.load_file(resource_path(os.path.join('screens', 'mainmenu', 'mainmenu.kv')))
Builder.load_file(resource_path(os.path.join('screens', 'wikipedia', 'wikipedia.kv')))
