import logging

from robocorp.tasks import task
from robocorp import workitems
from rpa_news_latimes_robocorp import RpaNewsLatimesRobocorp

from helper_functions import *
@task
def minimal_task():
    logger = logging.getLogger(__name__)

    try:
        check_output_directory()
        
        for item in workitems.inputs:
            logger.info(f"Started working on workitem.")
            workdata = item.payload
            rpa = RpaNewsLatimesRobocorp()
            rpa.set_webdriver()
            rpa.open_url("https://www.latimes.com/")
            rpa.search_content(search_phrase=workdata['search_phrase'])            
            rpa.sort_news_results(topic_sort_key=workdata['topic_sort_key'])       

            rpa.get_news(max_months=workdata['months_to_search'])    

            rpa.driver_quit()
            news_list = rpa.export_retrieved_news()
            save_dict_to_xlsx(news_list, 'output/news_list.xlsx')
            logger.info(f"Ended process to workdata: {workdata}")
    except Exception as e:
        logger.error(f"Error on task execution: {e}")
        raise e