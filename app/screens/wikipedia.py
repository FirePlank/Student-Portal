from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from kivymd.app import MDApp
import requests


class Wikipedia:
    def __init__(self, keyword):
        self.S = requests.Session()

        self.URL = "https://en.wikipedia.org/w/api.php"

        self.PARAMS = {
            "action": "query",
            "generator": "search",
            "gsrsearch": keyword,
            "prop": "extracts",
            "exintro": 1,
            "format": "json"
        }

        self.R = self.S.get(url=self.URL, params=self.PARAMS)
        self.DATA = self.R.json()

    def titles(self):
        titles = []
        for i in self.DATA["query"]["pages"]:
            titles.append(self.DATA["query"]["pages"][i]["title"])
        return titles

    def first_paragraphs(self):
        paragraphs = []
        for i in self.DATA["query"]["pages"]:
            paragraphs.append(self.DATA["query"]["pages"][i]["extract"])
        return paragraphs

    def urls(self):
        urls = []
        for i in self.DATA["query"]["pages"]:
            urls.append(f'https://en.wikipedia.org/wiki/{self.DATA["query"]["pages"][i]["title"].replace(" ", "_")}')
        return urls

    def all(self):
        all=[]
        for i in self.DATA["query"]["pages"]:
            all.append([self.DATA["query"]["pages"][i]["title"], f'https://en.wikipedia.org/wiki/{self.DATA["query"]["pages"][i]["title"].replace(" ", "_")}', self.DATA["query"]["pages"][i]["extract"]])

class Wikipedia_Main(MDScreen):
    def search(self, query):
        if query.strip() == "":
            toast('What do you want to search?', duration=1)
        else:
            self.ids.results.text = Wikipedia(query.strip()).all()
