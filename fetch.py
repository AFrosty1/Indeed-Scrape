# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 22:13:40 2019

@author: Adrian
"""
def indeedFetchNow(company):
    '''Fetch current stats from indeed. Returns a Dictionary of the stats.'''
    from bs4 import BeautifulSoup
    import requests
    company_repl = company.replace(' ','-')
    raw_html = requests.get('https://www.indeed.ca/cmp/' + company_repl + '/reviews')
    
    if raw_html.status_code!=200:
        print('HTML fetch failed.')
        return
    else:
        print('Connection Success!')
    
    soup = BeautifulSoup(raw_html.content, 'html.parser')
    
    activity={}
    
    # Dictionary of HTML parameters
    locs = {'Reviews': {'Tag': 'li', 'Class': 'cmp-menu--reviews cmp-menu-selected'}
            , 'Salaries': {'Tag': 'li', 'Class': 'cmp-menu--salaries'}
            , 'Jobs': {'Tag': 'li', 'Class': 'cmp-menu--jobs'}
            , 'Overall Rating': {'Tag': 'span', 'Class': 'cmp-header-rating-average'}
    }
    try:
        for key, value in locs.items():
            html = soup.find_all(value['Tag'], class_=value['Class'])
            val = html[0].get_text('|').split('|')[0]
            if val in ['Salaries', 'Reviews', 'Jobs']:
                val = '0'
            else:
                pass
            activity[key] = val 
    except:
        print('Tag not found - pt1')
        return
    
    #categories
    html_rating_categories = soup.find_all('a', class_='cmp-underline-none')
    try: 
        for item in html_rating_categories:
            if len(item.contents)==1:
                pass
            else:
                rating_type = item.contents[2]
                rating = item.contents[0].text
                activity[rating_type] = rating
    except:
        print('Tag not found - pt2')
        return
        
    return activity

