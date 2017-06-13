from bs4 import BeautifulSoup
import requests
import json
import selenium
import argparse
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen
from getopt import GetoptError, getopt
import sys
import os
from getpass import getuser
from time import time, sleep
from colorama import Fore, Style
from colorama import init
init()


class Playlist:

    def __init__(self, total):

        self.rate = 0
        self.speed = 0
        self.transferData = 0
        self.total = total
        self.totalsize, self.sizetype = self.datasize(total)
        self.speedtype = ''
        self.flag = 0

# ================================Progress Bar Function===================

    def progressbar(self, length):
        show = ''
        for _ in range(length):
            show += "#"
        for _ in range(30 - length):
            show += "-"
        show = "|" + show + "|"
        if length != 30:
            if length % 3 == 0:
                show = "/ " + show
            elif length % 3 == 1:
                show = "- " + show
            else:
                show = "\ " + show
        return show

    # ================================Transfer Speed Function=================

    def transferrate(self, blocksize):
        try:
            interval = time() - self.rate
            if self.rate == 0:
                self.transferData += blocksize
                self.rate = time()
            elif interval == 0 or interval < 1:
                self.transferData += blocksize
            else:
                self.speed = float(self.transferData / (interval))
                self.transferData = 0
                self.rate = time()
            return self.speed
        except Exception:
            pass

    # ================================Type of Data============================

    def datasize(self, block):
        if block / 1024 < 1000:
            block = block / 1024
            sizetype = 'KB'
        elif block / 1048576 < 1000:
            block = block / 1048576
            sizetype = 'MB'
        elif block / 1073741824 < 1000:
            block = block / 1073741824
            sizetype = 'GB'
        return block, sizetype

    # ================================Main Integrating function===============

    def reporthook(self, blocknum, blocksize):
        size = 0
        currenttype = ''
        length = 30
        percentage = 100.00
        desc = int(blocknum * blocksize)
        if self.total > 0:
            length = int((desc / self.total) * 30)
            percentage = float(desc / self.total * 100)
        self.speed = self.transferrate(blocksize)
        speedShow, self.speedtype = self.datasize(self.speed)
        size, currenttype = self.datasize(desc)
        progress = self.progressbar(length)

        if percentage > 100:
            percentage = 100
            size = self.totalsize
        elif percentage == 100 and self.totalsize < 0:
            self.totalsize = size
        p1 = " %.2f %%" % (percentage)
        p2 = " %s" % (progress)
        p3 = " %.2f %s / %.2f %s %.2f %s/s   " % (
            size, currenttype,
            self.totalsize,
            self.sizetype,
            speedShow,
            self.speedtype
        )
        sys.stderr.write(
            "\r" + p1 + Fore.GREEN + p2 + Style.RESET_ALL + p3 +
            Style.RESET_ALL
        )
        sys.stderr.flush()


def main():

    # =====================================Globar Variables===================
    url = ''
    name = 'default'
    prefix = "https://www.youtube.com"
    opts = ''
    args = ''
    start = 0
    end = 0
    path = "playlist"
    # url = input("Enter the Youtube-url\n")
    # name = input("Enter the name for the video\n")
    # name = name + ".mp4"

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--url', nargs='?',
                        help="Complete download link of the playlist", type=str)
    parser.add_argument('-l', '--list', nargs='?',
                        help="List id of the playlist", type=str)
    parser.add_argument('-s', '--start', nargs='?',
                        help="Start no. of playlist", type=int)
    parser.add_argument('-e', '--end', nargs='?',
                        help="End no. of playlist", type=int)
    args = parser.parse_args()

    if args.url:
        url = args.url
    elif args.list:
        url = "https://www.youtube.com/playlist?list=" + args.list
    else:
        print(parser.parse_args(['--help']))

    if args.start:
        start = args.start - 1
    if args.end:
        end = args.end

    try:

        # Phantom JS

        driver = webdriver.PhantomJS(
            executable_path=r'C:\Users\ankit\Downloads\phantomjs-2.1.1-windows (1)\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        driver.set_window_size(1120, 550)

        # FireFox

        # binary = FirefoxBinary(
        #     'C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')
        # driver = webdriver.Firefox(firefox_binary=binary)
        # driver.set_window_size(1120, 550)

        driver.get(url)
        WebDriverWait(driver, 10000).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".pl-header-title")
            )
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        path = soup.find(
            "h1", class_="pl-header-title").string.replace('\n', '').replace(' ', '').replace(',', '').replace('.', '').replace(':', '')

        _urls = soup.find_all(
            "a", class_="pl-video-title-link")

        totalVideos = len(_urls)
        if end == 0:
            end = totalVideos

        print("There are total of " + str(totalVideos) + " Videos in the playlist")

        if not os.path.exists(path):
            os.system('mkdir %s' % path)

        for i in range(start, end):

            _url = _urls[i]

            _name = _url.string.replace('\n', '').replace(
                ' ', '').replace(',', '').replace('.', '').replace(':', '')

            _name += '.mp4'

            _url = prefix + _url.get("href")

            driver.get("http://en.savefrom.net")
            WebDriverWait(driver, 10000).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#sf_url")
                )
            )
            shURL = driver.find_element_by_xpath(
                '//input[@id="sf_url" and @type="text"]')
            shURL.send_keys(_url)

            WebDriverWait(driver, 10000).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#sf_submit")
                )
            )
            shSubmit = driver.find_element_by_xpath(
                '//button[@id="sf_submit" and @class="submit" and @name="sf_submit"]')
            shSubmit.click()

            WebDriverWait(driver, 10000).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     ".link.link-download.subname.ga_track_events.download-icon")
                )
            )
            # sleep(10)
            soupInner = BeautifulSoup(driver.page_source, 'html.parser')
            click = soupInner.find(
                "a", class_="link link-download subname ga_track_events download-icon")
            url_parse = click.get("href")
            print(str(i + 1) + "- Downloading " + _name)
            with open(path + "\\" + _name, 'wb') as out_file:
                with urlopen(url_parse) as fp:
                    info = fp.info()
                    if 'Content-Length' in info:
                        x = int(info['Content-Length'])
                    else:
                        x = -1
                    if x < 10000:
                        x = -1

                    i = 1
                    block_size = 1024 * 8
                    ob = Playlist(x)
                    while True:
                        block = fp.read(block_size)
                        ob.reporthook(i, block_size)
                        i += 1
                        if not block:
                            break
                        out_file.write(block)
            print("\n")
            print("Successfully download " + _name)
            sys.stdout.write("\a")
    except Exception as e:
        print(e)
    driver.quit()


if __name__ == '__main__':
    main()
