import re
from robocorp.tasks import task
from robocorp import workitems
from robocorp.workitems import Input
from robot_rpa import RobotRpa

@task
def minimal_task():
    selenium = RobotRpa()
    selenium.set_webdriver()
    selenium.open_url("https://github.com/robocorp/rpaframework", "github.png")
    print("Done.")