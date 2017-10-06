from bs4 import BeautifulSoup
import subprocess
import os
import requests
import urllib.request
import json
import time
import argparse
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

url = input("Enter the URL\n")
name = input("Enter the video's name\n")
name += ".mp4"
n = name.split(' ')
name = "_".join(n)
print(name)
try:

    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--driver", type=str, default="phantomjs",
        help="which driver to use [option: phantomjs, firefox, chrome]")

    args = vars(ap.parse_args())
    choice = args["driver"]

    driver = ""
    if choice == "firefox":
        binary = FirefoxBinary('firefox')
        driver = webdriver.Firefox(firefox_binary=binary)
    elif choice == "chrome":
        driver = webdriver.Chrome();
    elif choice == "phantomjs":
        driver = webdriver.PhantomJS(
            executable_path=r'phantomjs')
    else:
        print("Invalid Choice");
        sys.exit(1);

    driver.set_window_size(1120, 550)

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
