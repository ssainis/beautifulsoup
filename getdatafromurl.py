# -*- coding: utf-8 -*-
"""
Created on Mon Feb 01 11:12:06 2016

@author: ssainis
"""

# download data from http://www.live-military-mode-s.eu/history2.php?start=100&DGCountry=IN
# there are 1000 entries - so start at 1 and go to 
# usign Beautiful Soup
from bs4 import BeautifulSoup
import urllib2
# import time
import random
import csv

#%% Function list 
def generate_url(url_root,url_tail,i):
    req = url_root + str(i) + url_tail
    return(req)

def read_table_from_page(req):
    response = urllib2.urlopen(req)
    the_page = response.read()
    
    soup = BeautifulSoup(the_page)
    
    tabul = soup.find_all("table",{"width":"100%"})
    
    records = [] # store all of the records in this list
    for tabulka in tabul:
        for row in tabulka.findAll('tr'):
            col = row.findAll('td')
            mode_s = col[1].string
            serial = col[2].string
            callsign = col[4].string
            gmt_time = col[5].string
            type_ac = col[6].string
            country = col[7].string
            operator = col[8].string 
            altitude = col[11].string
            record = [mode_s, serial, callsign, gmt_time, type_ac, country, operator, altitude]
            records.append(record)
    return (records)

def store_table_into_txt_File(records,fname):
    fl = open(fname, 'wb')
    out = csv.writer(fl, delimiter=',', quoting=csv.QUOTE_ALL)
    for row in records:
        data_line = convert_unicode_to_ascii(row)
        out.writerow(data_line)
    fl.close()

def convert_unicode_to_ascii(row):
    data_line = []    
    for entry in row:
        if type(entry) != 'NoneType':        
            entry = unicode(entry)        
            data_line.append(entry.encode('ascii','replace'))
    return(data_line)            
#%% Main 

url_root = 'http://www.live-military-mode-s.eu/history2.php?start='
url_tail = '&DGCountry=IN'
url_list = []
for i in range(1000):
    next_url = generate_url(url_root,url_tail,i*100)
    url_list.append(next_url)
    
i = 1
for url_name in url_list:
    records = [] 
#   time.sleep(random.randint(1, 10))   
    records[len(records):] = read_table_from_page(url_name)
    print i
    fname = 'output_'+str(i)+'.csv'
    store_table_into_txt_File(records,fname)
    i = i+1


