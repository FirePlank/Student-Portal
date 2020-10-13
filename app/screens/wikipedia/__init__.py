from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from kivymd.app import MDApp
import requests


class Wikipedia(MDScreen):
    def search(self, query):
        if query.strip() == "":
            toast('Please input a search query.', duration=1)
        else:
            self.ids.results.text = MDApp.get_running_app().search_wikipedia(query.strip())


class WikipediaBackend():
    def __init__(self, keyword):
        self.S = requests.Session()

        self.URL = "https://en.wikipedia.org/w/api.php"

        self.PARAMS = {
            "action": "query",
            "generator": "search",
            "gsrsearch": keyword,
            "prop": "extracts",
            "exintro": 1,
            "format": "json",
            "explaintext": True
        }

        try:
            self.R = self.S.get(url=self.URL, params=self.PARAMS)
            self.DATA = self.R.json()
        except Exception:
            self.DATA = None

    def summary(self):
        if self.DATA != None:
            try:
                data = self.DATA["query"]["pages"]
                for page in data:
                    if data[page]["index"] == 1:
                        title = data[page]["title"]
                        summary = data[page]["extract"]
                        break
                return title + '\n\n' + summary[:2000] + ('...' if len(summary) > 2000 else '')

            except:
                return "Sorry, couldn't fetch any search result for that."
        else:
            toast('Not Connected to the internet.', duration=1)
            return ''

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
