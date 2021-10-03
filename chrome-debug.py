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



rootPath = '//*[@id="zg_browseRoot"]/ul/li/span'
driver.get('https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods/')

# # get second node num
print('\nProgram was begin, now time: ' + str(nowTime))

secPath = '//*[@id="zg_browseRoot"]/ul/ul'
secNum = len(driver.find_element_by_xpath(secPath).find_elements_by_xpath('li'))


def ifElementExist(ifExits):
    try:
        driver.find_element_by_xpath(ifExits)
        return True
    except:
        return False


# get second node a tag

secondNodeInfo = {}
thridNodeInfo = {}
finalListInfo = {}

# # loop second node
for secNode in range(secNum, secNum+1):
    secNodePath = '//*[@id="zg_browseRoot"]/ul/ul/li[' + str(secNode) + ']/a'
    secondLink = driver.find_element_by_xpath(secNodePath).get_attribute("href")
    secondname = driver.find_element_by_xpath(secNodePath).text
    secondNodeInfo[secondname] = secondLink


for k,v in secondNodeInfo.items():
    driver.get(v)
    # get three node info
    thridPath = '//*[@id="zg_browseRoot"]/ul/ul/ul'
    thridNum = len(driver.find_element_by_xpath(thridPath).find_elements_by_xpath('li'))

    for thridNode in range (thridNum, thridNum+1):
        thridNodePath = '//*[@id="zg_browseRoot"]/ul/ul/ul/li[' + str(thridNode) + ']/a'
        if ifElementExist(thridNodePath):  # check dog page exits
            thridLink = driver.find_element_by_xpath(thridNodePath).get_attribute("href")
            thridname = driver.find_element_by_xpath(thridNodePath).text
            if thridLink not in thridNodeInfo:
                thridNodeInfo[thridLink] = [0,0]
            thridNodeInfo[thridLink][0] = k
            thridNodeInfo[thridLink][1] = thridname


for k,v in thridNodeInfo.items():

    linkName = k
    secName = v[0]
    thridName = v[1]
    driver.get(linkName)
    allproduct = driver.find_element_by_id('zg-ordered-list')
    allproducts = len(allproduct.find_elements_by_xpath('li'))
    # for page 1 and page 2
    for pages in range(1,3):
        # need modify
        for item in range (1,allproducts + 1):
            itemPath =    '//*[@id="zg-ordered-list"]/li[' + str(item) + ']/span/div/span/a'
            nodeNumPath = '//*[@id="zg-ordered-list"]/li[' + str(item) + ']/span/div/div/span[1]/span'
            if ifElementExist(itemPath):
                driver.find_element_by_xpath(itemPath).location_once_scrolled_into_view
                links = driver.find_element_by_xpath(itemPath).get_attribute("href")
                nodeNum = driver.find_element_by_xpath(nodeNumPath).text

                if links not in finalListInfo:
                    finalListInfo[links] = [0,0]
                    # index 0 == second node, index 1 == thrid node
                finalListInfo[links][0] = secName
                finalListInfo[links][1] = thridName+nodeNum

        # change pages
        # if pages == 1:
        #     nextPagePath = '//*[@id="zg-center-div"]/div[2]/div/ul/li[3]/a'
        #     if ifElementExist(nextPagePath):
        #         driver.find_element_by_xpath(nextPagePath).location_once_scrolled_into_view
        #         driver.find_element_by_xpath(nextPagePath).click()

saveInfoData = {}


pf1 = pd.DataFrame(finalListInfo)
pf1 = pd.DataFrame(pf1.values.T, index= pf1.columns, columns=pf1.index)
filepath = os.path.join(sys.path[0], 'output', 'all-link-for-'+nowTime+'.xlsx')
file_path1 = pd.ExcelWriter(filepath)
pf1.to_excel(file_path1,encoding='utf-8',index=True)
file_path1.save()

def getValue(tmpPath):
    try:
        values = driver.find_element_by_xpath(tmpPath).text
        return values
    except:
        return False

runNum = 0
for k,v in finalListInfo.items():

    runNum = runNum + 1
    print('Total have: '+ str(len(finalListInfo)) + ' link for loop. Now we checking: ' + str(runNum))

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


    driver.get(k)
    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, TOPNODEPATH)))
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, TOPNUMPATH)))

        TOPNUM = getValue(TOPNUMPATH).strip('#').strip(',')
        TOPNODE = getValue(TOPNODEPATH)
        if TOPNODE == 'Sports & Outdoors' and int(TOPNUM) <= 1000:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, ASINPATH)))
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, PRICEPATH)))
        
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
            REVIEW = (getValue(REVIEWPATH).split(' ',)[0]).replace(',','')
            QA = getValue(QAPATH).split(' ',)[0]
            PRICE = getValue(PRICEPATH)

            # print('asin: ', ASIN)
            # print('brand: ', BRAND)
            # print('SELLER: ', SELLER)
            # print('FBAFBM: ',FBAFBM)
            # print('FOLLOWSELLER: ',FOLLOWSELLER)
            # print('VARIANT: ',VARIANT)
            # print('DATE: ',DATE)
            # print('REVIEW: ',REVIEW)
            # print('QA: ',QA)
            # print('PRICE: ',PRICE)
            # print('TOPNUM: ',TOPNUM)
            # print('TOPNODE: ',TOPNODE)

            if ASIN not in saveInfoData.keys():
                saveInfoData[ASIN] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            saveInfoData[ASIN][2] = BRAND       # Brand
            saveInfoData[ASIN][1] = SELLER      # SELLER
            saveInfoData[ASIN][3] = FBAFBM      # Delivery
            saveInfoData[ASIN][4] = FOLLOWSELLER# Follow-up
            saveInfoData[ASIN][5] = VARIANT     # Variant
            saveInfoData[ASIN][6] = DATE        # Date First Available
            saveInfoData[ASIN][7] = REVIEW      # Reviews
            saveInfoData[ASIN][8] = QA          # QA
            saveInfoData[ASIN][9] = PRICE       # Price
            saveInfoData[ASIN][10] = TOPNUM      # First Node
            saveInfoData[ASIN][11] = TOPNODE    # First Rank
            saveInfoData[ASIN][15] = k          # Refer link
            saveInfoData[ASIN][12] = v[0]       # Sec node
            saveInfoData[ASIN][13] = v[1]       # Third node
            saveInfoData[ASIN][14] = nowTime    # Now time
    except:
        pass
    
header = [
    'ASIN', 'SELLER', 'Brand','Delivery', 'Follow-up', 'Variant', 'Date First Available', 'Reviews', 'QA', 'Price', 
    'First Rank','First Node','Sec Node', 'Third Node','Now Time', 'Refer Link' ]
pf = pd.DataFrame(saveInfoData)
# pf = pd.DataFrame(pf.values.T, index= pf.columns, columns=pf.index)
pf = pd.DataFrame(pf.values.T, index= pf.columns, columns=header)
filepath1 = os.path.join(sys.path[0], 'output', 'top1000-'+nowTime+'.xlsx')
file_path = pd.ExcelWriter(filepath1)
pf.to_excel(file_path,encoding='utf-8',index=True)
file_path.save()
finishTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-')
print(finishTime)