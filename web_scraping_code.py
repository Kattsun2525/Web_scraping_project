import pandas as pd
import numpy as np
import requests
import re
import lxml
import html5lib
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
from pandas import read_html as rh
from datetime import datetime as dt

# 1st step: Data collection (Web scraping)
# Get the first 100 rows of data
url_link = 'https://finance.yahoo.com/quote/NFLX/history?period1=1350777600&period2=1666310400&interval=1wk&filter=history&frequency=1wk&includeAdjustedClose=true'
r = requests.get(url_link,headers = {'User-Agent':'Mozilla/5.0'})
netflix_stock = pd.read_html(r.text)[0]

# Get the rest of data using a for loop
url_bef_num = 'https://finance.yahoo.com/quote/NFLX/history?period1=1350777600&period2='
url_aft_num = '&interval=1wk&filter=history&frequency=1wk&includeAdjustedClose=true'
num = 1666310400
for i in range(2,7):
    # For the second page of stock quotes, the number before '&interval' in the URL increases by 60220800
    if i == 2:
        num = num - 60220800
        print("i is 2")
    # For the fifth page of stock quotes, the number before '&interval' in the URL increases by 59875200
    elif i == 5:
        num = num - 59875200
        print("i is 5")
    # For the other n-th page of stock quotes, the number before '&interval' in the URL increases by 60480000
    else:
        num = num - 60480000
        print("i is else")
    
    url_link = url_bef_num + str(num) + url_aft_num
    r = requests.get(url_link,headers = {'User-Agent':'Mozilla/5.0'})
    print(url_link)
    netflix_stock = netflix_stock.append(pd.read_html(r.text)[0], ignore_index=True)
    
    
# 2nd step: Data Cleaning Steps
# Remove the following irrelevant rows
netflix_stock = netflix_stock.drop(netflix_stock.index[[100, 201, 302, 382, 403, 504, 528]])

# Change the date format for analysis
netflix_stock["Date2"] = [dt.strptime(i, "%b %d,  %Y") for i in netflix_stock["Date"]]
netflix_stock.set_index("Date2",inplace=True)

# Set the new date column to the index and drop the old date column
netflix_stock.set_index("Date2",inplace=True)
netflix_stock = netflix_stock.drop(labels="Date", axis=1)
netflix_stock.index.names = ['Date']



