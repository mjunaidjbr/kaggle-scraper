from .base import WebScraper
from .page import PageScraper


def run(browser: str = 'chrome', headless: bool = True) -> None:
    """
    Run the scraper.

    :param browser: The browser to use for scraping.
    :type browser: str
    :param headless: Whether to run the browser in headless mode.
    :type headless: bool
    """
    scraper = WebScraper(browser=browser, headless=headless)
    page = PageScraper(
        url='https://www.google.com',
        scraper=scraper
    )
    urls = page.fetch_urls(selector='a')
    print(urls)
