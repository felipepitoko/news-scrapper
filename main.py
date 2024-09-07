from selenium import webdriver
import time
from selenium.webdriver.common.by import By

try:
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--headless')
    driver_options.add_argument('--no-sandbox')
    driver_options.add_argument('--disable-gpu')
    driver_options.add_argument('--disable-blink-features=AutomationControlled')
    driver_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver_options.add_argument('--disable-dev-shm-usage')
    

    driver = webdriver.Chrome(options=driver_options)
    driver.get("https://www.reuters.com/")
    print('Connected to reuters!')

    time.sleep(5)

    sections_with_content = driver.find_elements(By.CSS_SELECTOR, 'section')

    print('Total of sections',len(sections_with_content))
    # for section in sections_with_content:
    #     if 'story-cluster' in section.get_attribute('data-testid'):
    #         print('A table of contents.')
    #         break

    # print('Total sections',len(sections_with_content))

    # time.sleep(5)

    driver.quit()
except Exception as e:
    print(e)