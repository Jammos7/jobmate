from scrapers.IndeedScraper import IndeedScraper
from scrapers.ReedScraper import ReedScraper
import pandas as pd

role=input('Please enter a role: ')
location=input('Please enter your location: ')

indeedScraper = IndeedScraper(role, location)
reedScraper = ReedScraper(role, location)


jobs = pd.concat([indeedScraper.get_jobs(), reedScraper.get_jobs()])

print(jobs.sort_values(by='salary', ascending=False))