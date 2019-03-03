# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 22:23:32 2019

@author: Adrian

# Pull review scores and counts from indeed for a selection of companies in WPG!
# Store this data in an Azure SQL Database

"""
import time
import pandas as pd
import pyodbc as py

import os
path = 'C:\\Users\\Adrian\\Desktop\\Indeed-Scrape'
os.chdir(path)

from fetch import indeedFetchNow

today = time.strftime('%Y-%m-%d')

# Open Connection to SQL Server (azure)
server = 'azuretrial.database.windows.net'
database = 'azureIndeed'
username = '***'
password = '***'
driver= '{SQL Server Native Client 11.0}'
con = py.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

# Pull in companies, as found on wikipedia.
companies = pd.read_csv('companies.txt', sep='\t', encoding ='latin1')
companies = companies[(companies['Headquarters']=='Winnipeg')&
                      (companies['Notes'].str.find('defunct')==-1)]

cols = ['Name', 'Industry', 'Sector', 'Headquarters', 'Founded', 'Notes']
companies = companies[cols]
companies['Founded'] = [str(val)[0:4] for val in companies['Founded']]

# With cursor, remove old companies and insert most recent list of companies
cursor = con.cursor()
cursor.execute('DELETE FROM companies')
cursor.executemany('INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?)', [tuple(row) for row in companies.values])
cursor.commit()

def cleanKs(item):
    '''Converts strings such as '10k' to an integer, in this case 10000. Note that precision is still lost '''
    if 'K' in item:
        return float(item.replace('K', ''))*1000
    else:
        return item

allToday = pd.DataFrame()

for index, row in companies.iterrows():
    # For each company, fetch data from indeed. Store results in dictionary.
    print(row['Name'])
    cmpStats = indeedFetchNow(row['Name'])
    if cmpStats is None:
        print('Fetch has failed for: ', row['Name'])
        continue
    else:
        cmpStats = {key: cleanKs(value) for key, value in cmpStats.items()}
        cmpStats['Date'] = today
        cmpStats['Company'] = row['Name']
        allToday = allToday.append(cmpStats, ignore_index=True)

cols = ['Company', 'Date', 'Culture', 'Job Security & Advancement', 'Management'
        , 'Pay & Benefits', 'Work-Life Balance', 'Overall Rating', 'Jobs'
        , 'Reviews', 'Salaries']

allToday = allToday[cols].dropna()

floatCols = ['Culture', 'Job Security & Advancement', 'Management'
        , 'Pay & Benefits', 'Work-Life Balance', 'Overall Rating']
intCols = ['Jobs', 'Reviews', 'Salaries']

for col in floatCols:
    allToday[col] = allToday[col].astype(float)
for col in intCols:
    allToday[col] = allToday[col].astype(int)

print(allToday)
cursor.executemany('INSERT INTO scores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [tuple(row) for row in allToday.values])
cursor.commit()
con.close()

