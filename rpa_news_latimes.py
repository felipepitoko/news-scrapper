import json, os, time, logging, random, string , re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helper_functions import *


class RpaNewsLatimes:

    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        self.search_phrase = None
        self.news_list = []
        
    def set_chrome_options(self):
        options = webdriver.ChromeOptions()
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
        options = self.set_chrome_options()
        self.driver = webdriver.Chrome(options=options)
        if self.driver:
            self.driver.implicitly_wait(5)

    def open_url(self, url:str):
        try:
            self.driver.get(url)
        except Exception as e:
            self.logger.error(f"Error opening URL: {e}")
            raise e
        
    def search_content(self, search_phrase:str=''):
        try:
            self.search_phrase = search_phrase
            search_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-element='search-button']")
            
            if search_button:                
                search_button.click()
                search_box = self.driver.find_element(By.CSS_SELECTOR, "input[data-element='search-form-input']")
                search_box.send_keys(search_phrase)
                
                subimit_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-element='search-submit-button']")
                subimit_button.click()
                
        except Exception as e:
            self.logger.error(f"Error searching content: {e}")
            raise e

    def sort_news_results(self, topic_sort_key:str=None, type_sort_key:str=None):
        try:
            sort_container = self.driver.find_element(By.CSS_SELECTOR, "select.select-input")
            
            sort_input = Select(sort_container)
            sort_input.select_by_visible_text('Newest')
            time.sleep(5)           
            
                
            see_all_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.see-all-button")
            for button in see_all_buttons:                    
                button.click()
                time.sleep(1)
            
            filter_menus = self.driver.find_elements(By.CSS_SELECTOR, "ul.search-filter-menu")
            
            topics_list = filter_menus[0].find_elements(By.TAG_NAME, "li")
            types_list = filter_menus[0].find_elements(By.TAG_NAME, "li")
            
            shadow_host_container = self.driver.find_elements(By.CSS_SELECTOR, "[name='metering-bottompanel']")
            
            if shadow_host_container:
                shadow_host = shadow_host_container[0]
                shadow_root = self.driver.execute_script('return arguments[0].shadowRoot;', shadow_host)
                element_in_shadow_dom = shadow_root.find_element(By.CSS_SELECTOR, "a.met-flyout-close")
                element_in_shadow_dom.click()
            
            if topic_sort_key:                
                for topic in topics_list:
                    topic_name = topic.find_element(By.TAG_NAME, "span").text
                    if topic_sort_key.upper() in topic_name.upper():
                        check_box = topic.find_element(By.TAG_NAME, "input")
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", check_box)                        
                        check_box.click()
                        time.sleep(3)
                        print('Selected topic:', topic_name)
                        break
                    
            if type_sort_key:                
                for type in types_list:
                    type_name = type.find_element(By.TAG_NAME, "span").text
                    if type_sort_key.upper() in type_name.upper():
                        check_box = type.find_element(By.TAG_NAME, "input")
                        check_box.click()
                        time.sleep(3)
                        print('Selected type:', type_name)
                        break

        except Exception as e:
            self.logger.error(f"Error sorting news results: {e}")
            raise e

    def get_news(self,max_months:int=0):
        try:
            all_news_retrieved = False
            max_date_to_search = get_first_day_of_earlier_month(max_months)
            
            while not all_news_retrieved:            
                news_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-content-type='article']")
                print('News retrieved', len(news_items))
                
                for news in news_items:
                    try:
                        div_content = news.find_element(By.CSS_SELECTOR, "div.promo-content")
                        
                        timestamp = div_content.find_element(By.CSS_SELECTOR, "p.promo-timestamp")
                        timestamp = timestamp.get_attribute("data-timestamp")
                        news_date_str = timestamp_to_date(int(timestamp))
                        
                        if compare_dates(news_date_str, max_date_to_search):
                            print('Got maximum of news!')
                            print('!!!!!!!!!!!!!!!!!!!!!!!!')
                            print(f'got {len(self.news_list)} articles!')
                            all_news_retrieved = True
                            break
                        
                        promo_title = div_content.find_element(By.CSS_SELECTOR, "h3.promo-title")                    
                        title_link = promo_title.find_element(By.TAG_NAME, "a")
                        news_link = title_link.get_attribute("href")
                        news_title = title_link.text
                        
                        paragraph_description = div_content.find_element(By.CSS_SELECTOR, "p.promo-description")
                        news_description = paragraph_description.text

                        print(news_date_str)                        
                        print(f"News title: {news_title}")
                        
                        media_content = news.find_element(By.CSS_SELECTOR, "div.promo-media")
                        image = media_content.find_elements(By.CSS_SELECTOR, "img.image")
                        
                        image_link = None
                        image_name = None
                        
                        if image:
                            image = image[0]
                            image_link = image.get_attribute("src")
                            # print('Image:', image_link)
                            
                            image_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                            image.screenshot(f'output/{image_name}.png') 

                        
                        title_matches = count_string_matches(self.search_phrase, news_title)
                        description_matches = count_string_matches(self.search_phrase, news_description)
                        total_search_matches = title_matches + description_matches

                        title_money_matches = find_and_count_money_patterns(news_title)
                        description_money_matches = find_and_count_money_patterns(news_description)
                        total_money_matches = title_money_matches + description_money_matches

                        print('Matches',total_search_matches)
                        print('Money matches',total_money_matches)

                        print('------------------')
                        
                        self.news_list.append({
                            'title': news_title,
                            'link': news_link,
                            'description': news_description,
                            'date': news_date_str,
                            'image_link': image_link,
                            'image_name': image_name,
                            'total_search_matches': total_search_matches
                        })
                        
                    except Exception as e:
                        self.logger.error(f"Error getting news: {e}")
                        print(e)
                        break
                    
                next_page_container = self.driver.find_element(By.CSS_SELECTOR, "div.search-results-module-next-page")
                next_page_link = next_page_container.find_elements(By.TAG_NAME, "a")
                if next_page_link:
                    next_page_link = next_page_link[0]
                    next_page_link.click()    
                else:
                    all_news_retrieved = True
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

    rpa = RpaNewsLatimes()
    rpa.set_webdriver()
    rpa.open_url("https://www.latimes.com/")
    rpa.search_content(search_phrase=input['search_phrase'])
    rpa.sort_news_results(topic_sort_key=input['topic'])
    
    rpa.get_news(max_months=input['months'])    

    rpa.driver_quit()

    news_list = rpa.export_retrieved_news()
    save_dict_to_xlsx(news_list, 'output/news_list.xlsx')