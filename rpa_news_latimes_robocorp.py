import time, logging

from RPA.Browser.Selenium import Selenium
from selenium.webdriver import ChromeOptions

from helper_functions import *

class RpaNewsLatimesRobocorp:
    """Retrieve the newest news from LAtimes website.
     
    It can also search for a given phrase and filter
    results by a given topic.
    """

    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        self.search_phrase = None
        self.news_list = []
        
    def set_chrome_options(self):
        """Define webdriver options

        Returns: a ChromeOptions object
        """

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
        """Set up the webdriver
        """
        try:
            browser = Selenium()
            options = self.set_chrome_options()
            browser.open_available_browser(
                headless=True, options=options,browser_selection='Chrome')        
            
            self.driver = browser
            self.logger.info("WebDriver set up successfully via rpaframework.")
        except Exception as e:
            self.logger.error(f"Error setting up WebDriver: {e}")
            raise e

    def open_url(self, url:str):
        """Open the given URL in the webdriver
        """
        try:
            self.driver.go_to(url)
            self.logger.info(f"Driver opened url {url}")
        except Exception as e:
            self.logger.error(f"Error opening URL: {e}")
            raise e
        
    def search_content(self, search_phrase:str=''):
        """Open the search input and inputs search phrase
        """
        try:
            self.search_phrase = search_phrase

            self.driver.click_button(
                "css:button[data-element='search-button']")
            
            self.driver.wait_until_element_is_visible(
                "css:input[data-element='search-form-input']",timeout=5)
            
            self.driver.input_text(
                "css:input[data-element='search-form-input']",search_phrase)
            
            self.driver.click_element(
                "css:button[data-element='search-submit-button']")

            self.driver.screenshot(
                locator=None,filename='output/search_results.png')      
            
            self.logger.info(f"Search for {search_phrase} completed.")                      
        except Exception as e:
            self.logger.error(f"Error searching content: {e}")
            raise e

    def sort_news_results(self, topic_sort_key:str=None):
        """Sort the search results by newest and topic, if applicable
        """
        try:
            select_list = self.driver.find_element('css:select.select-input')
            self.driver.select_from_list_by_value(select_list, '1')

            self.logger.info(f"News sorted by newest.")

            if topic_sort_key:
                self.driver.click_button('css:button.see-all-button')  

                time.sleep(5)
                
                topic_menu = self.driver.find_element(
                    'css:ul.search-filter-menu')  

                filter_list = self.driver.find_elements(
                    "tag:li",parent=topic_menu)

                for idx, list_item in enumerate(filter_list):
                    self.driver.scroll_element_into_view(locator=list_item)

                    shadow_host_container = self.driver.find_elements(
                        "[name='metering-bottompanel']")
                
                    if shadow_host_container:
                        self.logger.info('Banner in shadow root located.')
                    
                    filter_text = self.driver.find_element("tag:span", 
                                                           parent=list_item)
                    
                    filter_text:str = self.driver.get_text(filter_text)

                    if filter_text.upper() == topic_sort_key.upper():
                        self.driver.scroll_element_into_view(
                            locator=list_item)
                        
                        self.driver.wait_until_element_is_visible(
                            locator=list_item, timeout=10)
                        
                        click_box = self.driver.find_element(
                            "css:input.checkbox-input-element", 
                            parent=list_item
                            )
                        
                        self.driver.click_element(click_box)
                        time.sleep(5)
                        break

        except Exception as e:
            self.logger.error(f"Error sorting news results: {e}")
            self.driver.screenshot(locator=None, 
                                   filename=
                                   'output/error_sorting_results.png')
            raise e

    def get_news(self,max_months:int=0):
        """Collect news until limit of news age is achieved.
        """
        try:
            all_news_retrieved = False
            max_date_to_search = get_first_day_of_earlier_month(max_months)

            while not all_news_retrieved:                  
                news_items = self.driver.find_elements(
                    "css:[data-content-type='article']")

                if not news_items:
                    all_news_retrieved = True
                
                for idx, news in enumerate(news_items):
                    try:
                        image_link = None
                        image_name = None
                        news_title = None
                        news_description = None
                        news_link = None
                        
                        div_timestamp:list = self.driver.find_elements(
                            "css:p.promo-timestamp", parent=news)
                        
                        if div_timestamp:
                            div_timestamp = div_timestamp[0]

                            timestamp = self.driver.get_element_attribute(
                                div_timestamp, "data-timestamp"
                                )
                            
                            news_date_str = timestamp_to_date(int(timestamp))

                            if compare_dates(news_date_str, 
                                             max_date_to_search):
                                
                                all_news_retrieved = True

                                self.logger.info(
                                    f"""Reached max date to search:\
                                      {max_date_to_search}""")
                                
                                break

                        div_title:list = self.driver.find_elements(
                            "css:div.promo-title-container", parent=news)
                        
                        if div_title:
                            div_title = div_title[0]

                            title_anchor = self.driver.find_elements(
                                "css:a.link", parent=div_title)

                            if title_anchor:
                                news_title = self.driver.get_text(title_anchor)
                                news_link = self.driver.get_element_attribute(
                                    title_anchor, "href")

                        div_description:list= self.driver.find_elements(
                            "css:p.promo-description", parent=news)
                        
                        if div_description:
                            div_description = div_description[0]
                            news_description = self.driver.get_text(
                                div_description)

                        div_promo_media:list = self.driver.find_elements(
                            "css:div.promo-media", parent=news)
                        
                        if div_promo_media:
                            div_promo_media = div_promo_media[0]
                            
                            image = self.driver.find_elements(
                                "css:img.image", 
                                parent=div_promo_media)
                            
                            image_link = self.driver.find_elements(
                                "css:a.promo-placeholder", 
                                parent=div_promo_media)
                            
                            if image:
                                image = image[0]
                                image_name = None
                                if image_link:
                                    image_link = image_link[0]
                                    image_name = \
                                        self.driver.get_element_attribute(
                                        image_link, "href")
                                    
                                    image_name = image_name.split('/')[-1]
                                    
                                image_link = \
                                    self.driver.get_element_attribute(
                                        image, "src")
                                
                                self.driver.capture_element_screenshot(
                                    image, 
                                    f'output/{idx}_{news_date_str}_news.png'\
                                        if not image_link else\
                                            f'output/{image_name}.png')

                        title_matches = count_string_matches(
                            self.search_phrase, news_title)                        
                        description_matches = count_string_matches(
                            self.search_phrase, news_description)                        
                        total_search_matches = title_matches + \
                            description_matches

                        title_money_matches = find_and_count_money_patterns(
                            news_title)
                        description_money_matches = \
                            find_and_count_money_patterns(news_description)                        
                        total_money_matches = title_money_matches + \
                            description_money_matches

                        self.news_list.append({
                            'title': news_title,
                            'link': news_link,
                            'description': news_description,
                            'date': news_date_str,
                            'image_link': image_link,
                            'image_name': f"{image_name}.png",
                            'total_search_matches': total_search_matches,
                            'money_mentioned': 'True' if total_money_matches else 'False'
                        })

                        all_news_retrieved = True
                    except Exception as e:
                        all_news_retrieved = True
                        self.logger.error(f"Error getting news: {e}")
                        self.driver.screenshot(
                            locator=None, 
                            filename='output/error_news_details.png')
                        
                try:
                    next_page_container = self.driver.find_elements(
                        "css:div.search-results-module-next-page")
                    
                    next_page_container = next_page_container[0]
                    next_page_link = self.driver.find_elements(
                        "tag:a",parent=next_page_container)
                    
                    if next_page_link:
                        next_page_link = next_page_link[0]
                        self.driver.click_element(next_page_link)
                    else:
                        all_news_retrieved = True    
                        self.logger.info("No more news to retrieve.")
                except Exception as e:
                    self.logger.error(f"Error getting next page: {e}")
                    all_news_retrieved = True

        except Exception as e:
            self.logger.error(f"Error getting news: {e}")
            raise e
        
    def driver_quit(self):
        """Close the webdriver instance"""
        if self.driver:
            self.driver.close_browser()
            self.logger.info("WebDriver closed.")
            
    def export_retrieved_news(self)->list[dict]:
        """Export retrieved news.

        Returns:
            list[dict]: A list of dictionaries representing the retrieved news
        """
        return self.news_list