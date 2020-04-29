# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 12:50:24 2020

@author: Aviral Gaur
"""
#importing libraries
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


#sample website
url = "https://www.creativeshrimp.com/top-30-artworks-of-beeple.html"
title_list =[]
height_list =[]
width_list =[]
source_code = requests.get(url)


#using beautifulsoup for scraping the title and dimensions of the image
plain_text = source_code.text
soup = bs(plain_text)

a_tags = soup.find_all("a",{"class":"lightbox"})

for link in a_tags:
    href = link.get("href")
    temp = link.find("img")
    temp = temp.get("src")
    title_list.append(href.split("/")[-1])
    if href == temp:
        img_tag = soup.find("img",{"src":href})
        height_list.append(img_tag.get("height")) 
        width_list.append(img_tag.get("width"))
    else:
        height_list.append("Not Available")
        width_list.append("Not available")
        
    
    print(href)
#converting the list into an accessible comma separated value file(csv)   
final_list = {'Title':title_list,'Height':height_list, 'Width':width_list}
df = pd.DataFrame(final_list)
df = df.transpose()
df.to_csv("list_1.csv")








