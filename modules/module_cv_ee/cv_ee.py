import configparser
import os
import time
import mysql.connector
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
    html_page = urllib3.urlopen(url)
    soup = BeautifulSoup(html_page)
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))

    return links

os.system('color')
print(colored("One click job finder", 'blue', 'on_white', ['blink']))
print("http://www.gamma-intelligence.com")
# Getting IP address
#ip = "1.1.1.1"
ip = get('https://api.ipify.org').text
#ip = '0.0.0.0'
print(colored(("Public IP address is: " + ip),"green"))

config = configparser.ConfigParser()
file = ["config.ini"]
datainput = config.read(file)

if len(datainput) != len(file):
    raise ValueError("Failed to find file")
else:
    print(colored("Config file is ready to use", "green"))

print("Version:" + config['general']['version'] + " Release date: "+ config['general']['lastrelease'])

host = config['mysqlDB']['host']
port = config['mysqlDB']['port']
usr = config['mysqlDB']['user']
#pas = config['mysqlDB']['pass']
db = config['mysqlDB']['db']
#auth = config['mysqlDB']['auth_plugin']
#mysql_table = config['mysql_table']['table']
position_storing_table = config['mysql_table']['table']
position_select_query = config['mysql_table']['position_select_query']
main_url = config['Link']['link']
print(main_url)
pause = config['pause']["value"]
version = config['general']['version']

config = {

    'user': "" + usr + "",
    #'password': "" + pas + "",
    'host': "" + host + "",
    'port': "" + port + "",
    'database': "" + db + "",
    #'auth_plugin': "" + auth + "",
    'raise_on_warnings': True,
}
options = Options()
options.headless = False
_browser_profile = webdriver.FirefoxProfile()
_browser_profile.set_preference("dom.webnotifications.enabled", False)
#_browser_profile.set_preference("general.useragent.override", "Gamma Intelligence Web Crawler")

driver = webdriver.Firefox(_browser_profile, options=options)
driver.maximize_window()
#driver.h

link = mysql.connector.connect(**config)
crawler_start_time = datetime.now()
print(crawler_start_time)

while True:
    cursor = link.cursor(buffered=True)
    if link.is_connected():
        a = 1
        #print(colored("MySQL conection alive","green"))
    else:
        print(colored("MySQL connection failed","red"))

    #Executing query with highest priority
    try:
        cursor.execute(position_select_query)
        row = cursor.fetchone()[0]
        driver.get(row)
    except:
        cursor.execute(select_query_low)
        row = cursor.fetchone()[0]
        driver.get(main_url + str(row))

    #Marking automatically selected record as reserved (status=2)
    print(colored(row, "green"))
    #cursor.execute("UPDATE city24_pool SET checked=2 WHERE page_id=" + str(row))
    link.commit()

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    #company_name = soup.find("div", {"class": "accordion-inner"})
    page_source=soup.find("div", {"class": "itemTitleColumnLeft"})

    if str(page_source) != 'None':
        # -----Parsing the existing page objects------#
        print("********************")
        #--Type--
        type = cleanhtml(str(soup.find("div",  {"class": "itemTitleColumnLeft"}).h1.span))
        print(type)
        update_stmt = "UPDATE crawler_1_data SET status=1, date_requested=NOW(), ip='" + ip + "' where url='" + str(row) + "'"
        cursor.execute(update_stmt)
        link.commit()
        print(colored("Position " + str(row) + " inserted successfully", "green"))
        #pause

    else:
        update_stmt = "UPDATE crawler_1_data SET status=1, date_requested=NOW(), ip='" + ip + "' where url='" + str(row) + "'"
        cursor.execute(update_stmt)
        link.commit()
        continue

    ##End of inserting the company data
    #driver.back()
    time.sleep(int(pause))
    #driver.close()
print("Crawler alive time:" + str((datetime.now()-crawler_start_time)))