#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rrword.py
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

from pprint import pprint

import requests
from bs4 import BeautifulSoup


class RenrenDict(object):
    """
    """

    def __init__(self, word):
        """
        """
        self.wordpage = "http://www.91dict.com/words?w=" + word

    def generateFile(self):
        """
        """
        r = requests.get(self.wordpage)
        htmldoc = r.text
        soup = BeautifulSoup(htmldoc, "lxml")
        section = soup.find_all(attrs={"class": "col-sm-12 col-lg-7 checkWord"})[-1]

        with open("htmlBlock.html", "w") as f:
            f.write(str(section))


def main(args):

    rrd = RenrenDict("refugee")
    rrd.generateFile()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
