"""
@FileName：chengdu.py\n
@Description：机器学习\n
@Author：Surely\n
@Time： 2025 - 02 - 2025/2/1\n
"""
import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
import sys
import os
from selenium import webdriver
from collections import defaultdict
def flushprint(www):
    sys.stdout.write('\r')
    sys.stdout.write('%s' %www)
    sys.stdout.flush()

attr_score=pd.read_excel('beijing_score.xls')
review_content=[]

for index in range(0,1152):
    review_content_=[]
    url='https://www.tripadvisor.cn'+attr_score.iloc[index]['attr-link']
    attr_name=attr_score.iloc[index]['attr-name']
    attr_link=attr_score.iloc[index]['attr-link']
    score=attr_score.iloc[index]['score']
    review_num=attr_score.iloc[index]['review-num']
    review=[attr_name,attr_link,score,review_num]
    try:
        tt = random.random()
        flushprint(str(index)+':'+str(url)+':sleeping'+str(tt)+'seconds')
        time.sleep(tt)

        html=requests.get(url)
        html.encoding='utf-8'
        content=html.content
        soup=BeautifulSoup(content,'html.parser')
        try:
            if soup.select('.react-container .location-review-review-list-parts-ReviewFilters__filters_wrap--y1t86 .ui_columns .is-3-tablet .location-review-review-list-parts-ReviewFilter__filter_table--1H9KD .location-review-review-list-parts-LanguageFilter__taLnk--tu85q'):
                browser = webdriver.Chrome()
                browser.get(url)
                if browser.find_element_by_xpath('//*[@id="component_14"]/div[3]/div/div[1]/div[1]/div[4]/ul/div'):
                    browser.find_element_by_xpath('//*[@id="component_14"]/div[3]/div/div[1]/div[1]/div[4]/ul/div').click()
                elif browser.find_element_by_xpath('//*[@id="component_10"]/div[3]/div/div[1]/div[1]/div[4]/ul/div'):
                    browser.find_element_by_xpath('//*[@id="component_10"]/div[3]/div/div[1]/div[1]/div[4]/ul/div').click()
                elif browser.find_element_by_xpath('//*[@id="component_11"]/div[3]/div/div[1]/div[1]/div[4]/ul/div'):
                    browser.find_element_by_xpath('//*[@id="component_11"]/div[3]/div/div[1]/div[1]/div[4]/ul/div').click()
                elif browser.find_element_by_xpath('//*[@id="component_12"]/div[3]/div/div[1]/div[1]/div[4]/ul/div'):
                    browser.find_element_by_xpath('//*[@id="component_12"]/div[3]/div/div[1]/div[1]/div[4]/ul/div').click()
                elif browser.find_element_by_xpath('//*[@id="component_13"]/div[3]/div/div[1]/div[1]/div[4]/ul/div'):
                    browser.find_element_by_xpath('//*[@id="component_13"]/div[3]/div/div[1]/div[1]/div[4]/ul/div').click()

                source=browser.page_source
                soup2=BeautifulSoup(source, 'html.parser')
                for item in soup2.select('._32oTjHgM ._1W5CRnVt ._2yzvbm49 .location-review-review-list-parts-ReviewFilter__filter_table--1H9KD .location-review-review-list-parts-ReviewFilter__filter_row--p0z3u .location-review-review-list-parts-ReviewFilter__row_label--1njtd'):
                    review_content_.append(item.text)
                review.append(review_content_)
                review_content.append(review)
                browser.close()
            else:
                for item in soup.select('.location-review-review-list-parts-ReviewFilters__filters_wrap--y1t86 .is-3-tablet .location-review-review-list-parts-ReviewFilter__filter_table--1H9KD .location-review-review-list-parts-ReviewFilter__filter_row--p0z3u .location-review-review-list-parts-LanguageFilter__row_label--3OR-8'):
                    review_content_.append(item.text)
                review.append(review_content_)
                review_content.append(review)
        except Exception as w:
            print(index,url,w)
            review_content_='NaN'
            review.append(review_content_)
            review_content.append(review)

    except Exception as e:
            print(index,url,e)
            continue
df=pd.DataFrame(review_content,columns=['attr-name','attr-link','score','review-num','review-content'])
df.to_excel('beijing_review.xls')