import requests
import math
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, _url):
        self.url = _url
        self.headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70.", 
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-mobile": "?0",
        "Content-Type": "text/plain;charset=UTF-8"
        }

    def get_soup(self):
        page = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup

    def get_jobs_df(self):
        return
