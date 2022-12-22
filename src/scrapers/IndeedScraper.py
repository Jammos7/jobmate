from scrapers.scraper import Scraper
import pandas as pd
import math
import re

class IndeedScraper(Scraper):

    def __init__(self, _role, _location):
        url = "http://uk.indeed.com/jobs?q="+ _role + "&l=" + _location
        super().__init__(url)

    def get_jobs(self):
        jobs_df = pd.DataFrame()
        # Use a CSS selector to find the job listings
        table_list = self.soup.body.main.select(".resultContent")
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
                if table.select_one(".metadata.salary-snippet-container").select_one(".attribute_snippet"):
                    salaryString = table.select_one(".metadata.salary-snippet-container").select_one(".attribute_snippet").text
                else:
                    salaryString = 'Not Listed'                
                salary = re.search(pattern, salaryString).group(1).replace(',', '')
            else:
                salaryString = 'Not Listed'
                salary = math.nan
            URL = table.select_one("a[role=button]").get("href")
            job = {"source": "Indeed", "title":title, "companyName":companyName, "companyLocation":companyLocation, "salaryString":salaryString, "salary":float(salary), "URL":"http://uk.indeed.com" + URL}
            jobs_df = pd.concat([jobs_df, pd.DataFrame([job])])
        return jobs_df

