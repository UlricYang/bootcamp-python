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
import logging
import os
import random
import sys
from functools import lru_cache

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
# ================================================================
# PURPOSE：
# ================================================================
class BackTracing(object):
    """docstring for BackTracing."""

    def __init__(self):
        super(BackTracing, self).__init__()

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def subs(self):
        N = 16
        test_list = list()
        while True:
            t = random.randint(0, N)
            if t not in test_list:
                test_list.append(t)
            if len(test_list) == N:
                break

        def solve1(tlist, n):
            if n == 0:
                return [[]]
            else:
                temp = solve1(tlist[: n - 1], n - 1)
                ans = temp[:]
                for i in temp:
                    ans.append(i + [tlist[n - 1]])
                return ans

        ppt(len(solve1(test_list, len(test_list))))

        def solve2(tlist):
            if len(tlist) == 0:
                return [[]]
            else:
                temp = solve2(tlist[:-1])
                ans = temp[:]
                for i in temp:
                    ans.append(i + [tlist[-1]])
                return ans

        ppt(len(solve2(test_list)))

        @lru_cache()
        def solve3(n):
            if n == 0:
                return [[]]
            else:
                temp = solve3(n - 1)
                ans = temp[:]
                for i in temp:
                    ans.append(i + [test_list[-1]])
                return ans

        ppt(len(solve3(len(test_list))))


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def batch():
    obj = BackTracing()
    obj.subs()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MAIN
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main(args):
    batch()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
