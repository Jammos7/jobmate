import requests
import pandas as pd
import math
from bs4 import BeautifulSoup
import re

headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70.", 
    #"referer": "https://uk.indeed.com/",
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "sec-ch-ua-platform": "Windows",
    "sec-ch-ua-mobile": "?0",
    "Content-Type": "text/plain;charset=UTF-8"
    }

class Func:

    def __init__(this):
        this.headers = headers

    def get_indeed_jobs(this, _role, _location):
        jobs_df = pd.DataFrame()

        id_role = _role.replace(' ', '+')

        page = requests.get("http://uk.indeed.com/jobs?q="+ id_role + "&l=" + _location, headers=headers)

        soup = BeautifulSoup(page.text, "html.parser")

        # Use a CSS selector to find the job listings
        table_list = soup.body.main.select(".resultContent")

        for table in table_list:
            # Use the .text attribute to get the text of an element
            title = table.select_one('span[id^="jobTitle"]')['title']

            if table.select_one(".companyName").find("a"):
                companyName = table.select_one(".companyName").find("a").text
            else:
                companyName = table.select_one(".companyName").text


            if table.select_one(".companyLocation").find("a"):
                companyLocation = table.select_one(".companyLocation").find("a").text
            else:
                companyLocation = table.select_one(".companyLocation").text
            
            # Use a regular expression to extract the salary from the text
            pattern = r"\£([0-9.,]+)\s+a"
            if table.select_one(".metadata.salary-snippet-container"):
                salary = re.search(pattern, table.select_one(".metadata.salary-snippet-container").select_one(".attribute_snippet").text).group(1).replace(',', '')
            else:
                salary = math.nan

            URL = table.select_one("a[role=button]").get("href")

            job = {"source": "Indeed", "title":title, "companyName":companyName, "companyLocation":companyLocation, "salary":float(salary), "URL":"http://uk.indeed.com" + URL}

            jobs_df = pd.concat([jobs_df, pd.DataFrame([job])])
        
        return jobs_df

    def get_reed_jobs(this, _role, _location):
        jobs_df = pd.DataFrame()
        rd_role = _role.replace(' ', '-')

        rd_page = requests.get("http://www.reed.co.uk/jobs/" + rd_role + "-jobs-in-" + _location, headers=headers)
        print(rd_page.url)
        rd_soup = BeautifulSoup(rd_page.text, "html.parser")

        # Use a CSS selector to find the job listings
        table_list = rd_soup.body.select(".job-result-card")
        for table in table_list:
                # Use the .text attribute to get the text of an element
            title = table.select_one(".job-result-heading__title").find("a").text
            companyName = table.select_one(".job-result-heading__posted-by").find("a").text
            companyLocation = table.select_one(".job-metadata__item--location").get_text()

            # Use a regular expression to extract the salary from the text
            pattern = r"\£([0-9.,]+)\s+p"

            if re.search(pattern, table.select_one(".job-metadata__item--salary").get_text()):
                salary = re.search(pattern, table.select_one(".job-metadata__item--salary").get_text()).group(1).replace(',', '')
            else:
                salary = math.nan

            URL = table.select_one(".job-result-heading__title").find("a").get("href")

            job = {"source": "Reed", "title":title.strip(), "companyName":companyName.strip(), "companyLocation":companyLocation.strip(), "salary":float(salary), "URL":"http://reed.co.uk" + URL}
            jobs_df = pd.concat([jobs_df, pd.DataFrame([job])])
        
        return jobs_df