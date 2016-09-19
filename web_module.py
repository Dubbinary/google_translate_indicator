import requests
from bs4 import BeautifulSoup
from selenium import webdriver

headers = {'User-agent': 'Mozilla/5.0'}
base_url = "https://translate.google.com/#%s/%s/%s"

def translate(from_lang, to_lang, text):
    global headers, base_url
    url = base_url % (from_lang, to_lang, text)
    soup = BeautifulSoup(get_page_cotent(url), 'html.parser')
    # print(soup.find("span", {"id": "result_box"}).get_text())  #DEBUG
    return soup.find("span", {"id": "result_box"}).get_text()

def get_page_cotent(url):
    driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
    driver.get(url)
    driver.implicitly_wait(5)
    # driver.save_screenshot('screenshot.png')  #DEBUG
    return driver.page_source
