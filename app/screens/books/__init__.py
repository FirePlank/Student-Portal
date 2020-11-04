import requests
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
import webbrowser
from ..modules import sql_operator, show_toast
from ..widgets.hover_icon_button import HoverIconButton
from ..widgets.hover_flat_button import HoverFlatButton
from ..widgets.custom_scroll import CustomScroll
from ..widgets.searching_text import SearchingText
from datetime import datetime
from kivy.lang import Builder
import threading
from kivy.clock import mainthread
from kivymd.toast import toast


create_table_query = """
    CREATE TABLE IF NOT EXISTS books_history(
        unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
        search_word TEXT NOT NULL,
        search_date TEXT NOT NULL
    );
"""


class Books(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.backend = BooksBackend()
        self.results = None
        self.OPERATOR = sql_operator()
        self.OPERATOR.execute_query(create_table_query)

    @mainthread
    def add_book_widgets(self):
        if self.results:
            self.ids.scroll_box.remove_widget(self.searching_text)
            for result in self.results:
                result_widget = BookCard()
                result_widget.ids.cover.source = str(result[2])
                result_widget.ids.book_name.text = str(result[0])
                result_widget.ids.author_name.text = str(result[1])
                result_widget.ids.book_summary.text = '...'
                result_widget.description = str(result[4])
                result_widget.ids.book_price.text = str(result[5])
                result_widget.link = str(result[3])
                self.ids.scroll_box.add_widget(result_widget)
        else:
            self.searching_text.text = "No results"
        self.ids.scroller.scroll_y = 1
        self.ids.search_button.disabled = False
        self.ids.search_button.canvas.get_group(
            'hidden')[0].rgba = (0, 0, 0, 0)

    def search(self, query):
        if query != '':
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
    def no_internet(self):
        self.ids.scroll_box.remove_widget(self.searching_text)

    def search_thread(self, query):
        self.DATE = datetime.now().strftime("%c")
        self.results = None
        self.results = self.backend.scrape_all(query.strip())

        if self.results is None:
            self.no_internet()
            return

        self.OPERATOR.execute_query(create_table_query)

        add_keyword_query = f"""
        INSERT INTO
            books_history(search_word, search_date)
        VALUES
            ('{query}', '{self.DATE}')
        """

        check_status = "SELECT books_history from settings_data"
        check_status = self.OPERATOR.execute_read_query(check_status)[0][0]
        if check_status == 1:
            self.OPERATOR.execute_query(add_keyword_query)
        self.add_book_widgets()

    def open_in_browser(self, result_widget):
        try:
            webbrowser.open(result_widget.link)
        except:
            toast("Couldn't find any browser.", duration=1)

    def description(self, instance):
        if instance.ids.book_summary.text == "...":
            instance.ids.book_summary.text = instance.description
        else:
            instance.ids.book_summary.text = "..."


class BookCard(MDGridLayout):
    pass


class BooksBackend():

    def scrape_all(self, text):
        try:
            page = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q={text}").json()
            if page["totalItems"] == 0:
                show_toast("No results found.", duration=1)
                return False
            titles = []
            authors = []
            descriptions = []
            book_covers = []
            links = []
            prices = []
            items = page["items"][:31]
            for i in items:
                try:
                    titles.append(i["volumeInfo"]["title"])
                except BaseException:
                    titles.append("Could not find")
                try:
                    authors.append(i["volumeInfo"]["authors"][0])
                except BaseException:
                    authors.append('Could not find')
                try:
                    links.append(i["volumeInfo"]["infoLink"])
                except BaseException:
                    links.append("https://bit.ly/2EqoBMo")
                try:
                    descriptions.append(i["volumeInfo"]["description"])
                except BaseException:
                    descriptions.append("NONE")
                try:
                    book_covers.append(
                        i["volumeInfo"]["imageLinks"]["thumbnail"])
                except BaseException:
                    book_covers.append(
                        "https://www.archgard.com/assets/upload_fallbacks/image_not_found-54bf2d65c203b1e48fea1951497d4f689907afe3037d02a02dcde5775746765c.png")
                try:
                    prices.append(
                        f'{i["saleInfo"]["listPrice"]["amount"]} {i["saleInfo"]["listPrice"]["currencyCode"]}')
                except BaseException:
                    prices.append("Not Listed")

            return [[titles[i], authors[i], book_covers[i], links[i],
                     descriptions[i], prices[i]] for i in range(0, len(items))]
        except Exception as e:
            show_toast(
                'An Error occurred.\nEither you have exhausted daily book searches, or you are not connected to the internet.',
                duration=3)
            return None


Builder.load_file('books.kv')
