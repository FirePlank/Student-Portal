from youtubesearchpython import SearchVideos
import json
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
import webbrowser
from ..modules import sql_operator, show_toast
from ..widgets.hover_icon_button import HoverIconButton
from ..widgets.hover_flat_button import HoverFlatButton
from ..widgets.custom_scroll import CustomScroll
from ..widgets.searching_text import SearchingText
from datetime import datetime
from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
import threading
from kivy.clock import mainthread
from kivy.core.window import Window
from kivymd.toast import toast


create_table_query = """
    CREATE TABLE IF NOT EXISTS youtube_history(
        unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
        search_word TEXT NOT NULL,
        search_date TEXT NOT NULL
    );
"""


class Youtube(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results = None
        self.OPERATOR = sql_operator()
        self.OPERATOR.execute_query(create_table_query)

    def search(self, query):
        self.query = query.strip().lower()
        if query.strip() != '':
            self.ids.scroll_box.clear_widgets()
            self.searching_text = SearchingText()
            self.ids.scroll_box.add_widget(self.searching_text)
            self.thread = threading.Thread(
                target=self.search_thread, args=(query,))
            self.thread.daemon = True
            self.thread.start()
        else:
            show_toast("There's nothing to search...", duration=1)

    @mainthread
    def add_video_widgets(self):
        if self.results:
            self.ids.scroll_box.remove_widget(self.searching_text)
            for result in self.results:
                result_widget = ResultCard()
                result_widget.ids.thumbnail.source = str(
                    result.get('thumbnails')[0])
                result_widget.ids.video_name.text = str(result.get('title'))
                result_widget.ids.channel_name.text = str(
                    result.get('channel'))
                result_widget.ids.video_duration.text = str(
                    result.get('duration'))
                result_widget.ids.video_views.text = str(
                    result.get('views')) + ' views'
                result_widget.link = str(result.get('link'))
                self.ids.scroll_box.add_widget(result_widget)
            if self.query == 'tech with tim':
                self.secret_button = HoverFlatButton(text='Secret Button DO NOT CLICK', size_hint_y=None, height=Window.height/2)
                self.secret_button.bind(on_release=lambda instance: webbrowser.open('https://bit.ly/2EqoBMo'))
                self.ids.scroll_box.add_widget(self.secret_button)
        else:
            self.searching_text.text = "No results"
        self.ids.scroller.scroll_y = 1
        self.ids.search_button.disabled = False
        self.ids.search_button.canvas.get_group(
            'hidden')[0].rgba = (0, 0, 0, 0)

    @mainthread
    def no_internet(self):
        self.ids.scroll_box.remove_widget(self.searching_text)

    def search_thread(self, query):
        self.DATE = datetime.now().strftime("%c")
        self.results = None
        try:
            self.results = json.loads(
                SearchVideos(
                    query.strip(),
                    offset=1,
                    mode="json",
                    max_results=10).result())["search_result"]
        except BaseException:
            show_toast('Could not connect to the internet.', 1)
            self.no_internet()
            return

        self.OPERATOR.execute_query(create_table_query)

        add_keyword_query = f"""
        INSERT INTO
            youtube_history(search_word, search_date)
        VALUES
            ("{query.replace('"', "'")}", '{self.DATE}')
        """

        check_status = "SELECT youtube_history from settings_data"
        check_status = self.OPERATOR.execute_read_query(check_status)[0][0]
        if check_status == 1:
            self.OPERATOR.execute_query(add_keyword_query)
        self.add_video_widgets()

    def open_in_browser(self, result_widget):
        try:
            webbrowser.open(result_widget.link)
        except:
            toast("Can't find any web browser.", duration=1)


class ResultCard(MDGridLayout):
    pass


Builder.load_file('youtube.kv')
