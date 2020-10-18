from youtubesearchpython import SearchVideos
import json
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.properties import NumericProperty
from kivymd.toast import toast
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivy.uix.button import Button
import webbrowser


class Youtube(MDScreen):
    def search(self, query):
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
    def open_in_browser(self, result_widget):
        webbrowser.open(result_widget.link)


class ResultCard(MDCard):
    pass


class OpenButton(Button, ThemableBehavior, HoverBehavior):
    canvas_opacity = NumericProperty(0)

    def on_enter(self, *args):
        self.canvas_opacity = 1

    def on_leave(self, *args):
        self.canvas_opacity = 0
