# from RPA.core.webdriver import download, start
import logging
from selenium import webdriver
import json, os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helper_functions import timestamp_to_date, get_first_day_of_earlier_month, compare_dates



class RpaNews:

    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)



    def set_chrome_options(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument("--disable-gpu")
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

    def open_url(self, url:str, screenshot_name:str=None):
        try:
            self.driver.get(url)
            if screenshot_name:
                self.driver.get_screenshot_as_file(f'output/{screenshot_name}')

        except Exception as e:
            self.logger.error(f"Error opening URL: {e}")
            raise e
        
    def search_content(self, search_phrase:str):
        try:
            search_button = self.driver.find_element(By.CLASS_NAME, "SearchOverlay-search-button")
            if search_button:                
                search_button.click()
                print('Clicou no botão de pesquisa!')
                search_box = self.driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-input')
                print('Encontrada a search box!',search_box)

                if search_phrase:
                    search_box.send_keys(search_phrase)
                    
                time.sleep(1)
                'SearchOverlay-search-submit'
                go_search_button = self.driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-submit')
                go_search_button.click()
                print('Clicou no botão de pesquisa!')
                time.sleep(3)

            # search_box.send_keys(search_phrase)
            # search_box.submit()
            # self.driver.implicitly_wait(5)
        except Exception as e:
            self.logger.error(f"Error searching content: {e}")
            raise e
        
    def serach_category(self, category:str):
        try:
            category_filter = self.driver.find_element(By.CLASS_NAME, "SearchResultsModule-filters-content")

            if category_filter:
                category_filter.click()
                time.sleep(1)
                button_all_categories = self.driver.find_element(By.CLASS_NAME, "SearchFilter-seeAll-button")
                button_all_categories.click()
                time.sleep(1)

                'SearchFilter-items'
                category_list = self.driver.find_elements(By.CLASS_NAME, "SearchFilter-items-item")
                if category_list:
                    for category_item in category_list:
                        category_name = category_item.find_element(By.TAG_NAME, "span").text
                        
                        check_box = category_item.find_element(By.TAG_NAME, "input")
                        'SearchFilterInput-count'
                        category_count = category_item.find_element(By.CLASS_NAME, "SearchFilterInput-count").text
                        print(f'Category {category_name}: {category_count}',)

                        if category and category in category_name:
                            check_box.click()
                            time.sleep(1)
                            break

        except Exception as e:
            self.logger.error(f"Error searching category: {e}")
            raise e
        
    def sort_news_results(self, category_sort:str=None):
        try:
            if category_sort:
                
                sort_container = self.driver.find_element(By.CLASS_NAME, "SearchResultsModule-sorts")
                sort_select = sort_container.find_element(By.CLASS_NAME, "Select-input")
                select = Select(sort_select)            
                select.select_by_visible_text('Newest')
                time.sleep(3)
                
                category_filter = self.driver.find_element(By.CLASS_NAME, "SearchResultsModule-filters-content")
                category_filter.click()
                time.sleep(1)
                button_all_categories = self.driver.find_element(By.CLASS_NAME, "SearchFilter-seeAll-button")
                button_all_categories.click()
                category_list = self.driver.find_elements(By.CLASS_NAME, "SearchFilter-items-item")
                for category_item in category_list:
                    category_name = category_item.find_element(By.TAG_NAME, "span").text
                    if category_sort.upper() in category_name.upper():
                        check_box = category_item.find_element(By.TAG_NAME, "input")
                        check_box.click()
                        time.sleep(1)
                        self.driver.refresh()
                        break
                    
            
            
            
            # self.driver.refresh()
            # time.sleep(3)

        except Exception as e:
            self.logger.error(f"Error sorting news results: {e}")
            raise e

    def get_news(self,max_months:int=0):
        try:
            search_results_container = self.driver.find_element(By.CLASS_NAME, "SearchResultsModule-results")

            news_items = search_results_container.find_elements(By.CLASS_NAME, "PageList-items-item")
            
            max_date_to_search = get_first_day_of_earlier_month(max_months)

            # sort_input = self.driver.find_element(By.CLASS_NAME, "Select SearchFilterAsDropdown")
            # sort_input.click()
            # sort_input = sort_input.find_element(By.TAG_NAME, "select")
            # sort_input            

            if news_items:
                for news in news_items:
                    try:
                        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", news)
                        news_title = news.find_element(By.CLASS_NAME, "PagePromo-title")
                        news_title = news_title.find_element(By.TAG_NAME, "span").text

                        news_description = news.find_element(By.CLASS_NAME, "PagePromo-description")
                        news_description = news_description.find_element(By.TAG_NAME, "span").text

                        news_date = news.find_element(By.CLASS_NAME, "PagePromo-byline")
                        news_timestamp = news_date.find_element(By.TAG_NAME, "bsp-timestamp")
                        news_timestamp = news_timestamp.get_attribute("data-timestamp")
                        news_date_str = timestamp_to_date(int(news_timestamp))
                        
                        
                        if compare_dates(news_date_str, max_date_to_search):
                            print('Got maximum of news!')
                            print('!!!!!!!!!!!!!!!!!!!!!!!!')
                            break
                        
                        print(news_date_str)
                        print(news_title)
                        # print(news_description)

                        link_to_page = news.find_element(By.CLASS_NAME, "Link")                        
                        image_label = link_to_page.get_attribute("aria-label")
                        link_to_page = link_to_page.get_attribute("href")                        
                        print('Link:', link_to_page)
                        
                        
                        image_object = news.find_elements(By.TAG_NAME, "img")
                        image_name = None
                        image_link = None
                        
                        if image_object:
                            image_object = image_object[0]
                            image_link = image_object.get_attribute("src")   
                            image_name = '-'.join(link_to_page.split('/')[-1].split('-')[:-1])
                            image_object.screenshot(f'output/{image_name}.png')                            
                            
                            # download_image(image_link, f'')
                        else: image_link = None

                        # # print(image_label)
                        # # print(link_to_page)
                        print('Image',image_link)
                        print('Image name:', image_name)

                        print('------------------')
                    except Exception as e:
                        self.logger.error(f"Error getting news: {e}")
                        print(e)
                        break
        except Exception as e:
            self.logger.error(f"Error getting news: {e}")
            raise e
        
    def driver_quit(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    input = {
        'search_phrase': "elections in usa",
        'category': "",
        'months': 2
    }

    rpa = RpaNews()
    rpa.set_webdriver()
    rpa.open_url("https://apnews.com/", "arp_via_bot.png")
    rpa.search_content(search_phrase=input['search_phrase'])
    rpa.sort_news_results(category_sort=input['category'])

    rpa.get_news(max_months=input['months'])
    while True:
        True

    rpa.driver_quit()