#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright 2018 Ulric Yang <yangrui@posbao.net>
#
#  This program is free software: you can redistribute it and-or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation: either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY: without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program: if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#                    _ooOoo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                    O* = *O
#                ____*'---'*____
#              .   ' **| |** '.
#               * **||| : |||** *
#             * _||||| -:- |||||- *
#               | | *** - *** | |
#             | *_| ''*---*'' | |
#              * .-*__ '-' ___*-. *
#           ___'. .' *--.--* '. . __
#        ."" '< '.___*_<|>_*___.' >'"".
#       | | : '- *'.:'* _ *':.'* - ' : | |
#         * * '-. *_ __* *__ _* .-' * *
# ======'-.____'-.___*_____*___.-'____.-'======
#                    '=---='
# .............................................

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# PURPOSE:
#
#
# USAGE:
#
#
# CAUTION:
#
#
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# LIBRARY
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

import asyncio
import logging
import os
import pickle
import random
import re
import sys
import time
import uuid

import aiohttp
import pandas as pd

import jsonlines
from fake_useragent import UserAgent
from requests_html import HTML

try:
    from prettyprinter import cpprint as ppt
except Exception as e:
    from pprint import pprint as ppt


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# CONSTANT
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
UA = UserAgent()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# logger
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logfilename = os.path.splitext(__file__)[0]
logger = logging.getLogger(logfilename + ".log")
fhandler = logging.FileHandler(logfilename + ".log")
shandler = logging.StreamHandler()
fmt = " - ".join(
    ["%(asctime)s", "%(pathname)s:%(module)s:%(funcName)s", "%(lineno)s", "%(message)s"]
)
formatter = logging.Formatter(fmt)
fhandler.setFormatter(formatter)
shandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.addHandler(shandler)
logger.setLevel(logging.INFO)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# LOGIC
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ================================================================
# PURPOSE：
# ================================================================
class RetrieveWord(object):
    """docstring for RetrieveWord."""

    def __init__(self, baseurl):
        super(RetrieveWord, self).__init__()
        self.baseurl = baseurl
        self.sdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "success")

    def __enter__(self):
        not os.path.exists(self.sdir) and os.makedirs(self.sdir)
        self.words = self.get_words()

    def __exit__(self, *arg):
        results = list()
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        fs = [os.path.join(root, f) for root, dirs, files in os.walk(self.sdir) for f in files]
        for f in fs:
            with open(f, "r") as reader:
                try:
                    data = [row for row in reader][0]
                except Exception as e:
                    logger.error("load data error : {}".format(f))
                else:
                    results.append(data)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        with jsonlines.open("results.jsonlines", "w") as writer:
            writer.write_all(results)

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"User-Agent:": UA.chrome}) as response:
                try:
                    html = await response.text()
                    logger.info("processing: {}".format(url))
                    wordinfo = self.process_html(html)
                except Exception as e:
                    logger.error(e)
                else:
                    with jsonlines.open(
                        "success/{}.jsonl".format(url.split("=")[-1]), "w"
                    ) as writer:
                        writer.write(wordinfo)

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def run(self, chunksize=10):
        chunk = lambda x, n: [x[i : i + n] for i in range(0, len(x), n)]
        for c in chunk(self.words, chunksize):
            loop = asyncio.get_event_loop()
            tasks = [asyncio.ensure_future(self.fetch(self.baseurl.format(w.strip()))) for w in c]
            loop.run_until_complete(asyncio.gather(*tasks))
            time.sleep(random.random())


# ================================================================
# PURPOSE：
# ================================================================
class RRword(RetrieveWord):
    """docstring for RRword."""

    URL = "http://www.91dict.com/words?w={}"

    def __init__(self, excelfile):
        super(RRword, self).__init__(self.URL)
        self.excelfile = excelfile
        self.pattern = re.compile("\n+")

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def get_words(self):
        wpattern = re.compile(r"[\w\-]+")
        df = pd.read_excel(self.excelfile)
        res = list(df.iloc[:, 0])
        result = list(map(lambda x: wpattern.search(x).group(), res))
        return result

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def process_html(self, html):
        res = HTML(html=html)
        result = dict()
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        w_spell = res.find(".text", first=True).full_text
        w_pronunciation = self.pattern.split(res.find(".vos", first=True).full_text.strip("\n"))
        result["word"] = w_spell
        result["pronunciation"] = w_pronunciation
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        slides = res.find(".listBox")
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        #
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        w_meaning = slides[0].full_text.strip("\n")
        result["meaning"] = w_meaning
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        #
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        w_form = self.pattern.split(slides[1].full_text.strip("\n"))
        result["form"] = w_form
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        str_concat = lambda l: "\n".join(
            filter(lambda x: x and ("上文" not in x) and ("下文" not in x), l)
        )
        w_examples = list()
        examples = res.find("ul.slides.clearfix")[0].find("li")
        for each in examples:
            img_src = (
                each.find("div.imgMainbox", first=True)
                .find("img", first=True)
                .attrs.get("src")
                .split("?")[0]
            )
            context_src = self.pattern.split(each.find("div.mTop", first=True).full_text)
            context_prev = self.pattern.split(each.find("div.box")[0].full_text)
            context_next = self.pattern.split(each.find("div.box")[1].full_text)
            context_targ = self.pattern.split(each.find("div.mBottom", first=True).full_text)
            context_targ_meaning = self.pattern.split(each.find("div.mFoot", first=True).full_text)
            w_examples.append(
                {
                    "img_src": img_src,
                    "context_src": str_concat(context_src),
                    "context_prev": str_concat(context_prev),
                    "context_next": str_concat(context_next),
                    "context_targ": str_concat(
                        context_targ.extend(context_targ_meaning) or context_targ
                    ),
                    "tag": str(uuid.uuid4()),
                }
            )
        result["examples"] = w_examples

        return result


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MAIN
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main(args):
    obj = RRword("3k.xls")
    with obj:
        obj.run(20)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
