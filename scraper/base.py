import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

logger = logging.getLogger(__name__)


class WebScraper:
    """
    A class for web scraping using Selenium and a headless browser.

    :param browser: The name of the browser to use. Currently, only "chrome" and "firefox" are supported.
    :type browser: str
    :param headless: Whether to run the browser in headless mode.
    :type headless: bool
    :param parser: The parser to use for BeautifulSoup. Defaults to "html.parser".
    :type parser: str
    """

    def __init__(
        self,
        browser: str = 'chrome',
            headless: bool = True,
            parser: str = 'html.parser'
    ) -> None:
        if browser == 'chrome':
            self.chrome_init(headless=headless)
        elif browser == 'firefox':
            self.firefox_init(headless=headless)
        else:
            logger.error(f'Invalid browser: {browser}')
            raise ValueError(f'Invalid browser: {browser}')

        self.parser = parser

    def chrome_init(self, headless=True):
        try:
            self.options = ChromeOptions()
            self.options.headless = headless
            self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(),
                options=self.options
            )
        except Exception as e:
            logger.error(f'Error initializing Chrome: {e}')
            raise e

    def firefox_init(self, headless=True):
        try:
            self.options = FirefoxOptions()
            self.options.headless = headless
            self.driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install(),
                options=self.options
            )
        except Exception as e:
            logger.error(f'Error initializing Firefox: {e}')
            raise e

    def get(self, url: str) -> None:
        """
        Get a URL.

        :param url: The URL to get.
        :type url: str
        """
        try:
            self.driver.get(url)
        except Exception as e:
            logger.error(f'Error getting URL: {e}')
            raise e

    def soup(self) -> BeautifulSoup:
        """
        Scrape the page and return a BeautifulSoup object.

        :return: A BeautifulSoup object.
        :rtype: BeautifulSoup
        """
        try:
            return BeautifulSoup(self.driver.page_source, self.parser)
        except Exception as e:
            logger.error(f'Error beautifying page source: {e}')
            raise e

    def __del__(self):
        """Quit the driver."""
        try:
            self.driver.quit()
        except Exception as e:
            logger.error(f'Error quitting driver: {e}')
            raise e
