# Copyright (c) 2022 yeongjun hwang, Github : yeongjun0807, Email : yeongjun0807@gmail.com
# MIT License
# Crawler for korea stock (KOSPI, KOSDAQ) - load, analyze and save data in csv file
# ver. 0.0.1
# If you want to use this code, go to "https://data.go.kr", get key, make `key` file and put the key in it

import sys
import urllib3
import requests
import pandas as pd

def get_key():
   """get key from key file"""
   with open("key", "r") as f:
      k = f.read()
      return f"https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey={k}&numOfRows=10000&resultType=json" # stock webpage url (DO NOT EDIT)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Remove InsecureRequestWarning
url = get_key()

print("Crawling")

r = requests.get(url, verify = False)
raw_data = r.json() # first data (include both header and body)

if raw_data["response"]["header"]["resultCode"] == "00": # check status code
   print("Sucessful")

else:
   print("Failed")
   sys.exit() # quit program

data = raw_data["response"]["body"]["items"]["item"] # stock data (only body)

print("Analyzing")

df = pd.DataFrame(data)[["itmsNm", "vs", "fltRt", "mkp"]] # create new database -> for analyzing
df.rename(columns = {"itmsNm": "주식명", "vs": "증감", "fltRt": "증감률", "mkp": "현재가"}, inplace = True) # rename database

df["증감"] = df["증감"].astype(int) # ready to sort
df["증감률"] = df["증감률"].astype(float)

vs_sorted = df.sort_values(by = "증감", ascending = False) # sort data by increasing
fltRt_sorted = df.sort_values(by = "증감률", ascending = False) # sort data by change rate

n_df = pd.concat([vs_sorted.head(10), vs_sorted.tail(10), fltRt_sorted.head(10), fltRt_sorted.tail(10)]) # merge data -> for save in csv file

n_df.to_csv("stock.csv", encoding = "utf-8-sig", mode = "w", index = False) # save in csv file