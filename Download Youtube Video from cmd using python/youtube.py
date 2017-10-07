from bs4 import BeautifulSoup
import requests
import json
import selenium
import argparse
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
import sys
import os
from getpass import getuser
from time import time, sleep
from colorama import Fore, Style
from colorama import init
init()


def progressBar(length):
    show = ''
    for i in range(length):
        show += "#"
    for j in range(30-length):
        show += "-"
    show = "|"+show+"|"
    if length != 30:
        if length % 3 == 0:
            show = "/ " + show
        elif length % 3 == 1:
            show = "- " + show
        else:
            show = "\ " + show
    return show

# ================================Transfer Speed Function=================


def transferRate(blocksize):
    try:
        global speed, rate, transferData
        interval = time() - rate
        if rate == 0:
            transferData += blocksize
            rate = time()
        elif interval == 0 or interval < 1:
            transferData += blocksize
        else:
            speed = float(transferData/(interval))
            transferData = 0
            rate = time()
        return speed
    except Exception:
        pass

# ================================Type of Data============================


def dataSize(block):
    if block/1024 < 1000:
        block = block/1024
        sizeType = 'KB'
    elif block/1048576 < 1000:
        block = block/1048576
        sizeType = 'MB'
    elif block/1073741824 < 1000:
        block = block/1073741824
        sizeType = 'GB'
    return block, sizeType

# ================================Main Integrating function===============


def reporthook(blocknum, blocksize, total):
    size = 0
    currentType = ''
    length = 30
    percentage = 100.00
    global speed, speedType, totalsize, sizeType
    desc = int(blocknum*blocksize)
    if total > 0:
        length = int((desc/total)*30)
        percentage = float(desc/total*100)
    speed = transferRate(blocksize)
    speedShow, speedType = dataSize(speed)
    if totalsize == 0:
        totalsize, sizeType = dataSize(total)
    size, currentType = dataSize(desc)
    progress = progressBar(length)

    if percentage > 100:
        percentage = 100
        size = totalsize
    elif percentage == 100 and total < 0:
        totalsize = size
    p1 = " %.2f %%" % (percentage)
    p2 = " %s" % (progress)
    p3 = " %.2f %s / %.2f %s %.2f %s/s   " % (
        size, currentType, totalsize, sizeType, speedShow, speedType)
    sys.stderr.write("\r" +
                     p1 + Fore.GREEN + p2 + Style.RESET_ALL + p3 + Style.RESET_ALL)
    sys.stderr.flush()

# =====================================Globar Variables===================

argv = sys.argv[1:]
url = ''
name = 'default'
opts = ''
args = ''
rate = 0
speed = 0
transferData = 0
totalsize = 0
speedType = ''
sizeType = ''
flag = 0




url = input("Enter the Youtube-url\n")
name = input("Enter the name for the video\n")
name = name+".mp4"
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
    shURL = driver.find_element_by_xpath(
        '//input[@id="sf_url" and @type="text"]')
    shURL.send_keys(url)
    sleep(2)
    shSubmit = driver.find_element_by_xpath(
        '//button[@id="sf_submit" and @class="submit" and @name="sf_submit"]')
    shSubmit.click()
    sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    click = soup.find(
        "a", class_="link link-download subname ga_track_events download-icon")
    url_parse = click.get("href")
    driver.quit()
    print("Downloading Starts..\n")
    with open(name, 'wb') as out_file:
        with urlopen(url_parse) as fp:
            x = int(fp.info()['Content-Length'])
            i=1
            block_size = 1024 * 8
            while True:
                block = fp.read(block_size)
                reporthook(i,block_size,x)
                i+=1
                if not block:
                    break
                out_file.write(block)
    sys.stdout.write("\a")
    print("\nDownload Completed..!!!")
except Exception as e:
    print(e)
