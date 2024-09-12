from robocorp.tasks import task
from robocorp import workitems
from robocorp.workitems import Input
from robocorp.workitems import Output
from rpa_news_latimes_robocorp import RpaNewsLatimesRobocorp
import logging

from helper_functions import *
# {
#   "search_phrase": "fire in california"
# }
@task
def minimal_task():
    logger = logging.getLogger(__name__)

    try:
        for item in workitems.inputs:
            workdata = item.payload
            rpa = RpaNewsLatimesRobocorp()
            rpa.set_webdriver()
            rpa.open_url("https://www.latimes.com/")
            rpa.search_content(search_phrase=workdata['search_phrase'])
            
            rpa.sort_news_results(topic_sort_key=workdata['topic_sort_key'])
            
            # rpa.get_news(max_months=input['months'])    

            # rpa.driver_quit()
            # news_list = rpa.export_retrieved_news()
            # save_dict_to_xlsx(news_list, 'output/news_list.xlsx')
            logger.info(f"Ended process to workdata: {workdata}")
    except Exception as e:
        logger.error(f"Error on task execution: {e}")
        raise e