from robocorp.tasks import task
from robocorp import workitems
from robocorp.workitems import Input
from robocorp.workitems import Output
from rpa_news_latimes import RpaNewsLatimes

from helper_functions import *

@task
def minimal_task():
    for item in workitems.inputs:
        input = item.payload
        rpa = RpaNewsLatimes()
        rpa.set_webdriver()
        rpa.open_url("https://www.latimes.com/")
        rpa.search_content(search_phrase=input['search_phrase'])
        rpa.sort_news_results(topic_sort_key=input['topic_sort_key'])
        
        rpa.get_news(max_months=input['months'])    

        rpa.driver_quit()
        news_list = rpa.export_retrieved_news()
        save_dict_to_xlsx(news_list, 'output/news_list.xlsx')