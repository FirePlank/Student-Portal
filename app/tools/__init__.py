from os.path import dirname, join
from kivy.lang import Builder
import sys

def load_kv(filepath, file):
    ''' 
    load a kivy file from the current
    directory of the file calling this func
    where filepath is __file__ and file is a kv file
    ''' 
    filepath = dirname(filepath)
    Builder.load_file(join(filepath, file))

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")

    return join(base_path, relative_path)
