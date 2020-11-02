from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from ..widgets.hover_icon_button import HoverIconButton
import requests
from kivymd.app import MDApp
from ..modules import sql_operator
from datetime import datetime
from kivy.lang import Builder
import threading
from kivy.clock import mainthread


OPERATOR = sql_operator()
create_table_query = """
    CREATE TABLE IF NOT EXISTS wikipedia_history(
        unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
        search_word TEXT NOT NULL,
        search_date TEXT NOT NULL
    );
"""


class Wikipedia(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        OPERATOR.execute_query(create_table_query)

    def search(self, query):
        if query.strip() != '':
            self.ids.results.text = 'Searching...'
            self.thread = threading.Thread(
                target=self.search_thread, args=(query,))
            self.thread.daemon = True
            self.thread.start()
        else:
            show_toast("There's nothing to search...", duration=1)

    def search_thread(self, query):
        wikipedia = WikipediaBackend(query)
        summary = wikipedia.summary()
        self.show_result(summary)

    @mainthread
    def show_result(self, summary):
        self.ids.results.text = summary
        self.ids.search_button.disabled = False
        self.ids.search_button.canvas.get_group(
            'hidden')[0].rgba = (0, 0, 0, 0)


class WikipediaBackend():
    def __init__(self, keyword):
        self.keyword = keyword
        if self.keyword.lower() == "fireplank":
            title = "FirePlank (AKA The Best Programmer)"
            self.DATA = {
                'title': title,
                'extract': """FirePlank is the creator for the backend of this module and also the most genius programmer I know!
\nYou should totally check out
His twitter: https://twitter.com/FirePlank
His github: https://github.com/FirePlank
His discord server: https://discord.gg/K2Cf6ma
and his fiverr: https://www.fiverr.com/fireplank"""}
        elif self.keyword.lower() == "saykat":
            title = "Saykat"
            self.DATA = {
                'title': title,
                'extract': "Saykat is an intresting guy and a good friend... and that's about it :shrug:"}

        elif self.keyword.lower() == "krymzin":
            title = "KrYmZiN"
            self.DATA = {'title': title, 'extract':
                         """Krymzin's a skilled programmer in both frontend and backend. He made all the frontend for this entire app and it be looking kinda sexy if you ask me.
\nHis fiverr: https://fiverr.com/krymzin"""}
        else:
            self.DATE = datetime.now().strftime('%c')
            self.S = requests.Session()

            self.URL = "https://en.wikipedia.org/w/api.php"

            self.PARAMS = {
                "action": "query",
                "titles": self.keyword,
                "prop": "extracts|info",
                "inprop": "url",
                "redirects": 1,
                "format": "json",
                "exintro": 1,
                "explaintext": True
            }

            OPERATOR.execute_query(create_table_query)

            try:
                self.R = self.S.get(url=self.URL, params=self.PARAMS)
                self.DATA = self.R.json()["query"]["pages"]
                self.DATA = self.DATA[[i for i in self.DATA][0]]

                add_keyword_query = f"""
                INSERT INTO
                    wikipedia_history(search_word, search_date)
                VALUES
                    ("{self.keyword.replace('"', "'")}", '{self.DATE}')
                """

                check_status = "SELECT wikipedia_history from settings_data"
                check_status = OPERATOR.execute_read_query(check_status)[0][0]
                if check_status == 1:
                    OPERATOR.execute_query(add_keyword_query)

            except Exception as e:
                self.DATA = None

    def summary(self):
        if self.DATA is not None:
            try:
                title = self.DATA["title"]
                summary = self.DATA["extract"]
                references = []

                if "may refer to" in summary[-16:]:
                    params = {
                        'action': 'query',
                        'list': 'search',
                        'srsearch': self.keyword.title(),
                        'format': 'json'
                    }

                    data = requests.get(self.URL, params=params).json()
                    data = data['query']['search']

                    for search in data:
                        references.append(search['title'])

                summary += '\n\n' + '\n'.join(references)

                return f"{' '*(56-round(len(title)/2))}{title}\n\n" + \
                    summary[:2000] + ('...' if len(summary) > 2000 else '')

            except Exception as e:
                return "Sorry, couldn't fetch any search result for that."

        else:
            toast('Could not connect to the internet/slow connection', duration=1)
            return ''


Builder.load_file('wikipedia.kv')
