from scrapers.IndeedScraper import IndeedScraper
from scrapers.ReedScraper import ReedScraper
from flask import Flask, request, render_template
import pandas as pd
import string

app = Flask(__name__)

@app.route('/')
def main():
    joblist = pd.DataFrame()
    return render_template('index.html', data = joblist, showresults = False)
    

@app.route('/', methods=['POST'])
def results():
    role = request.form['role']
    location = request.form['location']
    indeedScraper = IndeedScraper(role, location)
    reedScraper = ReedScraper(role, location)
    joblist = pd.concat([indeedScraper.get_jobs(), reedScraper.get_jobs()]).sort_values(by='salary', ascending=False).to_dict(orient="records")
    return render_template('index.html', data = joblist, role = string.capwords(role), location = string.capwords(location), showresults = True)

if __name__ == '__main__':
    app.run(debug=True)