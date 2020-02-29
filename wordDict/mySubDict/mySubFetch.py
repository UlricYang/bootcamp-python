#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mySubFetch.py
#
#  Copyright 2017 Ulric Yang <ryang_nudt@163.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
import re
import subprocess
import urllib
from functools import reduce
from itertools import chain
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from wget import download


class SubFetch(object):
    """
	"""

    def __init__(self, keyword):
        """
		"""
        self.theurl = (
            "http://www.zmz2017.com/search/index/?page=1&keyword=" + keyword + "&type=subtitle"
        )

    def soupPage(self, theurl):
        """
		"""
        htmldoc = requests.get(theurl).text
        soup = BeautifulSoup(htmldoc, "lxml")
        return soup

    def getSub(self):
        """
		retrieve all qualified urls in one page
		"""
        soup = self.soupPage(self.theurl)
        sections = soup.find_all(attrs={"class": "t f14"})

        urlpool = []
        """
		p = re.compile('第\d+季第\d+集')		
		for s in sections:
			if p.search(s.text):				
				urlpool.append('http://www.zmz2017.com'+s.a['href'])
		"""
        for s in sections:
            urlpool.append("http://www.zmz2017.com" + s.a["href"])
        p = re.compile("第\d+季第\d+集")
        return urlpool

    def getNextpage(self):
        """
		return urls of all pages which contain multipul suburl for sub
		"""
        soup = self.soupPage(self.theurl)
        thesection = soup.find_all(attrs={"class": "pages pages-padding"})[-1]
        maxnum = thesection.find_all("a", href=True)[-1].text
        maxnum = re.sub("\D", "", maxnum)

        temp = []
        p = re.compile("page=\d+")
        for i in range(int(maxnum)):
            pp = "page=" + str(i + 1)
            s = re.sub(p, pp, self.theurl)
            temp.append(s)

        return temp

    def getWebpage(self):
        """
		"""
        webpages = []

        nextpages = self.getNextpage()
        for n in nextpages:
            s = self.getSub()
            webpages = list(chain(webpages, s))

        return webpages

    def getSubInPage(self, pageurl):
        """
		"""
        htmldoc = requests.get(pageurl).text
        soup = BeautifulSoup(htmldoc, "lxml")

        thesection = soup.find_all(attrs={"class": "subtitle-links tc"})[-1]
        thelinks = [link.get("href") for link in thesection.find_all("a", href=True)]
        theinfos = [link.text for link in thesection.find_all("a", href=True)]
        thelink = [tl for tl in thelinks if ("zip" or "rar") in tl]
        theinfo = [ti for ti in theinfos if ("zip" or "rar") in ti]

        print((theinfo[0], thelink[0]))
        # return((theinfo[0],thelink[0]))
        return thelink[0]

    def getAllSubs(self):
        """
		"""
        pages = self.getWebpage()
        rm = reduce(lambda x, y: x + "\n" + y, map(self.getSubInPage, pages))

        with open("downloads.txt", "a") as f:
            f.write(rm)

            # subprocess.call(['wget', '-i', 'downloads.txt'])


def main(args):

    keyword = "福尔摩斯：演绎法"

    sf = SubFetch(keyword)
    # sf.getSub()
    # sf.getNextpage()
    # sf.getWebpage()
    # sf.getSubInPage('http://www.zmz2017.com/subtitle/48634')
    sf.getAllSubs()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
