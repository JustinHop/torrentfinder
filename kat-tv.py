#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""torrentfinder

Usage:
    kat-tv.py update [options]
    kat-tv.py search [options]
    kat-tv.py show [options]
    kat-tv.py html [options]
    kat-tv.py csv [options]
    kat-tv.py status

Options:
    -h --help       This message
    -c --cache      Cache Only
    -u --update     Force Update
    -v --verbose    Verbose Output
    -D --debug      Debug Output

"""

from docopt import docopt
import re
import os
import io
import csv
import errno
# from urllib.parse import urlparse
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

    def csv(self, args):
        output = io.StringIO()
        self.cache_read()
        for torrent in self.torrents:
            writer = csv.writer(output,
                                quoting=csv.QUOTE_ALL)
            writer.writerow([torrent['title'],
                             torrent['number'],
                             torrent['size'],
                             torrent['files'],
                             torrent['age'],
                             torrent['seed'],
                             torrent['leech'],
                             torrent['url']])
        print(output.getvalue())

    def show(self, args):
        self.cache_read()
        for torrent in self.torrents:
            if args['--verbose']:
                print(torrent)
            else:
                print(str(torrent['page']) + ":" +
                      str(torrent['number']) + "\t" +
                      torrent['title'])

    def scrape(self, args):
        self.torrents = self.scrape_kat_tv_torrents()
        self.cache_save()
        self.driver.quit()

    def cache_read(self):
        try:
            with open(configDirCacheFile, 'r') as infile:
                self.torrents = json.load(infile)
        except OSError:
            raise

    def cache_save(self):
        try:
            with open(configDirCacheFile, 'w') as outfile:
                json.dump(self.torrents, outfile)
        except OSError:
            raise

    def scrape_kat_tv_torrents(self):

        number = 1
        pageno = 1
        pageend = 400

        r = re.compile(r'^magnet.*')
        pageend = pageend + 2
        if pageend > 400:
            pageend = 400

        while pageno < pageend:
            print("Pages Processed: " + str(pageno) +
                  ", Torrents Processed: " + str(number))
            try:
                if pageno <= 1:
                    self.driver.get(link)
                else:
                    pageurl = "".join([link, str(pageno), "/"])
                    print("pageurl: " + pageurl)
                    self.driver.get(pageurl)

                s = BeautifulSoup(self.driver.page_source)
                sleep(1)
            except:
                break

            for a in s.find_all('a', href=r):
                if a:
                    td = a.findParent('td')
                    tr = td.findParent('tr')
                    trs = tr.find_all('td')
                    ta = td.find_all('a', attrs=cellMainLink)

                    torrent = {}
                    torrent['title'] = ""
                    torrent['url'] = a['href']
                    torrent['page'] = int(pageno)
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

                    print(str(torrent['page']) + ":" +
                          str(torrent['number']) + "\t" +
                          torrent['title'])

                    self.torrents.append(torrent)
            pageno = pageno + 1

        return self.torrents


def main():
    args = docopt(__doc__, version='TorrentFinder 0.1.0')
    print(args)
    scraper = GetKatTV()
    if args['update']:
        scraper.scrape(args)
    elif args['show']:
        scraper.show(args)
    elif args['csv']:
        scraper.csv(args)


if __name__ == "__main__":
    main()
