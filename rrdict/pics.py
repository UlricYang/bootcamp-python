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

import itertools
import json

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# LIBRARY
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import logging
import os
import sys
from multiprocessing.dummy import Pool as ThreadPool

import requests

import jsonlines

try:
    from prettyprinter import cpprint as ppt
except Exception as e:
    from pprint import pprint as ppt


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# CONSTANT
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
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
class RetrievePicture(object):
    """docstring for RetrievePicture."""

    def __init__(self, jfile):
        super(RetrievePicture, self).__init__()
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.jfile = jfile
        with jsonlines.open(self.jfile, "r") as reader:
            self.data = [json.loads(row) for row in reader]
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.picdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pictures")

    def __enter__(self):
        not os.path.exists(self.picdir) and os.makedirs(self.picdir)

    def __exit__(self, *arg):
        pass

    def process_single(self, wordinfo):
        pics = wordinfo.get("examples")
        res = list(map(lambda x: {"img_src": x.get("img_src"), "tag": x.get("tag")}, pics))
        return res

    def process_multiple(self):
        res = list(map(lambda x: self.process_single(x), self.data))
        result = itertools.chain.from_iterable(res)
        return result

    def retrieve_pic(self, picinfo):
        src = picinfo.get("img_src")
        des = os.path.join(self.picdir, picinfo.get("tag") + ".jpg")
        r = requests.get(src)
        with open(des, "wb") as target:
            target.write(r.content)
        logger.info("retrieve picture:{}, store in:{}".format(src, des))

    def run(self):
        pool = ThreadPool(4)
        pool.map(self.retrieve_pic, self.process_multiple())
        pool.close()
        pool.join()


# ----------------------------------------------------------------
# FUNCTION:
# PARAMETERS:
# RESULT:
# ----------------------------------------------------------------


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MAIN
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main(args):
    jf = "results.jsonlines"
    obj = RetrievePicture(jf)
    with obj:
        obj.run()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
