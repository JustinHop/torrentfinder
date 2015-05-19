#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from warnings import warn
# import json
# import yaml
# from time import sleep

link = "http://kickass.to/tv/"
cellMainLink = {}
cellMainLink['class'] = "cellMainLink"


class GetKatTV(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def scrape(self):
        torrents = self.scrape_kat_tv_torrents()
        for torrent in torrents:
            print(torrent)

        self.driver.quit()

    def scrape_kat_tv_torrents(self):
        self.driver.get(link)

        torrents = []
        pageno = 1

        s = BeautifulSoup(self.driver.page_source)
        # r = re.compile(r'^(https?://torcache\.net/.*\.torrent)\?(.*)?')
        r = re.compile(r'^magnet.*')

        for a in s.find_all('a', href=r):
            if a:
                td = a.findParent('td')
                ta = td.find_all('a', attrs=cellMainLink)

                torrent = {}
                torrent['title'] = ""
                torrent['url'] = a['href']
                # torrent['title'] = ta.get_text

                for tata in ta:
                    # print(tata)
                    torrent['title'] = tata.text

                torrents.append(torrent)
            else:
                print("a : not exist")

        pageno = pageno + 1
        return torrents


def main():
    scraper = GetKatTV()
    scraper.scrape()


if __name__ == "__main__":
    main()
