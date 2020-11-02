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
from kivy.clock import Clock
import json
from kivymd.toast import toast


class Settings(MDScreen):
    def __init__(self, **kwargs):
        super(MDScreen, self).__init__(**kwargs)

        self.backend = SettingsBackend()

        self.theme = DropDown(
            bar_width=10,
            scroll_type=[
                'bars',
                'content'],
            effect_cls='ScrollEffect',
            smooth_scroll_end=10)
        self.theme.bar_inactive_color = self.theme.bar_color
        self.theme.bind(on_select=lambda instance, x: self.theme_changed(x))

        self.mainbutton_theme = HoverFlatButton(
            text=f"{self.backend.show_settings().get('theme').title()} ↓",
            size_hint=(
                0.6,
                1))
        self.mainbutton_theme.bind(on_release=self.theme.open)
        self.ids.theme.add_widget(self.mainbutton_theme)

        for theme in list(MDApp.get_running_app().themes):
            btn = HoverFlatButton(
                text=theme.title(),
                size_hint_y=None,
                height=self.mainbutton_theme.height)
            btn.bind(on_release=lambda btn: self.theme.select(btn.text))
            self.theme.add_widget(btn)

        self.transition = DropDown(
            bar_width=10,
            scroll_type=[
                'bars',
                'content'],
            effect_cls='ScrollEffect',
            smooth_scroll_end=10)
        self.transition.bar_inactive_color = self.transition.bar_color
        self.transition.bind(
            on_select=lambda instance,
            x: self.transition_changed(x))

        self.mainbutton_transition = HoverFlatButton(
            text=f"{self.backend.show_settings().get('page_transition').title()} ↓",
            size_hint=(
                0.6,
                1))
        self.ids.transition.add_widget(self.mainbutton_transition)
        self.mainbutton_transition.bind(on_release=self.transition.open)

        for transition in list(MDApp.get_running_app().transitions):
            btn = HoverFlatButton(
                text=transition.title(),
                size_hint_y=None,
                height=self.mainbutton_transition.height)
            btn.bind(on_release=lambda btn: self.transition.select(btn.text))
            self.transition.add_widget(btn)

        self.choose_color = ChooseColors()

        if MDApp.get_running_app().color_theme == 'custom':
            self.ids.appearance_settings.add_widget(self.choose_color)
        else:
            pass

        def get_status(self, setting):
            if self.backend.show_settings().get(setting):
                self.ids[setting].history_status = 1
            else:
                self.ids[setting].history_status = 0

        get_status(self, 'wikipedia_history')
        get_status(self, 'youtube_history')
        get_status(self, 'books_history')

    def theme_changed(self, theme):
        try:
            self.ids.appearance_settings.remove_widget(self.choose_color)
            self.ids.scroller.scroll_y = 1
        except BaseException:
            pass
        setattr(self.mainbutton_theme, 'text', theme.title() + ' ↓')
        self.backend.edit_settings('theme', theme.lower())
        MDApp.get_running_app().themes.get(theme.lower())()

    def transition_changed(self, transition):
        setattr(self.mainbutton_transition, 'text', transition.title() + ' ↓')
        self.backend.edit_settings('page_transition', transition.lower())
        user_settings = self.backend.show_settings()
        MDApp.get_running_app().transition_changed(user_settings)

    def color_theme_custom(self):
        self.ids.appearance_settings.add_widget(self.choose_color, index=1)
        user_settings = self.backend.show_settings()
        MDApp.get_running_app().color_theme_custom(user_settings)

    def edit_color(self, component, initial_color):
        self.popup = PopupColorPicker(
            component, size_hint=(
                None, None), auto_dismiss=False)
        self.popup.open()

    def display_settings(self):
        self.ids.wikipedia_history.history = self.backend.show_history(
            'wikipedia_history')
        self.ids.youtube_history.history = self.backend.show_history(
            'youtube_history')
        self.ids.books_history.history = self.backend.show_history(
            'books_history')
        def change(self):
            self.ids.history_box.current = self.ids.history_box.next()
        try:
            self.switch1.cancel()
            self.switch2.cancel()
            self.switch3.cancel()
        except BaseException:
            pass
        self.switch1 = Clock.schedule_once(lambda dt: change(self), 0.1)
        self.switch2 = Clock.schedule_once(lambda dt: change(self), 0.2)
        # Had to do this weird hack cause the height was not being adjusted
        # properly
        self.switch3 = Clock.schedule_once(lambda dt: change(self), 0.3)

    def on_leave(self):
        self.ids.history_box.current = self.ids.wikipedia_history_screen.name

    def delete_history(self, table):
        self.backend.delete_history(f'{table.lower()}_history')
        self.display_settings()

    def history_status(self, component):
        setting = f'{component.history_component.lower()}_history'
        if self.backend.show_settings().get(setting):
            self.backend.edit_settings(setting, 0)
            component.history_status = 0
        else:
            self.backend.edit_settings(setting, 1)
            component.history_status = 1


