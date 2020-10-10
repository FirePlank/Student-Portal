from app.tools import load_kv

import os
from kivy.resources import resource_add_path
resource_add_path(os.path.dirname(os.path.realpath(__file__)))

from .mainmenu import MainMenu

load_kv(__file__, os.path.join('kv', 'mainmenu.kv'))
