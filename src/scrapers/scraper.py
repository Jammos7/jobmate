import requests
import pandas as pd
from bs4 import BeautifulSoup

class Scraper():
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
        self.make_request()
        self.get_soup()
        self.html = '<table>'

    def make_request(self):
        self.page = requests.get(self.url, headers=self.headers)
        return self.page

    def get_soup(self):
        self.soup = BeautifulSoup(self.page.text, "html.parser")
        return self.soup

    def get_url(self):
        return self.url

    def get_jobs(self):
        return
