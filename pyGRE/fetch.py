#!-usr-bin-env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright 2017 Ulric Yang <ITC@itc-PC>
#
#  This program is free software; you can redistribute it and-or modify
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
#                    _ooOoo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                    O* = *O
#                ____*`---'*____
#              .   ' **| |** `.
#               * **||| : |||** *
#             * _||||| -:- |||||- *
#               | | *** - *** | |
#             | *_| ''*---*'' | |
#              * .-*__ `-` ___*-. *
#           ___`. .' *--.--* `. . __
#        ."" '< `.___*_<|>_*___.' >'"".
#       | | : `- *`.;`* _ *`;.`* - ` : | |
#         * * `-. *_ __* *__ _* .-` * *
# ======`-.____`-.___*_____*___.-`____.-'======
#                    `=---='
# .............................................
#          佛祖镇楼                  BUG辟易

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# PORPOSE:
#
# USAGE:
#
# CAUSION:
#
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# import all the required libraries
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import asyncio
import logging
import multiprocessing
import os
import pickle
import random
import re
from pprint import pprint

import aiohttp
import async_timeout
import xlrd
from lxml import etree

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# set up logs
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ================================================================
# config the file mode
# ================================================================
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    datefmt="%a, %d %b %Y %H:%M:%S",
    filename="runtime.log",
    filemode="a+",
)
# ================================================================
# config the console mode
# ================================================================
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# global variables
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
dirpath = os.path.dirname(os.path.abspath(__file__))


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FetchWord(object):
    """docstring for FetchWord"""

    def __init__(self):
        super(FetchWord, self).__init__()
        self.pageurl = "https://www.91dict.com/words?w="

    # ****************************************************************
    #
    # ****************************************************************
    async def fetchPage(self, session, word):
        with async_timeout.timeout(100):
            url = self.pageurl + word
            async with session.get(url) as resp:
                return await resp.text()

    # ****************************************************************
    #
    # ****************************************************************
    async def fetchWord(self, myloop, word):
        async with aiohttp.ClientSession(loop=myloop) as session:
            # ----------------------------------------------------------------
            #
            # ----------------------------------------------------------------
            html = await self.fetchPage(session, word)
            eh = etree.HTML(html)
            result = self.processPage(eh, word)
            wholeword = dict()
            wholeword[word] = result
            # ----------------------------------------------------------------
            #
            # ----------------------------------------------------------------
            filename = os.sep.join([dirpath, "wordsdump", ".".join([word, "pkl"])])
            with open(filename, "wb") as target:
                pickle.dump(wholeword, target)

    # ****************************************************************
    #
    # ****************************************************************
    def processPage(self, etree_page, word):
        infos = etree_page.xpath("//div[@class='tmInfo']")[0]
        # ----------------------------------------------------------------
        #
        # ----------------------------------------------------------------
        try:
            pronunciation = infos.xpath("//div[@class='vos']/span[2]/text()")
            pronunciation = pronunciation[1].strip("\n")
        except Exception as e:
            pronunciation = ""
        # ----------------------------------------------------------------
        #
        # ----------------------------------------------------------------
        try:
            meaning = infos.xpath("//div[@class='tmInfo']/div[1]/text()")
            meaning = list(map(lambda x: x.strip("\n"), meaning))
            meaning = list(filter(lambda x: x, meaning))
        except Exception as e:
            meaning = []
        # ----------------------------------------------------------------
        #
        # ----------------------------------------------------------------
        try:
            examples = []
            example = infos.xpath("//div[@class='tmInfo']/div[3]")[0]
            example = example.xpath("//ul[@class='slides clearfix']/li")
            for e in example:
                currnt1 = e.xpath(
                    "./div[@class='imgMainbox']/div[@class='carousel-caption']/div[@class='mBottom']/text()"
                )
                currnt2 = e.xpath(
                    "./div[@class='imgMainbox']/div[@class='carousel-caption']/div[@class='mFoot']/text()"
                )
                former = e.xpath(
                    "./div[@class='mTextend']/div[@class='box'][1]/div[@class='sty2']/p/text()"
                )
                latter = e.xpath(
                    "./div[@class='mTextend']/div[@class='box'][2]/div[@class='sty2']/p/text()"
                )
                res = tuple(
                    [
                        "\n".join(former),
                        "\n".join([word.join(currnt1), currnt2[0]]),
                        "\n".join(latter),
                    ]
                )
                examples.append(res)
        except Exception as e:
            print(e)
            examples = []
        # ----------------------------------------------------------------
        #
        # ----------------------------------------------------------------
        result = dict(pronunciation=pronunciation, meaning=meaning, examples=examples, word=word)
        return result


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def getwords(xlsfile):
    # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
    #
    # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
    xls = xlrd.open_workbook(xlsfile)
    sheet = xls.sheet_by_name("Sheet1")
    words = sheet.col_values(0)
    # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
    #
    # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
    finewords = []
    pattern = re.compile("(\w|-)+")
    for w in words:
        ps = pattern.search(w)
        finewords.append(ps.group())
    # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
    #
    # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
    with open("gre3000.pkl", "wb") as target:
        pickle.dump(finewords, target)
    # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
    #
    # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
    return words


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def main(pieces):

    # ================================================================
    #
    # ================================================================
    excelfile = os.sep.join([dirpath, "3000.xls"])
    # getwords(excelfile)
    with open("gre3000.pkl", "rb") as target:
        words = pickle.load(target)
    # ================================================================
    #
    # ================================================================
    fw = FetchWord()
    # ================================================================
    #
    # ================================================================
    theloop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(fw.fetchWord(theloop, w)) for w in words[100 * (pieces - 1) :]
    ]  # 100 * (pieces)]]
    theloop.run_until_complete(asyncio.gather(*tasks))

    return 0


if __name__ == "__main__":
    for i in range(31, 32):
        main(i)
