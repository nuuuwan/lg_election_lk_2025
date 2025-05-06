import time

from selenium import webdriver
from utils import Log

log = Log("WebPage")


class WebPage:
    def wait(self, t: int) -> None:
        log.debug(f"😴 {t}s")
        time.sleep(t)

    @staticmethod
    def get_options() -> webdriver.ChromeOptions:
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        return options

    def __init__(self, url: str):
        self.url = url
        self.driver = webdriver.Firefox(options=WebPage.get_options())

    def open(self):
        self.driver.get(self.url)
        self.wait(5)
        log.debug(f"🌏 {self.url}")
        return self.driver

    def close(self) -> None:
        self.driver.quit()
