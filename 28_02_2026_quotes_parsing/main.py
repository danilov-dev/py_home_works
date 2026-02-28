import json
from typing import Optional

from bs4 import BeautifulSoup, Tag
import requests

class Author:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
    def to_dict(self):
        return {'name': self.name, 'url': self.url}

class QuoteTag:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
    def to_dict(self):
        return {'name': self.name, 'url': self.url}

class Quote:
    def __init__(self, text: str, author: Author, tags: list):
        self.text = text
        self.author = author
        self.tags = tags

    def to_dict(self):
        return {
            'text': self.text,
            'author': self.author.name if self.author else None,
            'link_author': self.author.url if self.author else None,
            'tags': {tag.name: tag.url for tag in self.tags}
        }

class QuoteScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url.strip()
        self.quotes = []
        self.authors = []
        self.tags = []

    def _fetch_page(self, url:str) -> Optional[str]:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
            }
            page = requests.get(url,headers=headers, timeout=10)
            page.raise_for_status()
            return page.text
        except Exception as e:
            print(f"Error: {e}")
            return None


    def _parse_quote(self, quote_element: Tag) -> Optional[Quote]:
        try:
            text_element = quote_element.find('span', class_='text')

            if text_element is None:
                return None
            text = text_element.text.strip()

            author_element = quote_element.find('small', class_='author')
            author_name = author_element.text.strip() if author_element else "Неизвестный"

            author_link_elem = quote_element.find('a')['href'] if author_element else None
            author_url = self.base_url + author_link_elem.lstrip('/')
            author = Author(name=author_name, url=author_url)


            self.authors.append(author)

            tags = []
            tags_div = quote_element.find('div', class_='tags')
            if tags_div:
                tag_links = tags_div.find_all('a', class_='tag')
                for tag in tag_links:
                    tag_name = tag.text.strip()
                    tage_url_link = self.base_url + tag['href'].lstrip('/')

                    tag = QuoteTag(tag_name, tage_url_link)
                    tags.append(tag)
                    self.tags.append(tag)

            return Quote(text=text, author=author, tags=tags)
        except Exception as e:
            print(f"Parse error: {e}")
            return None

    def scrape_all_pages(self):
        num_page = 1

        while True:
            if num_page == 1:
                url = self.base_url
            else:
                url = f"{self.base_url}page/{num_page}/"

            page = self._fetch_page(url)
            if not page:
                break

            soup = BeautifulSoup(page, 'html.parser')
            quote_elements = soup.find_all('div', class_='quote')

            if not quote_elements:
                break

            for quote_element in quote_elements:
                quote = self._parse_quote(quote_element)
                if quote:
                    self.quotes.append(quote)

            num_page += 1

        return self

    def save_to_json(self, file_name: str):
        quotes_dict = {}
        for i, quote in enumerate(self.quotes,1):
            quotes_dict[str(i)] = quote.to_dict()
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(quotes_dict, f, indent=2, ensure_ascii=False)
            print("Файл записан успешно!")


if __name__ == '__main__':
    scraper = QuoteScraper("https://quotes.toscrape.com/")
    scraper.scrape_all_pages()
    scraper.save_to_json("quotes.json")