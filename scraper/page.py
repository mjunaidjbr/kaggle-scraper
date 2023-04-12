from .base import WebScraper


class Page:

    def __init__(self, url: str, scraper: WebScraper) -> None:
        self.url = url
        self.scraper = scraper
