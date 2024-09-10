import re
from robocorp.tasks import task
from robocorp import workitems
from robocorp.workitems import Input
from robot_rpa import RobotRpa

@task
def minimal_task():
    selenium = RobotRpa()
    selenium.set_webdriver()
    selenium.open_url("https://www.google.com/", "google.png")
    selenium.driver_quit()
    print("Done.")