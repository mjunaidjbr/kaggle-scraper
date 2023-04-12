import logging
from .base import WebScraper
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class PageScraper:
    """
    A class for representing a web page.

    :param url: The URL of the page.
    :type url: str
    :param scraper: The WebScraper object to use for scraping.
    :type scraper: WebScraper
    """

    def __init__(self, url: str, scraper: WebScraper) -> None:
        self.url = url
        self.scraper = scraper

        try:
            self.scraper.get(url)
            self.soup: BeautifulSoup = self.scraper.soup()
        except Exception as e:
            logger.error(f'Error getting page: {e}')
            raise e

    def fetch_urls(self, selector: str) -> list:
        """
        Fetch URLs from the page.

        :param selector: The CSS selector to use for finding the URLs.
        :type selector: str
        :return: A list of URLs.
        :rtype: list
        """
        try:
            urls = self.soup.select(selector)
            return [url.get('href') for url in urls]
        except Exception as e:
            logger.error(f'Error fetching URLs: {e}')
            raise e

    def __repr__(self) -> str:
        return f'Page(url={self.url})'
