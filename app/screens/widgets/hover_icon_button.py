from kivymd.uix.button import MDIconButton
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder


class HoverIconButton(MDIconButton):

    canvas_opacity = NumericProperty(0)
    tooltip_text = StringProperty('')

    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(MDIconButton, self).__init__(**kwargs)
        self.tooltip = ToolTip(text=self.tooltip_text)

    def on_mouse_pos(self, *args):
        self.close_tooltip()
        if not self.get_root_window():
            return
        pos = args[1]
        self.tooltip.pos = pos
        self.canvas_opacity = 0
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            self.schedule = Clock.schedule_once(self.display_tooltip, 0.5)
            self.canvas_opacity = 1 if not self.disabled else 0

    def close_tooltip(self, *args):
        try:
            self.schedule.cancel()
        except BaseException:
            pass
        try:
            Window.remove_widget(self.tooltip)
        except BaseException:
            pass

    def display_tooltip(self, *args):
        self.tooltip.text = self.tooltip_text
        Window.add_widget(self.tooltip)

    def on_press(self):
        self.close_tooltip()

    def on_release(self):
        self.close_tooltip()


class ToolTip(Label):
    pass


kv = """
<ToolTip>:
    color: app.text_color
    font_name: app.app_font
    font_size: str(min(Window.height/720*22, Window.width/720*22)) + 'sp'
    size_hint: None, None
    size: self.texture_size[0]+20, self.texture_size[1]+20
    canvas.before:
        Color:
            rgba: app.raised_button_color
        Rectangle:
            size: self.size
            pos: self.pos
    canvas.after:
        Color:
            id: line_color
            rgba: app.text_color
        Line:
            width: 1
            rectangle: self.x-dp((Window.height/720)*1), self.y-dp((Window.height/720)*1), self.width+dp((Window.height/720)*2), self.height+dp((Window.height/720)*2)


<HoverIconButton>:
    ripple_scale: 0
    canvas.before:
        Color:
            id: line_color
            rgba: app.accent_color[:-1]+[root.canvas_opacity]
        Line:
            width: 2
            rectangle: self.x-dp((Window.height/720)*2), self.y-dp((Window.height/720)*2), self.width+dp((Window.height/720)*4), self.height+dp((Window.height/720)*4)
"""

Builder.load_string(kv)
