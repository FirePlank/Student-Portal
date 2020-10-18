from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from ..widgets.hover_icon_button import HoverIconButton
import requests
from kivymd.app import MDApp


class Wikipedia(MDScreen):
    def search(self, query):
        if query.strip() == "":
            toast('Please input a search query.', duration=1)
        else:
            wikipedia = WikipediaBackend(query)
            summary = wikipedia.summary()
            self.ids.results.text = summary


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
                return f"{' '*(56-round(len(title)/2))}{title}\n\n" + summary[:2000] + ('...' if len(summary) > 2000 else '')
            except:
                if self.keyword.lower() == "fireplank":
                    title="FirePlank (AKA The Best Programmer)"
                    return f"{' '*(56-round(len(title)/2))}{title}\n\n" + """FirePlank is the creator for the backend of this module and also the most genius programmer I know!
\nYou should totally check out 
his twitter: https://twitter.com/FirePlank
his github: https://github.com/FirePlank
and his discord server: https://discord.gg/K2Cf6ma"""
                elif self.keyword.lower() == "saykat":
                    title="SaykaT"
                    return f"{' '*(56-round(len(title)/2))}{title}\n\n" + "SaykaT is an intresting guy and a good friend... and that's about it :shrug:"
                elif self.keyword.lower() == "krymzin":
                    title="KrYmZiN"
                    return f"{' '*(56-round(len(title)/2))}{title}\n\n" + """I got to be honest with you. I had to copy and paste that name cuz I that name be wild son.
But other than the name he's a skilled programmer in both frontend and backend. He made all the frontend for this entire app and it be looking kinda sexy if you ask me."""
                elif self.keyword.lower() == "unlock_dark_mode":
                    if MDApp.get_running_app().color_theme != 'dark':
                        MDApp.get_running_app().unlock_dark_mode()
                        return "Enjoy dark mode."
                    else:
                        return "You're already in dark mode. try 'normal_theme'."
                elif self.keyword.lower() == "normal_theme":
                    if MDApp.get_running_app().color_theme != 'normal':
                        MDApp.get_running_app().color_theme_normal()
                        return "Normal color theme :)"
                    else:
                        return "The current color theme is already the normal theme. try 'unlock_dark_mode'."

                return "Sorry, couldn't fetch any search result for that."
        else:
            toast('Not Connected to the internet.', duration=1)
            return 'Please check your internet connection.'
