from robocorp.tasks import task
from custom_selenium import CustomSelenium
from robocorp import workitems
import logging

@task
def minimal_task():
    logger = logging.getLogger(__name__)

    for item in workitems.inputs:
        try:
            logger.info("Processing item with data: %s", item.payload)
            selenium = CustomSelenium()
            selenium.set_webdriver()
            selenium.open_url(item['access_link'], item['img_filename'])
            selenium.driver_quit()
            logger.info("Processing item with data: %s", item.payload)
        except Exception as e:
            logger.error("Error processing item with data %s: %s", item.payload, e)
            raise