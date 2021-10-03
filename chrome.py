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
chrome_options.add_extension('C:\\Users\\Administrator\\Desktop\\get-TOP100\\lnbmbgocenenhhhdojdielgnmeflbnfb\\sellersprite-amazon-resea.crx')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get('https://www.amazon.com/?currency=USD&language=en_US')
time.sleep(1)

thridNodeInfo = {}
linke = [
'https://www.amazon.com/Modvel-Compression-Knee-Sleeve-Pair/dp/B079GGXJ63/ref=sr_1_1?dchild=1&keywords=B079GGXJ63&qid=1633245486&sr=8-1',
'https://www.amazon.com/BLUEENJOY-Compression-Socks-Athletic-Crossfit/dp/B07Q8WMNQR/ref=sr_1_1?dchild=1&keywords=B07Q8WMNQR&qid=1633245504&sr=8-1'
]

def ifElementExist(ifExits):
    try:
        driver.find_element_by_xpath(ifExits)
        return True
    except:
        return False
def getValue(tmpPath):
    try:
        values = driver.find_element_by_xpath(tmpPath).text
        return values
    except:
        return False
for link in linke:
    driver.get(link)
    ASINPATH = '//*[@id="sellersprite-extension-quick-view-listing"]/div/div[1]/span[1]'
    BRANDPATH = '//*[@id="sellersprite-extension-quick-view-listing"]/div/div[2]/div[1]/div[1]/span/a'
    SELLERPATH = '//*[@id="sellersprite-extension-quick-view-listing"]/div/div[2]/div[1]/div[2]/span/a[1]'
    FBAFBMPATH = '//*[@id="tabular-buybox-truncate-0"]/span[2]/span'
    FOLLOWSELLERPATH = '//*[@id="sellersprite-extension-quick-view-listing"]/div/div[2]/div[1]/div[2]/span/a[2]'
    VARIANTPATH = '//*[@id="sellersprite-extension-quick-view-listing"]/div/div[2]/div[5]/span[4]/span/span'
    # DATEPATH = '//*[@id="sellersprite-extension-quick-view-listing"]/div/div[2]/div[4]/div[2]/span/span'
    DATEPATH = '//*[@id="sellersprite-extension-quick-view-listing"]/div/div[2]/div[4]/div/span/span'
    # REVIEWPATH = '//*[@id="acrCustomerReviewText"]'
    REVIEWPATH = '//*[@id="averageCustomerReviews"]/span[3]'
    QAPATH = '//*[@id="askATFLink"]/span'
    PRICEPATH = '//*[@id="priceblock_ourprice"]'
    TOPNUMPATH = '//*[@id="sellersprite-extension-quick-view-listing"]/div/div[2]/div[2]/p[1]/span/span'
    TOPNODEPATH = '//*[@id="sellersprite-extension-quick-view-listing"]/div/div[2]/div[2]/p[1]/a'
    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, TOPNODEPATH)))
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, TOPNUMPATH)))

        TOPNUM = getValue(TOPNUMPATH).strip('#').strip(',')
        TOPNODE = getValue(TOPNODEPATH)
        if TOPNODE == 'Sports & Outdoors' and int(TOPNUM) <= 1000:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, ASINPATH)))
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, PRICEPATH)))
            # if ifElementExist(DATEPATH):
            #     print('11111111')
                
            # else:
            #     print('2222222')
            #     driver.refresh()
            #     WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, REVIEWPATH)))
            #     REVIEW = getValue(REVIEWPATH).split(' ',)[0].strip(',')
            #     print(type(REVIEW))
            REVIEW = (getValue(REVIEWPATH).split(' ',)[0]).replace(',','')
            print(type(REVIEW))
            
            # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, DATEPATH)))
            # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, REVIEWPATH)))
        
            ASIN = getValue(ASINPATH).split(' ',)[-1]
            BRAND = getValue(BRANDPATH)
            SELLER = getValue(SELLERPATH)
            if getValue(FBAFBMPATH) == 'Amazon.com':
                FBAFBM = 'AMZ'
            elif getValue(FBAFBMPATH) == 'Amazon':
                FBAFBM = 'FBA'
            else:
                FBAFBM = 'FBM'
            FOLLOWSELLER = getValue(FOLLOWSELLERPATH).split(' ',)[-1]
            VARIANT = getValue(VARIANTPATH)
            DATE = getValue(DATEPATH)
            # REVIEW = getValue(REVIEWPATH)
            QA = getValue(QAPATH)
            PRICE = getValue(PRICEPATH)

            print('asin: ', ASIN)
            print('brand: ', BRAND)
            print('SELLER: ', SELLER)
            print('FBAFBM: ',FBAFBM)
            print('FOLLOWSELLER: ',FOLLOWSELLER)
            print('VARIANT: ',VARIANT)
            print('DATE: ',DATE)
            print('REVIEW: ',REVIEW)
            print('QA: ',QA)
            print('PRICE: ',PRICE)
            print('TOPNUM: ',TOPNUM)
            print('TOPNODE: ',TOPNODE)
            print('+++++++++++++++')
            # if ASIN not in saveInfoData.keys():
            #     saveInfoData[ASIN] = [0,0,0,0,0,0,0,0,0,0,0,0]
            # saveInfoData[ASIN][0] = BRAND
            # saveInfoData[ASIN][1] = SELLER
            # saveInfoData[ASIN][2] = FBAFBM
            # saveInfoData[ASIN][3] = FOLLOWSELLER
            # saveInfoData[ASIN][4] = VARIANT
            # saveInfoData[ASIN][5] = DATE
            # saveInfoData[ASIN][6] = REVIEW
            # saveInfoData[ASIN][7] = QA
            # saveInfoData[ASIN][8] = PRICE
            # saveInfoData[ASIN][9] = TOPNUM
            # saveInfoData[ASIN][10] = TOPNODE

    except:
        pass
    # finally:
    #     driver.quit()



    # allproductpath = '//*[@id="zg-ordered-list"]'
    # allnum = len(driver.find_element_by_xpath(allproductpath).find_elements_by_xpath('li'))

    # for i in range (1, allnum+1):
    #     print('\n',str(i), ' product')
    #     asinpath = '//*[@id="zg-ordered-list"]/li[' + str(i) + ']/span/div/span/div[3]/div/div[1]/span[1]'
    #     if ifElementExist(asinpath):
    #         driver.find_element_by_xpath(asinpath).location_once_scrolled_into_view
    #         ASIN = driver.find_element_by_xpath(asinpath).text
    #         # print('11111111111111111')
    #     else:
    #         try:
    #             print('11111111111111111')
    #             print(asinpath)
    #             WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, asinpath)))
    #             if ifElementExist(asinpath):
    #                 driver.find_element_by_xpath(asinpath).location_once_scrolled_into_view
    #                 ASIN = driver.find_element_by_xpath(asinpath).text
    #                 print('2222222222222222')
    #             else:
    #                 driver.refresh()
    #                 time.sleep(10)
    #                 ASIN = driver.find_element_by_xpath(asinpath).text
    #                 print('3333333333333333')
    #         except:
    #             pass
    #     print(ASIN)






    
        






