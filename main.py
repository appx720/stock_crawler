# Copyright (c) 2022 yeongjun hwang, Github : yeongjun0807, Email : yeongjun0807@gmail.com
# MIT License
# Crawler for korea stock (KOSPI) - load data and save them in csv file
# ver. Beta

import os
import pandas as pd # for save csv file and analyze data
from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions() # add options
options.add_argument("headless") # invisible window
options.add_argument("disable-gpu") # avoid bugs
url = "https://finance.naver.com/sise/sise_market_sum.naver?&page=" # stock webpage url  (DO NOT EDIT)

browser = webdriver.Chrome("chromedriver", options = options)
browser.maximize_window() # maximize_window

print("waiting...")
browser.implicitly_wait(3) # wait for stability
browser.get(url)

# find unchecked checkboxes and uncheck
checkboxes = browser.find_elements(By.NAME, "fieldIds")

for checkbox in checkboxes:
    if checkbox.is_selected():
        checkbox.click() # uncheck

# check elements
item_select = ["거래량", "시가", "고가", "저가"] # DO NOT EDIT THIS KOREAN CODE!! ## TODO: English patch
#  trading volume, market price, high price, low price

for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, "..") # parent element
    label = parent.find_element(By.TAG_NAME, "label")

    if label.text in item_select:
        checkbox.click() # check

# click apply button
btn_apply = browser.find_element(By.XPATH, "//a[@href='javascript:fieldSubmit()']") # DO NOT EDIT THIS XPATH
btn_apply.click()

for i in range(1, 40): # repeat page
    # move page
    browser.get(url + str(i))

    # get data
    data_frame = pd.read_html(browser.page_source)[1]
    data_frame.dropna(axis = "index", how = "all", inplace = True) # if data don't exist in an entire row
    #                        row/column              apply
    data_frame.dropna(axis = "columns", how = "all", inplace = True) # if data don't exist in an entire column
    #data_frame.drop(["N"], axis = 1, inplace = True)

    if len(data_frame) == 0: # if no data
        break

    
    ## TODO: English patch, change save method

    # save file
    file_n = "stock.csv"

    if os.path.exists(file_n): # exclude header
        data_frame.to_csv(file_n, encoding = "utf-8-sig", index = False, mode = "a", header = False)
    
    else: # if file isn't exist, include header
        data_frame.to_csv(file_n, encoding = "utf-8-sig", index = False)

    print(f"Finished Page {i}")

browser.quit()
print("Finished Crawling")