from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivy.properties import NumericProperty

class MainMenu(MDScreen):
    pass

class CustomIconButton(MDIconButton, ThemableBehavior, HoverBehavior):
    '''Custom item implementing hover behavior.'''
    canvas_opacity = NumericProperty(0, rebind=True)

    def on_enter(self, *args):
        '''The method will be called when the mouse cursor
        is within the borders of the current widget.'''

        self.canvas_opacity = 1

    def on_leave(self, *args):
        '''The method will be called when the mouse cursor goes beyond
        the borders of the current widget.'''

        self.canvas_opacity = 0
