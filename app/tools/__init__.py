from os.path import dirname, join
from kivy.lang import Builder

def load_kv(filepath, file):
    ''' 
    load a kivy file from the current
    directory of the file calling this func
    where filepath is __file__ and file is a kv file
    ''' 
    filepath = dirname(filepath)
    Builder.load_file(join(filepath, file))
