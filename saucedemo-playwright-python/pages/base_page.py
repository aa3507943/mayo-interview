from playwright.sync_api import Page, Response
import logging

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    def navigate(self, path: str = ""):
        url = f"https://www.saucedemo.com{path}"
        self.logger.info(f"Navigating to {url}")
        return self.page.goto(url)

    def wait_for_url(self, pattern: str):
        self.page.wait_for_url(pattern)

    def get_title(self) -> str:
        return self.page.title()

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def click(self, selector: str):
        self.logger.info(f"Clicking element: {selector}")
        self.page.click(selector)

    def fill(self, selector: str, text: str):
        self.logger.info(f"Filling element: {selector} with text: {text}")
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)
