from robocorp.tasks import task
from robocorp import workitems
from robocorp.workitems import Input
from robocorp.workitems import Output
from rpa_news_latimes import RpaNewsLatimes

@task
def minimal_task():
    rpa = RpaNewsLatimes()
    rpa.set_webdriver()
    rpa.open_url("https://www.latimes.com/", "latimes.png")
    rpa.search_content(search_phrase=input['search_phrase'])
    rpa.sort_news_results(topic_sort_key=input['topic_sort_key'])
    
    rpa.get_news(max_months=input['months'])    

    rpa.driver_quit()