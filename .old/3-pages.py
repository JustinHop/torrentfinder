#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from warnings import warn
# import json
# import yaml
from time import sleep

link = "http://kickass.to/tv/"
cellMainLink = {}
cellMainLink['class'] = "cellMainLink"
pageNextButton = {}
pageNextButton['class'] = "turnoverButton"


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
        count = 1
        pageno = 2
        pageend = 10

        s = BeautifulSoup(self.driver.page_source)
        r = re.compile(r'^magnet.*')
        pageend = pageend + 2

        while pageno < pageend:
            for a in s.find_all('a', href=r):
                if a:
                    td = a.findParent('td')
                    ta = td.find_all('a', attrs=cellMainLink)

                    torrent = {}
                    torrent['title'] = ""
                    torrent['url'] = a['href']
                    torrent['page'] = pageno - 1
                    torrent['number'] = count
                    count = count + 1

                    for tata in ta:
                        torrent['title'] = tata.text

                    torrents.append(torrent)
            next_page_elem = self.driver.find_element_by_link_text(str(pageno))

            if next_page_elem:
                next_page_elem.click()
                pageno = pageno + 1
                sleep(1)
            else:
                break

        return torrents


def main():
    scraper = GetKatTV()
    scraper.scrape()


if __name__ == "__main__":
    main()
