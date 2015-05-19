#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import errno
from bs4 import BeautifulSoup

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from warnings import warn
import json
# import yaml
from time import sleep

link = "http://kickass.to/tv/"
cellMainLink = {}
cellMainLink['class'] = "cellMainLink"
pageNextButton = {}
pageNextButton['class'] = "turnoverButton"
configDirCacheFile = os.path.expanduser("~/.config/torrentfinder/cache.json")
configDir = os.path.dirname(configDirCacheFile)


class GetKatTV(object):
    def __init__(self):
        try:
            os.makedirs(configDir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        self.driver = webdriver.PhantomJS()
        self.torrents = []

    def scrape(self):
        self.torrents = self.scrape_kat_tv_torrents()
        self.cache_save()
        for torrent in self.torrents:
            print(torrent)

        self.driver.quit()

    def cache_save(self):
        try:
            with open(configDirCacheFile, 'w') as outfile:
                json.dump(self.torrents, outfile)
        except OSError:
            raise

    def scrape_kat_tv_torrents(self):
        self.driver.get(link)

        number = 1
        pageno = 2
        pageend = 100

        s = BeautifulSoup(self.driver.page_source)
        r = re.compile(r'^magnet.*')
        pageend = pageend + 2

        while pageno < pageend:
            print("Pages Processed: " + str(pageno - 2) +
                  ", Torrents Processed: " + str(number))
            for a in s.find_all('a', href=r):
                if a:
                    td = a.findParent('td')
                    tr = td.findParent('tr')
                    trs = tr.find_all('td')
                    ta = td.find_all('a', attrs=cellMainLink)

                    torrent = {}
                    torrent['title'] = ""
                    torrent['url'] = a['href']
                    torrent['page'] = int(pageno - 1)
                    torrent['number'] = int(number)
                    number = number + 1

                    torrent['size'] = trs[1].text
                    torrent['files'] = int(trs[2].text)
                    torrent['age'] = trs[3].text
                    torrent['age'] = torrent['age'].replace(u"&nbsp;", " ")
                    torrent['age'] = torrent['age'].replace(u"\xa0", " ")
                    torrent['seed'] = int(trs[4].text)
                    torrent['leech'] = int(trs[5].text)

                    for tata in ta:
                        torrent['title'] = tata.text

                    self.torrents.append(torrent)
            next_page_elem = self.driver.find_element_by_link_text(str(pageno))

            if next_page_elem:
                try:
                    next_page_elem.click()
                except:
                    break
                pageno = pageno + 1
                sleep(1)
            else:
                break

        return self.torrents


def main():
    scraper = GetKatTV()
    scraper.scrape()


if __name__ == "__main__":
    main()
