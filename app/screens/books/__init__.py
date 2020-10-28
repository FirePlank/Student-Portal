import requests
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
import webbrowser
from ..modules import sql_operator
from ..widgets.hover_icon_button import HoverIconButton
from ..widgets.hover_flat_button import HoverFlatButton
from datetime import datetime
from kivymd.toast import toast
from kivy.lang import Builder
from ..widgets.custom_scroll import CustomScroll


class Books(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.backend = BooksBackend()

    def search(self, query):
        self.OPERATOR = sql_operator()
        self.DATE = datetime.now().strftime("%c")
        self.ids.scroll_box.clear_widgets()
        self.results = self.backend.scrape_all(query.strip())
        if self.results:
            for result in self.results:
                result_widget = BookCard()
                result_widget.ids.cover.source = str(result[2])
                result_widget.ids.book_name.text = str(result[0])
                result_widget.ids.author_name.text = str(result[1])
                result_widget.link = str(result[3])
                self.ids.scroll_box.add_widget(result_widget)

        create_table_query = """
        CREATE TABLE IF NOT EXISTS books_history(
            unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_word TEXT NOT NULL,
            search_date TEXT NOT NULL
        );
        """

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

    def open_in_browser(self, result_widget):
        webbrowser.open(result_widget.link)


class BookCard(MDCard):
    pass


class BooksBackend():

    def scrape_all(self, text):
        try:
            page = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={text}").json()
            if page["totalItems"]==0:
                toast("No results found.", duration=1.25)
                return
            titles = []
            authors = []
            descriptions = []
            book_covers = []
            links = []
            prices = []
            for i in page["items"][:11]:
                titles.append(i["volumeInfo"]["title"])
                authors.append(i["volumeInfo"]["authors"][0])
                links.append(i["volumeInfo"]["infoLink"])
                try:descriptions.append(i["volumeInfo"]["description"])
                except:descriptions.append("NONE")
                try:book_covers.append(i["volumeInfo"]["imageLinks"]["thumbnail"])
                except:book_covers.append("https://www.archgard.com/assets/upload_fallbacks/image_not_found-54bf2d65c203b1e48fea1951497d4f689907afe3037d02a02dcde5775746765c.png")
                try:prices.append(f'{i["saleInfo"]["listPrice"]["amount"]} {i["saleInfo"]["listPrice"]["currencyCode"]}')
                except:prices.append("NOT FOR SALE")

            return [[titles[i], authors[i], book_covers[i], links[i], descriptions[i], prices[i]] for i in range (0,10)]
        except Exception as e:
            print(e)
            toast('An Error occured.\n' + f'Error: {str(e)}'.center(min(len(f'Error: {str(e)}'), len('An Error occured.'))), duration=3)


Builder.load_file('books.kv')
