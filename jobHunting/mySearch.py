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

import copy
import logging
import os
import random
import sys
import time

try:
    from beeprint import pp as ppt
except Exception as e:
    try:
        from prettyprinter import cpprint as ppt
    except Exception as e:
        from pprint import pprint as ppt


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# CONSTANT
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOGGER
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONST
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# LOGIC
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def howlong(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        logger.info("time consumed:{}".format(end - start))
        print("{} : {}".format(func.__name__, end - start))
        return r

    return wrapper


# ================================================================
# PURPOSE：
# ================================================================
class MySearch(object):
    """docstring for MySearch."""

    def __init__(self, num):
        super(MySearch, self).__init__()

        tmp = set()
        while True:
            tmp.add(random.randint(11, 99))
            if len(tmp) >= num:
                break

        self.numbers = list(tmp)

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def binarySearch(self, x):
        targets = sorted(copy.deepcopy(self.numbers))
        n = 0

        logger.warning("\n\n\nbinary search,\tinitial:{}".format(targets))
        low, high = 0, len(targets) - 1
        while low <= high:
            n += 1
            mid = int((low + high) / 2)
            logger.info("mid={},targets[{}]={}".format(mid, mid, targets[mid]))
            if targets[mid] > x:
                high = mid - 1
            elif targets[mid] < x:
                low = mid + 1
            else:
                logger.info("found it: {}".format(x))
                logger.info("n={}".format(n))
                return targets[mid]

        logger.info("found nothing")
        logger.info("n={}".format(n))
        return None

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def interpolationSearch(self, x):
        targets = sorted(copy.deepcopy(self.numbers))
        n = 0

        logger.warning("\n\n\nbinary search,\tinitial:{}".format(targets))
        low, high = 0, len(targets) - 1
        while low <= high:
            n += 1
            mid = low + int((high - low) * (x - targets[low]) / (targets[high] - targets[low]))
            logger.info("mid={},targets[{}]={}".format(mid, mid, targets[mid]))
            if targets[mid] > x:
                high = mid - 1
            elif targets[mid] < x:
                low = mid + 1
            else:
                logger.info("found it: {}".format(x))
                logger.info("n={}".format(n))
                return targets[mid]

        logger.info("found nothing")
        logger.info("n={}".format(n))
        return None


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def batch():
    obj = MySearch(8)
    obj.binarySearch(33)
    obj.interpolationSearch(33)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MAIN
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main(args):
    batch()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
