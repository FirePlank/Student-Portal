from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from kivymd.app import MDApp
from ..widgets.hover_icon_button import HoverIconButton
import requests


class Wikipedia(MDScreen):
    def search(self, query):
        if query.strip() == "":
            toast('Please input a search query.', duration=1)
        else:
            self.ids.results.text = MDApp.get_running_app().search_wikipedia(query.strip())


class WikipediaBackend():

    def __init__(self, keyword):
        self.keyword = keyword
        self.S = requests.Session()

        self.URL = "https://en.wikipedia.org/w/api.php"

        self.PARAMS = {
            "action": "query",
            "titles": keyword,
            "prop": "extracts|info",
            "inprop": "url",
            "redirects": 1,
            "format": "json",
            "exintro": 1,
            "explaintext": True
        }
        try:
            self.R = self.S.get(url=self.URL, params=self.PARAMS)
            self.DATA = self.R.json()["query"]["pages"]
            self.DATA = self.DATA[[i for i in self.DATA][0]]
        except:
            self.DATA=None

    def title(self):
        return self.DATA["title"]

    def first_paragraph(self):
        return self.DATA["extract"]

    def summary(self):
        if self.DATA is not None:
            try:
                title=self.DATA["title"]
                url=self.DATA["fullurl"]
                summary=self.DATA["extract"]
                return title + '\n\n' + summary[:2000] + ('...' if len(summary) > 2000 else '')
            except:
                return "Sorry, couldn't fetch any search result for that."
        else:
            toast('Not Connected to the internet.', duration=1)
            return 'Please check your internet connection.'
