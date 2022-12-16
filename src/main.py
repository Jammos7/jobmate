import func
import pandas as pd

fc = func.Func()
role=input('Please enter a role: ')
location=input('Please enter your location: ')

jobs = fc.get_indeed_jobs(role, location)
jobs = pd.concat([jobs, fc.get_reed_jobs(role, location)])

print(jobs)
jobs.to_csv("jobs.csv")