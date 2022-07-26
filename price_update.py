from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from send2trash import send2trash
from itertools import combinations
from itertools import product
from collections import defaultdict
import unicodedata
from datetime import datetime 
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://0e0c55ie39.execute-api.eu-central-1.amazonaws.com/default/fplAnalytics-DownloadPlayerStatusData")

time.sleep(10)

df = pd.read_csv (r'/Users/jordandass/Downloads/fplAnalytics-playerStautsData.csv')

send2trash(r'/Users/jordandass/Downloads/fplAnalytics-playerStautsData.csv')

name_list = []
cost_list = []
total_points_list = []
position_list = []
ppg_list = []
team_list = []
points_cost_list = []
clean_name_list = []

time_now = re.findall('[0-9]{4}-[0-9]+-[0-9]+', str(datetime.now()))[0]

def strip_accents(s):
       return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

for num in range(len(df)):
    if int(df.iloc[num, 6]) != 0:
        if str(df.iloc[num, 4]) != 'NotAvail':
            name_list.append(df.iloc[num, 0])
            cost_list.append(df.iloc[num, 3])
            total_points_list.append(df.iloc[num, 6])
            position_list.append(df.iloc[num, 2])
            ppg_list.append(df.iloc[num, 8])
            team_list.append(df.iloc[num, 1])
            points_cost_list.append(format(float(df.iloc[num, 6])/float(df.iloc[num, 3]),'.2f'))
            clean_name_list.append(strip_accents(str(df.iloc[num, 0]).lower()))
            
            
prices_df = pd.read_csv('prices.csv')
cost_list_ = []
for player in list(prices_df['Players']):
    cost_list_.append(list(df[df["name"] == player]["cost"])[0])
if list(prices_df.iloc[:,-1]) != cost_list_ or time_now in list(prices_df.columns):
    prices_df[time_now] = cost_list_
    prices_df.to_csv('prices.csv', index = False)


driver.quit()