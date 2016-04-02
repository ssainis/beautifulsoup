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
            type_ac_u=unicode(type_ac)
            if type_ac_u.encode('ascii','replace') == 'Saab 2000AEW':
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
for i in range(57):
    next_url = generate_url(url_root,url_tail,i*100)
    url_list.append(next_url)
    
i = 1
records = [] 

for url_name in url_list:
#   time.sleep(random.randint(1, 10))   
    records[len(records):] = read_table_from_page(url_name)
    print i
    i = i+1

fname = 'output_saab.csv'
store_table_into_txt_File(records,fname)

#%% time
time_array = []
import datetime 
i = 0 
for row in records :
    time_records = row[3]
    time_records = unicode(time_records)
    time_records = time_records.encode('ascii','replace')
    out = datetime.datetime.strptime(time_records, " %Y-%m-%d %H:%M:%S") 
    time_array.append(out)

diff_hrs = []        
for i in range(1,len(time_array)):
        time_diff = time_array[i-1] - time_array[i]
        diff_hrs.append(time_diff.days*24 + time_diff.seconds/3600.0)
        
        
import matplotlib.pyplot as plt
import numpy as np
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
bins = np.linspace(0,300,100)
plt.hist(diff_hrs, bins, alpha = 0.5)
plt.title("PAF Saab 200AEW ADS B")
plt.xlabel("Time between flights in hours")
plt.ylabel("Number of flights")

fig = plt.gcf()