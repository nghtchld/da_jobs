# * scraped Seek and Indeed for Data Analysis jobs
# looks for skill keywords and builds data structures
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import pickle
import time
import sys
import os

# paths
raw_dir = 'data/raw/'
save_dir = 'data/interim/'
proc_dir = 'data/processed/'
fig_dir = 'figures/'

# define job search
job_search = "Data Analyst"
# turn job search into Seek query string
job_param = job_search.lower().replace(' ', '-') + '-jobs'

# * loop over job search results pages
# * initial page has no "page number"
# intiial URL generation
url = ("https://www.seek.com.au/" + job_param)

# loop, try: over N more pages, except: pass
pg_no = 1
da_ad_links = []

for n in range(10, 100):
    time.sleep(0.5)
    try:
        next_pg = "?page=" + str(pg_no + n)  # int as str
        next_url = url + next_pg
        r = requests.post(next_url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, "lxml")
        h1_tags = soup.find_all('h1')

        for h1 in h1_tags:
            if "Data Analyst" in h1.get_text():
                da_ad_links.append(h1.find('a').get('href')[:13])
    except:
        print("Error!", sys.exc_info()[0], "occured.")
        pass


# TODO counting jobClassification and jobSubClassification, use DF?
# <a href="... data-automation="jobClassification" ... target="_self">Information &amp; Communication Technology</a>
# <a href="... data-automation="jobSubClassification" ... target="_self">Business/Systems Analysts</a>
# <div data-automation="jobDescription" ...
# * loop for scraping each job ad page in url list
# init job page text text list
#jobs_text_list = []
# URL request, job description loop
for i in range(len(da_ad_links)):
    time.sleep(0.5)
    url_job = ("https://www.seek.com.au/" + da_ad_links[i])
    h_doc_job = requests.post(url_job).text
    div_job = (BeautifulSoup(h_doc_job, "lxml")
               .find('div', class_="templatetext"))
    if div_job is None:
        div_job = (BeautifulSoup(t_doc, "lxml")
                   .find('div', attrs={"data-automation": "jobDescription"}))
    jobs_text_list.append(div_job.get_text())

# save jobs_text_list to pickle
file = 'seek_jobs_text.pickle'
with open(save_dir + file, 'wb') as f:
    pickle.dump(jobs_text_list, f)

# TODO analyse the job desc text data
# * use multidict approach? use a dict of target words only?
# * trying multidict approach in new file: jobs_mutlidict.py

# TODO script that exports each job link and key skills to excel sheet
