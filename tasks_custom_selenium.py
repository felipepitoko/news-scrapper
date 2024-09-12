from robocorp.tasks import task
from custom_selenium import CustomSelenium
from robocorp import workitems
import logging

@task
def minimal_task():
    logger = logging.getLogger(__name__)

    for item in workitems.inputs:
        try:
            workdata = item.payload
            logger.info("Processing item with data: %s", workdata)
            selenium = CustomSelenium()
            selenium.set_webdriver()
            selenium.open_url(workdata['access_link'], workdata['img_filename'])
            selenium.driver_quit()
            logger.info("End of processing item with data: %s", workdata)
        except Exception as e:
            logger.error("Error processing item with data %s: %s", item.payload, e)
            raise