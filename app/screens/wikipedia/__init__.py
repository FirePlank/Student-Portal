from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from kivymd.app import MDApp

class Wikipedia(MDScreen):
    def search(self, query):
        if query.strip() == "":
            toast('What to search? xD', duration=1)
        else:
            self.ids.results.text = MDApp.get_running_app().search_wikipedia(query.strip())
