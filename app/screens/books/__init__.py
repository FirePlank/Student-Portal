import requests
from bs4 import BeautifulSoup as bs
import re


class BooksBackend:
    def __init__(self, text):
        self.text = text

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext.replace("\n", "")

    def scrape_all(self):
        page = requests.get(f"https://www.goodreads.com/search?utf8=%E2%9C%93&query={self.text}")
        soup = bs(page.content, 'html.parser')

        soup_call_title = soup.find_all('a', class_='bookTitle')[:11]
        links = [f"https://www.goodreads.com{i['href']}"for i in soup_call_title]
        titles = [BooksBackend.cleanhtml(self, str(i))for i in soup_call_title]
        authors = [BooksBackend.cleanhtml(self, str(i))for i in soup.find_all('a', class_='authorName')][:11]
        book_covers = [i["src"]for i in soup.find_all(class_='bookCover')][:11]

        return [[titles[i], authors[i], book_covers[i], links[i]] for i in range(0,11)]