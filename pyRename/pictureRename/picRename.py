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
import hashlib
import logging
import os
import sys

from aiofile import AIOFile

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
class PicRename(object):
    def __init__(self, picfolder):
        self.piclist = [
            os.path.join(root, f) for root, dirs, files in os.walk(picfolder) for f in files
        ]

    async def getMD5(self, pic):
        async with AIOFile(pic, "rb") as afp:
            content = await afp.read()
            picmd5 = hashlib.md5(content).hexdigest()
        return picmd5

    async def get_pics(self):
        for each in self.piclist:
            yield each

    async def rename(self, logo):
        async for p in self.get_pics():
            try:
                pictype = os.path.splitext(p)[1]
                md5 = await self.getMD5(p)
                newname = os.path.dirname(p) + os.sep + logo + "-" + md5 + pictype.lower()
                if not os.path.exists(newname):
                    os.rename(p, newname)
                    logger.info("{} ---> {}".format(p, newname))
            except Exception as e:
                logger.error(e)


# ----------------------------------------------------------------
# FUNCTION:
# PARAMETERS:
# RESULT:
# ----------------------------------------------------------------


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MAIN
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main(args):
    p = "/home/ulric/workspace/codes/py/pyRename/pictureRename/pic"

    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(PicRename(each[0]).rename(each[1]))
        for each in [(os.path.join(p, l), l) for l in os.listdir(p)]
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
