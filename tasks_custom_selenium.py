from robocorp.tasks import task
from custom_selenium import CustomSelenium

@task
def minimal_task():
    selenium = CustomSelenium()
    selenium.set_webdriver()
    selenium.open_url("https://www.latimes.com/", "latimes.png")
    selenium.driver_quit()
    print("Done.")