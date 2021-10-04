import xlrd
import openpyxl
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert 
from PIL import Image
import time
import csv
import re
import sys
import datetime
import string
import os
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0


nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-')
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--disable-images')
chrome_options.add_argument('--start-maximized')
chrome_options.add_extension(os.path.join(sys.path[0], 'plugin', 'sellersprite-amazon-resea.crx'))
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get('https://www.amazon.com/?currency=USD&language=en_US')
time.sleep(1)

thridNodeInfo = {}
linke = [
'https://www.amazon.com/Best-Sellers-Sports-Outdoors-Boating-Sailing/zgbs/sporting-goods/3421331/ref=zg_bs_nav_sg_2_10971181011',
'https://www.amazon.com/Best-Sellers-Sports-Outdoors-Fitness-Clothing/zgbs/sporting-goods/11444071011/ref=zg_bs_nav_sg_2_10971181011',
'https://www.amazon.com/Best-Sellers-Sports-Outdoors-Exercise-Fitness-Equipment/zgbs/sporting-goods/3407731/ref=zg_bs_nav_sg_2_10971181011'
]

for i in linke:
    driver.get(i)
    
    for num in range(1,51):
        tmppath = '//*[@id="zg-ordered-list"]/li['+str(num)+']/span/div/div/span[1]/span'
        driver.find_element_by_xpath(tmppath).location_once_scrolled_into_view
        time.sleep(1)
    for num in range(1,51):
        asinpath = '//*[@id="zg-ordered-list"]/li['+str(num)+']/span/div/span/div[3]/div/div[1]/span[1]'
        driver.find_element_by_xpath(asinpath).location_once_scrolled_into_view
        # brandpath = '//*[@id="zg-ordered-list"]/li['+str(num)+']/span/div/span/div[3]/div/div[2]/div[1]'
        sellerpath = '//*[@id="zg-ordered-list"]/li['+str(num)+']/span/div/span/div[3]/div/div[2]/div[2]/span'
        varpath = '//*[@id="zg-ordered-list"]/li['+str(num)+']/span/div/span/div[3]/div/div[2]/div[9]'
        datepath = '//*[@id="zg-ordered-list"]/li['+str(num)+']/span/div/span/div[3]/div/div[2]/div[6]/span/span'
        ASIN = driver.find_element_by_xpath(asinpath).text
        # BRAND = driver.find_element_by_xpath(brandpath).text
        SELLER = driver.find_element_by_xpath(sellerpath).text
        VARS = driver.find_element_by_xpath(varpath).text
        DATES = driver.find_element_by_xpath(datepath).text

        print(ASIN,SELLER,VARS,DATES)

