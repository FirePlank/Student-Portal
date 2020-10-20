from youtubesearchpython import SearchVideos
import json
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.properties import NumericProperty
import webbrowser
from ..modules import sql_operator
from ..widgets.hover_icon_button import HoverIconButton
from ..widgets.hover_flat_button import HoverFlatButton
from datetime import datetime


class Youtube(MDScreen):
    def search(self, query):
        self.OPERATOR = sql_operator()
        self.DATE = datetime.now().strftime("%c")
        self.ids.scroll_box.clear_widgets()
        self.results = json.loads(SearchVideos(query, offset=1, mode="json", max_results=10).result())["search_result"]
        for result in self.results:
            result_widget = ResultCard()
            result_widget.ids.thumbnail.source = str(result.get('thumbnails')[0])
            result_widget.ids.video_name.text = str(result.get('title'))
            result_widget.ids.channel_name.text = str(result.get('channel'))
            result_widget.ids.video_duration.text = str(result.get('duration'))
            result_widget.ids.video_views.text = str(result.get('views')) + ' views'
            result_widget.link = str(result.get('link'))
            self.ids.scroll_box.add_widget(result_widget)

        create_table_query = """
        CREATE TABLE IF NOT EXISTS youtube_history(
            unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_word TEXT NOT NULL,
            search_date TEXT NOT NULL
        );
        """
        
        self.OPERATOR.execute_query(create_table_query)

        add_keyword_query = f"""
        INSERT INTO
            youtube_history(search_word, search_date)
        VALUES
            ('{query}', '{self.DATE}')
        """

        self.OPERATOR.execute_query(add_keyword_query)
        
    def open_in_browser(self, result_widget):
        webbrowser.open(result_widget.link)


class ResultCard(MDCard):
    pass
