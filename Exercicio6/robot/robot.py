from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as ServiceFirefox
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium import webdriver
from .waits import Waits
import logging


def get_driver():
    try:
        # service_firefox = ServiceFirefox(executable_path=GeckoDriverManager().install())
        # driver = webdriver.Firefox(service=service_firefox)
        
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        service_chrome = ServiceChrome(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service_chrome, options=chrome_options)
        return driver
    
    except:
        return None


class JKRowling:
    def __init__(self):
        self.waits = Waits()
                       
    def open_browser(self):
        try:
            driver = get_driver()
            driver.maximize_window()
            driver.get('http://quotes.toscrape.com/')
            return {'error': False, 'type': '', 'data': '', 'driver': driver}
        
        except Exception as e:
            print(e)
            return {'error': True, 'type': 'Error opening browser', 'data': f'{e}'}
        
    def find_quotes(self, driver:webdriver):
        try:
            list_data = []
            list_quotes = self.waits.wait_all_presence({"css_selector": "div[class='quote']"}, driver)
            for quote in list_quotes:
                
                if quote.find_element(By.CSS_SELECTOR, ".author").text == "J.K. Rowling":
                    data = {"text": "", "tags": []}

                    text = quote.find_element(By.CSS_SELECTOR, ".text").text
                    data['text'] = str(text).strip().replace("“", "'").replace("”", "'").replace("\"", "'")
                    
                    tags = quote.find_elements(By.CSS_SELECTOR, ".tag")
                    for tag in tags:
                        data["tags"].append(tag.text)
                        
                    list_data.append(data)
            return {'error': False, 'type': '', 'data': list_data}
                        
        except Exception as e:
            print(e)
            return {'error': True, 'type': 'Error extracting quotes', 'data': f'{e}'}
        
    def author_extraction(self, driver:webdriver):
        try:
            driver.get(f"http://quotes.toscrape.com/author/J-K-Rowling/")
            
            name = self.waits.wait_presence({"css_selector": "h3[class='author-title']"}, driver).text
            birth_date = self.waits.wait_presence({"css_selector": "span[class='author-born-date']"}, driver).text
            birth_location = self.waits.wait_presence({"css_selector": "span[class='author-born-location']"}, driver).text
            description = self.waits.wait_presence({"css_selector": "div[class='author-description']"}, driver).text
            
            data = {
                "name": name,
                "birth_date": birth_date,
                "birth_location": birth_location,
                "description": description,
            }
            return {'error': False, 'type': '', 'data': data}
            
        except Exception as e:
            print(e)
            return {'error': True, 'type': 'Error extracting author information', 'data': f'{e}'}
            
            