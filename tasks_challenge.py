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
            search_phrase = workdata.get('search_phrase', '')
            topic_sort_key = workdata.get('topic_sort_key', None)
            months_to_search = workdata.get('months_to_search', 1)
            order_by = workdata.get('order_by', 'relevance')

            rpa = RpaNewsLatimesRobocorp()
            rpa.set_webdriver()
            rpa.open_url("https://www.latimes.com/")
            rpa.search_content(search_phrase=search_phrase)            
            rpa.sort_news_results(topic_sort_key=topic_sort_key,order_by=order_by)       

            rpa.get_news(max_months=months_to_search)    

            rpa.driver_quit()
            news_list = rpa.export_retrieved_news()
            save_dict_to_xlsx(news_list, 'output/news_list.xlsx')
            logger.info(f"Ended process to workdata: {workdata}")
    except Exception as e:
        logger.error(f"Error on task execution: {e}")
        raise e
    

{
    "search_phrase": "israeli war",
    "months_to_search": 3
}