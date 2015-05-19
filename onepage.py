#!/usr/bin/env python

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import json
import time

driver = webdriver.PhantomJS()
driver.get("http://kickass.to")
driver.find_elements_by_link_text("TV Shows Torrents")

time.sleep(10)

print(json.dumps(driver.page_source))
