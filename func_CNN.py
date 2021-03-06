import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

def get_CNN(name, day=7, out_put=False):

    url = f'https://www.cnn.com/search/?size=10&q={name}&category=business'
    
    #set chrome driver to headerless
    option_ = Options()
    option_.add_argument('--headless')
    
    #create driver to scrape
    driver = webdriver.Chrome(chrome_options=option_)
    driver.implicitly_wait(0.01)
    driver.get(url)
    
    # Wait maximum 120 seconds for page to load the need elements
    timeout = 120
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//h3[@class='cnn-search__result-headline']")))
    except TimeoutException:
        print('Timed out waiting for page to load')
        return ''

    # find_elements_by_xpath/or _by_tag_name returns an array of selenium objects.
    h3_elements = driver.find_elements_by_tag_name("h3")

    #find a tag with h3 tag
    #get links from a_tag uneder h3 tags
    list_links = []
    for h3_element in h3_elements:
        try:
            #print(h3_element.find_element_by_tag_name('span').text)
            list_links.append(h3_element.find_element_by_tag_name("a").get_attribute('href'))
        except:
            continue

    #close web_driver
    driver.quit()
    
    #use request here for performence ot practice selenium
    #pratice selenium + multiprocess 

    ####get article from list_links####

    #failure list
    list_fail_link = []
    #article text
    text = ''

    #get articles from the list_links
    for i_link in list_links:
        #set chrome driver to headerless
        option_ = Options()
        option_.add_argument('--headless')
        
        #create driver to scrape
        driver = webdriver.Chrome(chrome_options=option_)
        driver.get(i_link)
        
        # Wait x seconds for page to load the need elements
        timeout = 8
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='zn-body__paragraph']")))
        except TimeoutException:
            print('Timed out waiting for page to load')
            list_fail_link.append(i_link)
            continue
    
        p_elements = driver.find_elements_by_class_name("zn-body__paragraph")
        #get article and coleect all into var:text
        for p_element in p_elements:
            try:
                text = text + ' ' +  str(p_element.text)
            except:
                continue
        
        #clease driver
        driver.quit()

    

    if out_put:
        with open(f'{name}_CNN_result.txt', 'w') as fp:
            fp.write(text)

    return text

#print(get_CNN('apple'))
