
import requests
from bs4 import BeautifulSoup
import smtplib
import time
import csv
import re
import sys
from selenium import webdriver
import os
import pandas as pd

pws = os.getcwd()
chromedriver = pws+'/chromedriver'

headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.com'
    }

site = "https://www.99acres.com/search/property/buy/maharashtra?city=223&keyword=Maharashtra&preference=S&area_unit=1&budget_min=0&res_com=R"
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(chromedriver, chrome_options=options)
# get source code
driver.get(site)
html = driver.page_source
soup = BeautifulSoup(html)
r1 = soup.select_one('.Pagination__srpPagination')
pages = r1.findAll("div", {"class":"Pagination__srpPageBubble"})
pages1 = r1.find_all('a')

for page in range(1,len(pages1)):
    site = "https://www.99acres.com/property-in-maharashtra-5-lakhs-to-5-lakhs-ffid-page-" + str(page) 
    print("=========site",site)
    new_cdf =  pd.read_csv('cool.csv')
    column_name = list(new_cdf.columns)
    df = pd.DataFrame(columns = column_name)
    properties = soup.findAll("div", {"class":"srpTuple__tupleDetails"})
    for propertie in properties:
        name = propertie.select_one('.srpTuple__propertyName').getText()
        images = propertie.select_one('.srpTuple__photonImgSec')
        if images:
            image_url = images.img['src']
        description = propertie.select_one('#srp_tuple_description').getText()
        address = propertie.select_one('#srp_tuple_property_title').getText().replace("\n", "")
        price = propertie.select_one('#srp_tuple_price').getText()
        try:
            badroom = propertie.select_one('#srp_tuple_bedroom').getText()
        except:
            badroom = ''
        try:
            bathroom = propertie.select_one('#srp_tuple_bathroom').getText()
        except:
            bathroom = ''
        mydict = {
            'image' : image_url,
            'name' : name , 
            'address' : address,
            'description' : description, 
            'price' : price,  
            'badroom' : badroom,  
            'bathroom' : bathroom,
            }
        print("dict---===",len(mydict))
    # df = pd.DataFrame(mydict)
    #     # df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings}) 
    # df.to_csv('products.csv', index=False, encoding='utf-8')
        # writer = pd.ExcelWriter('pandas_simple.xlsx')
        # df.to_excel(writer,'Sheet1')
        # writer.save()
        df = df.append(mydict, ignore_index=True)
        df.to_csv('acress.csv', encoding='utf-8', index=False)
driver.close() 
