from bs4 import BeautifulSoup
import requests
import urllib.request
import json
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


url = input("Enter the Youtube-url\n")
name = input("Enter the name for the video\n")
name=name+".mp4"
try:

    # Phantom JS

    driver = webdriver.PhantomJS(executable_path=r'C:\Users\ankit\Downloads\phantomjs-2.1.1-windows (1)\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.set_window_size(1120, 550)
    driver.get("http://en.savefrom.net")

    # FireFox

    # driver = webdriver.Firefox()
    # driver.get("http://en.savefrom.net")

    shURL = driver.find_element_by_xpath('//input[@id="sf_url" and @type="text"]')
    shURL.send_keys(url)
    time.sleep(2)
    shSubmit = driver.find_element_by_xpath('//button[@id="sf_submit" and @class="submit" and @name="sf_submit"]')
    shSubmit.click()
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    click = soup.find("a", class_="link link-download subname ga_track_events download-icon")
    url_parse = click.get("href")
    driver.quit()
    print("Downloading Starts..\n")
    # print(url_parse)
    urllib.request.urlretrieve(url_parse, name)
    print("Download Completed..!!!")
except Exception as e:
    print(e)
