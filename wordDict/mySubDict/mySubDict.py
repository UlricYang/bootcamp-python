#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mySubDict.py
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


import collections
import os.path as op
import re
import string
from pprint import pprint

import pysrt
import unqlite


class SubDict(object):
    """
	"""

    def __init__(self, subpath):
        """
		"""
        if op.isfile(subpath):
            self.subpath = subpath

        self.dbsubs = unqlite.UnQLite("subs.db")
        self.dbword = unqlite.UnQLite("word.db")

        subtitles = self.dbsubs.collection("subtitles")
        if subtitles.exists():
            pass
        else:
            subtitles.create()

        words = self.dbword.collection("words")
        if words.exists():
            pass
        else:
            words.create()

    def processSub(self):
        """
		"""
        sub = pysrt.open(self.subpath, encoding="gbk")
        temp = []

        for s in sub:
            if s.text.find("}") == -1:
                temp.append(s)

        self.subs = temp

    def storeSubtitles(self, thetitle, episode):
        """
		"""
        mys = self.subs
        myc = self.dbsubs.collection("subtitles")
        temp = []

        tempindex = thetitle + "-" + episode + "-"
        sublength = len(str(len(mys)))
        for i, s in enumerate(mys):
            myindex = tempindex + str(i).zfill(sublength)
            mycontent = s.text
            temp.append({"myindex": myindex, "mycontent": mycontent})

        myc.store(temp)

    def storeWords(self):
        """
		"""
        mys = self.subs
        myc = self.dbword.collection("words")

        temp = ""
        for i, s in enumerate(mys):
            temp += s.text.split("\n")[-1] + " "

        delset = string.punctuation
        delset = delset.replace("'", "")
        fline = re.sub("[" + delset + "]", " ", temp).lower()
        rawwords = re.split("\s+", fline)
        newwords = collections.Counter(rawwords)

        wwww = []
        for n in newwords:
            myword = n
            mytime = newwords[n]
            wwww.append({"myword": myword, "mytime": mytime})

        for w in wwww:
            mf = myc.filter(lambda odj: obj["myword"] == w)
            if len(mf):
                theid = mf[0]["__id"]
                newtime = mf[0]["mytime"] + w["mytime"]
                myc.update(theid, {{"myword": myword, "mytime": newtime}})
            else:
                myc.store(w)

    def storeWords_another(self):
        """
		"""
        mys = self.subs

        temp = ""
        for i, s in enumerate(mys):
            temp += s.text.split("\n")[-1] + " "

        delset = string.punctuation
        delset = delset.replace("'", "")
        fline = re.sub("[" + delset + "]", " ", temp).lower()

        rawwords = re.split("\s+", fline)
        newwords = collections.Counter(rawwords)

        for n in newwords:
            myword = n
            mytime = newwords[n]
            if len(myword) > 0:
                self.dbword[myword] = int(self.dbword[myword]) + int(mytime)
                """
				try:
					self.dbword[myword] += mytime
				except Exception as e:
					self.dbword[myword] = mytime
				"""


def main(args):

    thesubpath = "/home/ulric/workspace/codes/py/mySubDict/subs/test.srt"
    thename = "TheFlash"
    theseason = 3
    theepisode = 16
    thetag = "S" + str(theseason).zfill(2) + "E" + str(theepisode).zfill(2)

    sd = SubDict(thesubpath)
    sd.processSub()
    sd.storeSubtitles(thename, thetag)
    sd.storeWords()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
