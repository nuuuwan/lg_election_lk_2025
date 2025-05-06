import time

from selenium import webdriver
from utils import Log

log = Log("WebPage")


class WebPage:

    @staticmethod
    def get_options() -> webdriver.ChromeOptions:
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        return options

    @staticmethod
    def open_driver() -> webdriver.Firefox:
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    @staticmethod
    def close_driver(driver: webdriver.Firefox) -> None:
        driver.quit()

    def wait(self, t: int) -> None:
        log.debug(f"😴 {t}s")
        time.sleep(t)

    def __init__(self, url: str, driver: webdriver.Firefox) -> None:
        self.url = url
        self.driver = driver

    def open(self):
        self.driver.get(self.url)
        self.wait(5)
        log.debug(f"🌏 {self.url}")
