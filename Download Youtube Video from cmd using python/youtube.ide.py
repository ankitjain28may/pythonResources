from bs4 import BeautifulSoup
import subprocess
import os
import requests
import urllib.request
import json
import time
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

url = input("Enter the Youtube-url\n")
name = input("Enter the name for the video\n")
name=name+".mp4"
n = name.split(' ')
name = "_".join(n)
print(name)
try:

    # Phantom JS

    driver = webdriver.PhantomJS(executable_path=r'C:\Users\ankit\Downloads\phantomjs-2.1.1-windows (1)\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.set_window_size(1120, 550)

    # FireFox

    # binary = FirefoxBinary('C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')
    # driver = webdriver.Firefox(firefox_binary=binary)

    driver.get("http://en.savefrom.net")
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
    path = os.getcwd()
    # print("Downloading Starts..\n")
    # print(url_parse)
    # urllib.request.urlretrieve(url_parse, name)


    installs = [
        'idman.exe /n /d ' + '"' + url_parse + '"' + ' /p ' + '"' + path + '"' + ' /f ' + '"' + name + '"' + ' /q',
    ]

    print("Wait for the Downloading, Its in progress..!!!")
    for install in installs:
        proc = subprocess.Popen(install, stdout=subprocess.PIPE)
        output, error = proc.communicate()
        if output!=None:
            print(output.decode('utf-8'))
        elif error!=None:
            print(error.decode('utf-8'))
except Exception as e:
    print(e)
