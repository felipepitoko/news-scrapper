from robocorp.tasks import task
from robocorp import workitems
from robocorp.workitems import Input
from robocorp.workitems import Output
from rpa_news import RpaNews

@task
def minimal_task():
    selenium = RpaNews()
    selenium.set_webdriver()
    selenium.open_url("https://www.google.com/", "google.png")
    selenium.driver_quit()
    # workitems.outputs.create(payload={"file_saida": "google.png"},files=["google.png", "google.png"],save=True)
    print("Done.")