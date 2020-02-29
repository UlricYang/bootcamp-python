#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright Ulric Yang
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
#                ____*'---'*____
#                . ' **| |** ' .
#               * **||| : |||** *
#             * _||||| -:- |||||- *
#               | | *** - *** | |
#             | *_| ''*---*'' | |
#              * .-*__ '-' ___*-. *
#           ___'. .' *--.--* '. .'__
#        ."" '< '.___*_<|>_*___.' >'"".
#       | | : '- *'.:'* _ *':.'* - ' : | |
#         * * '-. *_ __* *__ _* .-' * *
# ======'-.____'-.___*_____*___.-'____.-'======
#                    '=---='
# .............................................
#          佛祖镇楼                  BUG辟易

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# PORPOSE:
#
# USAGE:
#   python <filename>
# CAUSION:
#
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# ================================================================
# import all the required libraries
# ================================================================

import asyncio
import logging
import sys

import aiofile
import aiohttp

try:
    from prettyprinter import cpprint as cpt
except Exception as e:
    from pprint import pprint as cpt


# ================================================================
# set up logs
# ================================================================
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# config the file mode
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    datefmt="%a, %d %b %Y %H:%M:%S",
    filename="runtime.log",
    filemode="a+",
)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# config the console mode
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# global variables
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# sum up the whole procedule
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def main(args):

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
