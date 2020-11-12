import configparser
import os
import time
import mysql.connector
import re
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

os.system('color')
#Set start clean mode True only if you would like to rebuild all links
start_clean_mode = True
print(colored("One click job finder", 'blue', 'on_white', ['blink']))
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
pas = config['mysqlDB']['pass']
db = config['mysqlDB']['db']
#auth = config['mysqlDB']['auth_plugin']
#mysql_table = config['mysql_table']['table']
position_storing_table = config['mysql_table']['table']
position_select_query = config['mysql_table']['position_select_query']
order = config['mysql_table']['select_order']
main_url = config['Link']['link']
print(main_url)
pause = config['pause']["value"]

config = {
    'user': "" + usr + "",
    'password': "" + pas + "",
    'host': "" + host + "",
    'port': "" + port + "",
    'database': "" + db + "",
    #'auth_plugin': "" + auth + "",
    'raise_on_warnings': True,
}
print(config)
options = Options()
options.headless = False
_browser_profile = webdriver.FirefoxProfile()
_browser_profile.set_preference("dom.webnotifications.enabled", False)
#_browser_profile.set_preference("general.useragent.override", "Here is your browser")

driver = webdriver.Firefox(_browser_profile, options=options)
driver.maximize_window()

link = mysql.connector.connect(**config)
crawler_start_time = datetime.now()
print(crawler_start_time)

cursor = link.cursor(buffered=True)

if (start_clean_mode == True):
    all_urls = getLinks(main_url)
    regexp = re.compile("/vacancy/[0-9]+")
    # Getting only unique URLs
    # TODO: refactor as this method could use sometimes a lot of memory
    unique_urls = set(all_urls)
    for x in unique_urls:
        if regexp.search(x):
            result = regexp.search(x)
            sql_query="REPLACE INTO project_schema.crawler_1_data (url,raw_html_data," \
                      "plain_position_description,details,highlights,company,deadline) " \
                      "VALUES ('https://www.cv.ee" + result.group(0) \
                      + "','Empty','Empty','Empty','Empty','Empty','Empty')"
            cursor.execute(sql_query)

#Starting the parsing

query = position_select_query + ' ' + order
print(query)

#Starting the query cycle
while True:
    cursor.execute(query)
    url = cursor.fetchone()[0]
    print(url)
    driver.get(url)
    #elem = driver.find_element_by_xpath("//*")
    #source_code = elem.get_attribute("outerHTML")
    time.sleep(2)
    description = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/header[2]/div/div[2]/h2').text
    print(description)
    company = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/header[2]/div/div[2]/h2/span').text
    print(company)

    position = str(description).replace(company,"")
    print(position)

    tabs1 = driver.find_elements_by_class_name("react-tabs__tab")
    #print(len(tabs1))
    time.sleep(2)
    tabs1[0].click()
    #print(driver.find_element_by_css_selector('span.react-tabs[role="tabpanel"]'))
    details = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[1]').text
    details = str(details).replace("'","")
    details = str(details).replace('"', "")
    time.sleep(2)
    tabs1[1].click()
    primary_info = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[1]').text
    print(primary_info)
    time.sleep(2)
    tabs1[2].click()

    company_info = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[1]').text
    print(company_info)
    deadline = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/aside/div[1]/div/div/div/div[1]/span/span').text
    print(deadline)
    update_query="UPDATE `project_schema`.`crawler_1_data` SET plain_position_description = '" + position \
                 + "',details = '" + details + "',company = '" + company + "',deadline = '" + deadline \
                 + "', status = 1, date_requested=CURRENT_TIMESTAMP WHERE url='" + url + "'"
    print(update_query)
    cursor.execute(update_query)
    link.commit()


