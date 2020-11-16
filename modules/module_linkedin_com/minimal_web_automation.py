import os
import time
import re
import pandas as pd
from requests import get
from decimal import *
from bs4 import BeautifulSoup
import urllib3
import urllib.request
from termcolor import colored
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def getLinks(url):
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, features="html.parser")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    return links

def getWorkLinks(url):
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, features="html.parser")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    return links

url = "https://www.linkedin.com"
print(url)

#options = Options()
#options.headless = False
#_browser_profile = webdriver.FirefoxProfile()
#_browser_profile.set_preference("dom.webnotifications.enabled", False)
#_browser_profile.set_preference("general.useragent.override", "Here is your browser")
#driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()
driver.maximize_window()
driver.get(url)
driver.find_element_by_class_name("nav__button-secondary").click()
driver.find_element_by_id("username").clear()
driver.find_element_by_id("username").send_keys("valera987653@RAMBLER.RU")
driver.find_element_by_id("password").clear()
driver.find_element_by_id("password").send_keys("244466666Valera")
driver.find_element_by_class_name("login__form_action_container ").click()
time.sleep(5)
#driver.find_element_by_class_name("global-nav__me-photo ghost-person ember-view")
if (driver.find_element_by_class_name('artdeco-button__icon') == True):
    driver.find_element_by_class_name('artdeco-button__icon').click()
time.sleep(2)
#print(driver.find_elements_by_class_name("global-nav__primary-link ember-view"))
driver.get("https://www.linkedin.com/jobs/")
#driver.find_element_by_id('global-nav-icon--mercado__jobs--active').click()
driver.find_element_by_class_name("jobs-search-box__text-input").clear()
driver.implicitly_wait(2)
driver.find_element_by_partial_link_text("Search").click()
#print(driver.current_url)
print(getWorkLinks(driver.current_url))