class ChooseColors(GridLayout):
    pass


class ColorField():
    pass


class PopupColorPicker(Popup):
    components = {
        'Bg color': 'bg_color',
        'Tile color': 'tile_color',
        'Button color': 'raised_button_color',
        'Tile text color': 'text_color',
        'Bg text color': 'title_text_color',
        'Accent color': 'accent_color'
    }

    def __init__(self, component, **kwargs):
        super().__init__()
        self.title = 'Pick color'
        self.backend = SettingsBackend()
        self.color_editing = self.components.get(component)
        self.ids.picker.color = (1, 1, 1, 1)

    def save_color(self):
        if self.color_editing == 'bg_color' and self.ids.picker.color[3] < 1:
            toast('Bg color opacity cannot be less than 1', duration=1)
        else:
            self.backend.edit_settings(self.color_editing, self.ids.picker.color)
            MDApp.get_running_app().settings.theme_changed('custom')


class HistoryView(GridLayout):
    pass


class SettingsBackend:
    create_settings_table = """
    CREATE TABLE IF NOT EXISTS settings_data(
        bg_color TEXT NOT NULL,
        tile_color TEXT NOT NULL,
        raised_button_color TEXT NOT NULL,
        text_color TEXT NOT NULL,
        title_text_color TEXT NOT NULL,
        accent_color TEXT NOT NULL,
        theme TEXT NOT NULL,
        page_transition TEXT NOT NULL,
        wikipedia_history INTEGER NOT NULL,
        youtube_history INTEGER NOT NULL,
        books_history INTEGER NOT NULL
    )
    """
    default_value = """
    INSERT INTO
        settings_data(bg_color, tile_color, raised_button_color, text_color, title_text_color, accent_color, theme, page_transition, wikipedia_history, youtube_history, books_history)
    VALUES
        ('[29/255, 29/255, 29/255, 1]', '[40/255, 40/255, 40/255, 1]', '[52/255, 52/255, 52/255, 1]', '[1, 1, 1, 1]', '[1, 1, 1, 1]', '[0.5, 0.7, 0.5, 1]', "dark", "slide", '1', '1', '1')
    """

    delete_table = "DROP TABLE IF EXISTS settings_data"

    show_table_date = "SELECT * FROM settings_data"

    OPERATOR = sql_operator()

    def show_settings(self):
        self.OPERATOR.execute_query(self.create_settings_table)
        self.OPERATOR.execute_query(self.default_value)
        data = self.OPERATOR.execute_read_query(self.show_table_date)[0]

        try:
            output_data = {
                "bg_color": string_to_list(data[0]),
                "tile_color": string_to_list(data[1]),
                "raised_button_color": string_to_list(data[2]),
                "text_color": string_to_list(data[3]),
                "title_text_color": string_to_list(data[4]),
                "accent_color": string_to_list(data[5]),
                "theme": data[6],
                "page_transition": data[7],
                "wikipedia_history": data[8],
                "youtube_history": data[9],
                "books_history": data[10]
            }
        except BaseException:
            self.OPERATOR.execute_query(self.delete_table)
            return self.show_settings()

        if output_data.get('theme') in MDApp.get_running_app().themes:
            pass
        else:
            self.edit_settings('theme', 'dark')
            self.show_settings()

        if output_data.get(
                'page_transition') in MDApp.get_running_app().transitions:
            pass
        else:
            self.edit_settings('page_transition', 'slide')
            self.show_settings()

        return output_data

    def edit_settings(self, key, value):
        update_query = f"""
        UPDATE
            settings_data
        SET
            {key} = '{value}'
        """

        self.OPERATOR.execute_query(update_query)

    def show_history(self, table):
        query = f"SELECT * FROM {table}"
        history = self.OPERATOR.execute_read_query(query)
        history = [
            f'{i[1]} -- {i[2]}' for i in reversed(history)] if history else 'Nothing in here...'
        return '\n\n'.join(
            str(x) for x in history) if history != 'Nothing in here...' else history

    def delete_history(self, table):
        query = f"DROP TABLE IF EXISTS {table}"
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table}(
                unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_word TEXT NOT NULL,
                search_date TEXT NOT NULL
            );
        """
        self.OPERATOR.execute_query(query)
        self.OPERATOR.execute_query(create_table_query)


Builder.load_file('settings.kv')
