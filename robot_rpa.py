from RPA.core.webdriver import download, start
import logging
from selenium import webdriver
import json, os



class RobotRpa:

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
        options = self.set_chrome_options()
        self.driver = webdriver.Chrome(options=options)

    def open_url(self, url:str, screenshot_name:str=None):
        try:
            self.driver.get(url)
            if screenshot_name:
                self.driver.get_screenshot_as_file(f'output/{screenshot_name}')

                if not os.path.exists('output'):
                    os.makedirs('output')

                data = {
                    "name": "John Doe",
                    "age": 30,
                    "city": "New York"
                }

                filepath = os.path.join('output', "data.json")

                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)

        except Exception as e:
            self.logger.error(f"Error opening URL: {e}")
            raise e

    def driver_quit(self):
        if self.driver:
            self.driver.quit()