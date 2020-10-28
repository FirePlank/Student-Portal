import requests
from bs4 import BeautifulSoup as bs
import re
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

        self.OPERATOR.execute_query(add_keyword_query)
        
    def open_in_browser(self, result_widget):
        webbrowser.open(result_widget.link)


class BookCard(MDCard):
    pass


class BooksBackend():
    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext.replace("\n", "")

    def scrape_all(self, text):
        try:
            page = requests.get(f"https://www.goodreads.com/search?utf8=%E2%9C%93&query={text}")
            soup = bs(page.content, 'html.parser')

            soup_call_title = soup.find_all('a', class_='bookTitle')[:10]
            links = [f"https://www.goodreads.com{i['href']}"for i in soup_call_title][:10]
            titles = [BooksBackend.cleanhtml(self, str(i))for i in soup_call_title][:10]
            authors = [BooksBackend.cleanhtml(self, str(i))for i in soup.find_all('a', class_='authorName')][:10]
            book_covers = [i["src"]for i in soup.find_all(class_='bookCover')][:10]
            if len(titles) == 0:
                toast('No results', duration=1.5)
            return [[titles[i], authors[i], book_covers[i], links[i]] for i in range (0, len(titles))]
        except Exception as e:
            print(e)
            toast('An Error occurred. Check your internet connection.\n' + f'Error: {str(e)}'.center(min(len(f'Error: {str(e)}'), len('An Error occurred. Check your internet connection.'))), duration=3)


Builder.load_file('books.kv')
