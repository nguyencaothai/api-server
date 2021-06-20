from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

PATH = '/root/python_tool/screenshot_tool/'

def take_screenshot(url, token):
    # Set option for chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1360,768')

    driver = webdriver.Chrome(PATH + 'chromedriver', options=chrome_options)

    # Request URL
    driver.get(url)

    full_page_size = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    driver.set_window_size(full_page_size('Width'), full_page_size('Height'))
    time.sleep(5)
    driver.save_screenshot(PATH + token + '.png')
