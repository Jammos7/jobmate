from scrapers.scraper import Scraper
import math
import re
import pandas as pd

class ReedScraper(Scraper):

    def __init__(self, _role, _location):
        url = "http://www.reed.co.uk/jobs/" + _role.replace(' ', '-') + "-jobs-in-" + _location
        super().__init__(url)

    def get_jobs(self):
        jobs_df = pd.DataFrame()
        # Use a CSS selector to find the job listings
        table_list = self.soup.body.select(".job-result-card")
        for table in table_list:
                # Use the .text attribute to get the text of an element
            title = table.select_one(".job-result-heading__title").find("a").text
            companyName = table.select_one(".job-result-heading__posted-by").find("a").text
            companyLocation = table.select_one(".job-metadata__item--location").get_text()

            # Use a regular expression to extract the salary from the text
            pattern = r"\£([0-9.,]+)\s+p"

            if re.search(pattern, table.select_one(".job-metadata__item--salary").get_text()):
                salaryString = table.select_one(".job-metadata__item--salary").get_text().strip()
                salary = re.search(pattern, salaryString).group(1).replace(',', '')
            else:
                salaryString = 'N/A'
                salary = math.nan

            URL = table.select_one(".job-result-heading__title").find("a").get("href")

            job = {"source": "Reed", "title":title.strip(), "companyName":companyName.strip(), "companyLocation":companyLocation.strip(), "salaryString":salaryString, "salary":float(salary), "URL":"http://reed.co.uk" + URL}
            jobs_df = pd.concat([jobs_df, pd.DataFrame([job])])
        
        return jobs_df