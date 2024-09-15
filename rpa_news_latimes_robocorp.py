import json, os, time, logging, random, string , re
from RPA.Browser.Selenium import Selenium
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helper_functions import *


class RpaNewsLatimesRobocorp:

    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        self.search_phrase = None
        self.news_list = []
        
    def set_chrome_options(self):
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")        
        options.add_argument('--disable-web-security')
        options.add_argument("--start-maximized")
        options.add_argument('--remote-debugging-port=9222')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return options

    def set_webdriver(self):
        try:
            browser = Selenium()
            options = self.set_chrome_options()
            browser.open_available_browser(headless=True, options=options,browser_selection='Chrome')        
            
            self.driver = browser
            self.logger.info("WebDriver set up successfully via rpaframework.")
        except Exception as e:
            self.logger.error(f"Error setting up WebDriver: {e}")
            raise e

    def open_url(self, url:str):
        try:
            self.driver.go_to(url)
            self.logger.info(f"Driver opened url {url}")
        except Exception as e:
            self.logger.error(f"Error opening URL: {e}")
            raise e
        
    def search_content(self, search_phrase:str=''):
        try:
            self.search_phrase = search_phrase

            self.driver.click_button("css:button[data-element='search-button']")
            
            self.driver.wait_until_element_is_visible("css:input[data-element='search-form-input']",timeout=5)
            self.driver.input_text("css:input[data-element='search-form-input']",search_phrase)
            
            self.driver.click_element("css:button[data-element='search-submit-button']")

            self.driver.screenshot(locator=None,filename='output/search_results.png')      
            self.logger.info(f"Search for {search_phrase} completed.")      
                
        except Exception as e:
            self.logger.error(f"Error searching content: {e}")
            raise e

    def sort_news_results(self, topic_sort_key:str=None, type_sort_key:str=None):
        try:
            select_list = self.driver.find_element('css:select.select-input')
            self.driver.select_from_list_by_value(select_list, '1')

            self.driver.screenshot(locator=None, filename='output/sorted_newest_results.png')            

            self.logger.info(f"News sorted by newest.")

            if topic_sort_key:
                self.driver.click_button('css:button.see-all-button')

                self.driver.screenshot(locator=None, filename='output/after_click_see_all.png')   

                time.sleep(5)
                
                topic_menu = self.driver.find_element('css:ul.search-filter-menu')  

                filter_list = self.driver.find_elements("tag:li",parent=topic_menu)

                self.driver.screenshot(locator=None, filename='output/start_get_list_items.png') 

                for idx, list_item in enumerate(filter_list):
                    self.driver.scroll_element_into_view(locator=list_item)

                    shadow_host_container = self.driver.find_elements("[name='metering-bottompanel']")
                
                    if shadow_host_container:
                        self.driver.screenshot(locator=None, filename='output/shadow_root.png') 
                    
                    filter_text = self.driver.find_element("tag:span", parent=list_item)
                    filter_text:str = self.driver.get_text(filter_text)

                    if filter_text.upper() == topic_sort_key.upper():
                        self.driver.scroll_element_into_view(locator=list_item)
                        self.driver.wait_until_element_is_visible(locator=list_item, timeout=10)
                        click_box = self.driver.find_element("css:input.checkbox-input-element", parent=list_item)
                        self.driver.click_element(click_box)
                        time.sleep(5)
                        break

                self.driver.screenshot(locator=None, filename='output/end_sorted_topic_results.png')

        except Exception as e:
            self.logger.error(f"Error sorting news results: {e}")
            self.driver.screenshot(locator=None, filename='output/error_sorting_news_results.png')
            raise e

    def get_news(self,max_months:int=0):
        try:
            all_news_retrieved = False
            max_date_to_search = get_first_day_of_earlier_month(max_months)
                  
            news_items = self.driver.find_elements("css:[data-content-type='article']")
            print('News retrieved', len(news_items))

            if not news_items:
                all_news_retrieved = True
            
            for idx, news in enumerate(news_items):
                try:
                    div_content = self.driver.find_elements("css:div.promo-content", parent= news)
                    if div_content:
                        print('shadow banner found')
                    
                    timestamp = self.driver.find_element("css:p.promo-timestamp", parent=div_content)
                    if timestamp:
                        print('timestamp found')
                        timestamp = self.driver.get_element_attribute(timestamp, "data-timestamp")
                        news_date_str = timestamp_to_date(int(timestamp))
                        self.logger.info(f"News date: {news_date_str}")
                    
                    self.driver.screenshot(locator=None, filename=f'output/{idx}_{news_date_str}_news.png')

                    all_news_retrieved = True
                    
                    # if compare_dates(news_date_str, max_date_to_search):
                    #     print('Got maximum of news!')
                    #     print('!!!!!!!!!!!!!!!!!!!!!!!!')
                    #     print(f'got {len(self.news_list)} articles!')
                    #     all_news_retrieved = True
                    #     break
                    
                    # promo_title = div_content.find_element(By.CSS_SELECTOR, "h3.promo-title")                    
                    # title_link = promo_title.find_element(By.TAG_NAME, "a")
                    # news_link = title_link.get_attribute("href")
                    # news_title = title_link.text
                    
                    # paragraph_description = div_content.find_element(By.CSS_SELECTOR, "p.promo-description")
                    # news_description = paragraph_description.text

                    # print(news_date_str)                        
                    # print(f"News title: {news_title}")
                    
                    # media_content = news.find_element(By.CSS_SELECTOR, "div.promo-media")
                    # image = media_content.find_elements(By.CSS_SELECTOR, "img.image")
                    
                    # image_link = None
                    # image_name = None
                    
                    # if image:
                    #     image = image[0]
                    #     image_link = image.get_attribute("src")
                    #     # print('Image:', image_link)
                        
                    #     image_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    #     image.screenshot(f'output/{image_name}.png') 

                    
                    # title_matches = count_string_matches(self.search_phrase, news_title)
                    # description_matches = count_string_matches(self.search_phrase, news_description)
                    # total_search_matches = title_matches + description_matches

                    # title_money_matches = find_and_count_money_patterns(news_title)
                    # description_money_matches = find_and_count_money_patterns(news_description)
                    # total_money_matches = title_money_matches + description_money_matches

                    # print('Matches',total_search_matches)
                    # print('Money matches',total_money_matches)

                    # print('------------------')
                    
                    # self.news_list.append({
                    #     'title': news_title,
                    #     'link': news_link,
                    #     'description': news_description,
                    #     'date': news_date_str,
                    #     'image_link': image_link,
                    #     'image_name': image_name,
                    #     'total_search_matches': total_search_matches
                    # })
                    
                except Exception as e:
                    all_news_retrieved = True
                    self.logger.error(f"Error getting news: {e}")
                    print(e)
                
            # next_page_container = self.driver.find_element(By.CSS_SELECTOR, "div.search-results-module-next-page")
            # next_page_link = next_page_container.find_elements(By.TAG_NAME, "a")
            # if next_page_link:
            #     next_page_link = next_page_link[0]
            #     next_page_link.click()    
            # else:
            #     all_news_retrieved = True
        except Exception as e:
            self.logger.error(f"Error getting news: {e}")
            raise e
        
    def driver_quit(self):
        if self.driver:
            self.driver.quit()
            
    def export_retrieved_news(self):
        return self.news_list

if __name__ == "__main__":
    input = {
        "search_phrase": "elections in usa",
        "topic": "Entertainment & Arts",
        "news_type": "",
        "months": 0
    }

    rpa = RpaNewsLatimesRobocorp()
    rpa.set_webdriver()
    rpa.open_url("https://www.latimes.com/")
    rpa.search_content(search_phrase=input['search_phrase'])
    # rpa.sort_news_results(topic_sort_key=input['topic'])
    
    # rpa.get_news(max_months=input['months'])    

    # rpa.driver_quit()

    # news_list = rpa.export_retrieved_news()
    # save_dict_to_xlsx(news_list, 'output/news_list.xlsx')