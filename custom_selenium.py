from RPA.core.webdriver import download, start
import logging
from selenium import webdriver
from RPA.Browser.Selenium import Selenium

class CustomSelenium:

    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)

    def set_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-web-security')
        options.add_argument("--start-maximized")
        options.add_argument('--remote-debugging-port=9222')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return options

    def set_webdriver(self, browser="Chrome"):
        browser = Selenium()
        options = self.set_chrome_options()
        browser.open_available_browser(headless=True, options=options,browser_selection='Chrome')        
        
        self.driver = browser

    def open_url(self, url:str, screenshot:str=None):
        self.driver.go_to(url)
        if screenshot:
            self.driver.screenshot(locator=None, filename=f'output/{screenshot}')

    def driver_quit(self):
        if self.driver:
            self.driver.close_browser()

if __name__ == "__main__":
    custom_selenium = CustomSelenium()
    custom_selenium.set_webdriver()
    custom_selenium.open_url("https://www.google.com/", "google.png")
    # custom_selenium.full_page_screenshot("XXXXXXXXXXXXXXXXXXXXXXXX")
    custom_selenium.driver_quit()