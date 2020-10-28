from kivymd.uix.screen import MDScreen
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.properties import NumericProperty
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivy.lang import Builder
from ..modules import sql_operator, string_to_list
from ..widgets.custom_scroll import CustomScroll
from ..widgets.hover_flat_button import HoverFlatButton
from ..widgets.hover_icon_button import HoverIconButton
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window


class Settings(MDScreen):
    def __init__(self, **kwargs):
        super(MDScreen, self).__init__(**kwargs)

        self.backend = SettingsBackend()

        self.theme = DropDown(bar_width=10, scroll_type=['bars', 'content'], effect_cls='ScrollEffect', smooth_scroll_end=10)
        self.theme.bar_inactive_color = self.theme.bar_color
        self.theme.bind(on_select=lambda instance, x: self.theme_changed(x))

        self.mainbutton_theme = DropDownButton(text=f"{self.backend.show_settings().get('theme').title()} ↓", size_hint=(0.6, 1))
        self.mainbutton_theme.bind(on_release=self.theme.open)
        self.ids.theme.add_widget(self.mainbutton_theme)

        for theme in list(MDApp.get_running_app().themes):
            btn = DropDownButton(text=theme.title(), size_hint_y=None, height=self.mainbutton_theme.height)
            btn.bind(on_release=lambda btn: self.theme.select(btn.text))
            self.theme.add_widget(btn)

        self.transition = DropDown(bar_width=10, scroll_type=['bars', 'content'], effect_cls='ScrollEffect', smooth_scroll_end=10)
        self.transition.bar_inactive_color = self.transition.bar_color
        self.transition.bind(on_select=lambda instance, x: self.transition_changed(x))

        self.mainbutton_transition = DropDownButton(text=f"{self.backend.show_settings().get('page_transition').title()} ↓", size_hint=(0.6, 1))
        self.ids.transition.add_widget(self.mainbutton_transition)
        self.mainbutton_transition.bind(on_release=self.transition.open)

        for transition in list(MDApp.get_running_app().transitions):
            btn = DropDownButton(text=transition.title(), size_hint_y=None, height=self.mainbutton_transition.height)
            btn.bind(on_release=lambda btn: self.transition.select(btn.text))
            self.transition.add_widget(btn)

        self.choose_color = ChooseColors()

        if MDApp.get_running_app().color_theme == 'custom':
            self.ids.appearance_settings.add_widget(self.choose_color)
        else:
            pass
        
    def theme_changed(self, theme):
        try:
            self.ids.appearance_settings.remove_widget(self.choose_color)
            self.ids.scroller.scroll_y = 1
        except:
            pass
        setattr(self.mainbutton_theme, 'text', theme.title()+' ↓')
        self.backend.edit_settings('theme', theme.lower())
        MDApp.get_running_app().themes.get(theme.lower())()

    def transition_changed(self, transition):
        setattr(self.mainbutton_transition, 'text', transition.title()+' ↓')
        self.backend.edit_settings('page_transition', transition.lower())
        MDApp.get_running_app().root.transition = MDApp.get_running_app().transitions.get(transition.lower())()

    def color_theme_custom(self):
        self.ids.appearance_settings.add_widget(self.choose_color, index=1)
        user_settings = self.backend.show_settings()
        MDApp.get_running_app().color_theme_custom(user_settings)

    def edit_color(self, component, initial_color):
        self.popup = PopupColorPicker(component, size_hint=(None, None), auto_dismiss=False)
        self.popup.open()


class DropDownButton(Button, ThemableBehavior, HoverBehavior):
    canvas_opacity = NumericProperty(0)

    def on_enter(self, *args):
        self.canvas_opacity = 1

    def on_leave(self, *args):
        self.canvas_opacity = 0


class ChooseColors(GridLayout):
    pass


class ColorField():
    pass


class PopupColorPicker(Popup):
    components = {
        'Background color:': 'bg_color',
        'Tile color:': 'tile_color',
        'Button background color:': 'raised_button_color',
        'Tile text color:': 'text_color',
        'Background text color:': 'title_text_color',
        'Accent color:': 'accent_color'
    }

    def __init__(self, component, **kwargs):
        super().__init__()
        self.title = 'Pick color'
        self.backend = SettingsBackend()
        self.color_editing = self.components.get(component)
        self.ids.picker.color = (1, 1, 1, 1)

    def save_color(self):
        self.backend.edit_settings(self.color_editing, self.ids.picker.color)
        MDApp.get_running_app().settings.theme_changed('custom')


class SettingsBackend:
    def __init__(self):
        self.OPERATOR = sql_operator()
        create_settings_table = """
        CREATE TABLE IF NOT EXISTS settings_data(
            bg_color TEXT NOT NULL,
            tile_color TEXT NOT NULL,
            raised_button_color TEXT NOT NULL,
            text_color TEXT NOT NULL,
            title_text_color TEXT NOT NULL,
            accent_color TEXT NOT NULL,
            theme TEXT NOT NULL,
            page_transition TEXT NOT NULL
        )
        """
        default_value = """
        INSERT INTO
            settings_data(bg_color, tile_color, raised_button_color, text_color, title_text_color, accent_color, theme, page_transition)
        VALUES
            ("[71/255, 93/255, 102/255, 1]", "[133/255, 144/255, 149/255, 1]", "[144/255, 159/255, 165/255, 1]", "[0, 0, 0, 1]", "[1, 1, 1, 1]", "[0.5, 0.7, 0.5, 1]", "dark", "slide") 
        """

        self.OPERATOR.execute_query(create_settings_table)
        self.OPERATOR.execute_query(default_value)

    def show_settings(self):
        show_table_date = "SELECT * FROM settings_data"
        data = self.OPERATOR.execute_read_query(show_table_date)[0]

        output_data = {
            "bg_color" : string_to_list(data[0]),
            "tile_color" : string_to_list(data[1]),
            "raised_button_color" : string_to_list(data[2]),
            "text_color" : string_to_list(data[3]),
            "title_text_color" : string_to_list(data[4]),
            "accent_color" : string_to_list(data[5]),
            "theme" : data[6],
            "page_transition" : data[7]
        }

        return output_data

    def edit_settings(self, key, value):
        update_query = f"""
        UPDATE
            settings_data
        SET
            {key} = '{value}'
        """

        self.OPERATOR.execute_query(update_query)

    def wikipedia_history(self):
        query = "SELECT * FROM wikipedia_history"
        history = self.OPERATOR.execute_read_query(query)
        history = [i[1] for i in history]
        return history

    def youtube_history(self):
        query = "SELECT * FROM youtube_history"
        history = self.OPERATOR.execute_read_query(query)
        history = [i[1] for i in history]
        return history

    def book_history(self):
        query = "SELECT * FROM books_history"
        history = self.OPERATOR.execute_read_query(query)
        history = [i[1] for i in history]
        return history


Builder.load_file('settings.kv')
