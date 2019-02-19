# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 22:23:32 2019

@author: Adrian
"""
import time
import pandas as pd
import pyodbc as py
from fetch import indeedFetchNow

today = time.strftime('%Y-%m-%d')

# Open Connection to SQL Server (local)
con = py.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=***\SQLEXPRESS;"
                      "Database=indeed;"
                      "Trusted_Connection=yes;")

# 75 of Canada's largest companies
companies = pd.read_csv('companies.txt', sep='\t', encoding ='latin1')
companies = companies[(companies['Headquarters']=='Winnipeg')&
                      (companies['Notes'].str.find('defunct')==-1)]

cols = ['Name', 'Industry', 'Sector', 'Headquarters', 'Founded', 'Notes']
companies = companies[cols]
companies['Founded'] = [str(val)[0:4] for val in companies['Founded']]
cursor = con.cursor()
#cursor.execute('DELETE FROM companies')
#cursor.executemany('INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?)', [tuple(row) for row in companies.values])
#cursor.commit()

def cleanKs(item):
    if 'K' in item:
        return float(item.replace('K', ''))*1000
    else:
        return item

allToday = pd.DataFrame()
for index, row in companies.iterrows():
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

