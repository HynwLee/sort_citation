# -*- coding: utf-8 -*-
# title: sort_citation.py
# author: Hyeonwoo Lee
# date created: 2020-04-23
# description:
# input: a text file(references)
# output: a sorted list of references wrt their numbers of citation 

before_sort = []
with open(r'D:\Hyeonwoo_Lee\SourceCodes\python\sort_citation\REFERENCES_INPUT_TEST.txt', 'r', encoding='utf-8') as f:
    before_sort.append( (f.readline())[:-1] + ' ')
    for line in f:
        if line[0] != '[':
            before_sort[-1] = before_sort[-1] + line[:-1] + ' '
        else:
            before_sort.append(line[:-1] + ' ')

print(len(before_sort))
print(before_sort)

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
path = 'D:\Hyeonwoo_Lee_Old\SourceCodes\python\SSA_WebCrawler\chromedriver.exe'

driver = webdriver.Chrome(path)

driver.get(r'https://scholar.google.com')
try:
    assert "Google" in driver.title
except AssertionError:
    print("Error: can't reach Google Scholar")

error_papers = []
for i in range(0, len(before_sort)):
    tmp = ''
    q= driver.find_element_by_xpath('//*[@id="gs_hdr_tsi"]')
    q.send_keys(before_sort[i][3:])
    q.send_keys(Keys.RETURN)
    # try~except, if there is selenium.common.exceptions.NoSuchElementException
    # then that paper is deleted form before_sort and goes into error_papers list
    try:
        tmp = driver.find_element_by_xpath('//*[@id="gs_res_ccl_mid"]/div/div[2]/div[3]/a[3]').text
    except selenium.common.exceptions.NoSuchElementException:
        print('selenium.common.exceptions.NoSuchElementException:.{}'.format(before_sort[i]))
        error_papers.append(before_sort[i])
        before_sort[i] = 'error #Cit:0'
    num_citation = ''
    for letter in tmp:
        if letter.isnumeric():
            num_citation = num_citation + letter
        else: 
            break
    before_sort[i] = before_sort[i] + '#Cit:' + num_citation
    q= driver.find_element_by_xpath('//*[@id="gs_hdr_tsi"]')
    q.clear()

# stage 3. sort the list. key is the # of citation.
after_sort = []
try:
    after_sort = sorted(before_sort, key = lambda x: int(x[x.index('#Cit:') + 5:]), reverse=True)
except ValueError:
    print("#cit: invalid literal for int() with base 10. Seems the program couldn't get the # of citation.")

with open(r'D:\Hyeonwoo_Lee\SourceCodes\python\sort_citation\REFERENCES_OUTPUT.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(after_sort))

print("Done!")



