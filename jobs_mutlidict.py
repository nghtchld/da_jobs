# * loads Seek for Data Analysis jobs job descriptions
# builds multidict for skill keywords
import multidict
import pandas as pd
import re
import pickle
import sys
import matplotlib.pyplot as plt
# paths
raw_dir = 'data/raw/'
save_dir = 'data/interim/'
proc_dir = 'data/processed/'
fig_dir = 'figures/'

# load jobs desc pickle
infile = open(save_dir + 'seek_jobs_text.pickle', 'rb')
jobs_text_list = pickle.load(infile)
infile.close

# * define list of skills keywords
skills = ['collection', 'reporting', 'statistical', 'visualisation', 'cleansing',
            'modelling', 'python', 'sql', 'excel', 'machine', 'Tableau', 'powerbi',
            'sas', 'jupyter', 'aws', 'azure', 'cloud', 'etl', 'rdbms', 'access']

# make a keyword multidict of skills
keySkillsDict = {}
tmpDict = {}

# define test desc_test as one job desc
#desc_test = jobs_text_list[0].lower()

# counting frequencies of skills over job descriptions
# each skill only counted once per job, added to multidict
for job in jobs_text_list:
    desc = job.lower()
    for skill in skills:
        if skill in desc.split(" "):
            val = tmpDict.get(skill, 0)
            tmpDict[skill] = val + 1
for k, v in sorted(tmpDict.items(), key=lambda kv: kv[1]):
    keySkillsDict.setdefault(k, v)

# making a df with percent column, for plots
df_skills = pd.DataFrame(keySkillsDict.items(), columns=['skill', 'total'])
df_skills['percentage'] = (df_skills.total / len(jobs_text_list)) * 100 
df_skills.head()

plt.barh(df_skills['skill'], df_skills['total'])

plt.barh(df_skills['skill'], df_skills['percentage'])


