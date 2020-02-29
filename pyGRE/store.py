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


import logging
import os
import pickle
from pprint import pprint

import unqlite

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


class StoreWords(object):
    """docstring for StoreWords"""

    def __init__(self, picklespath):
        super(StoreWords, self).__init__()
        self.picklespath = picklespath

    # ****************************************************************
    #
    # ****************************************************************
    def _getPickles(self):
        pickles = []
        for root, dirs, files in os.walk(self.picklespath):
            for f in files:
                if f.endswith(".pkl"):
                    pickles.append(os.sep.join([root, f]))
        return pickles

    # ****************************************************************
    #
    # ****************************************************************
    def toDB(self, dbname, collectionname):
        # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
        #
        # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
        db = unqlite.UnQLite(dbname)
        cl = db.collection(collectionname)
        if not cl.exists():
            cl.create()
        else:
            cl.drop()
            cl.create()
        # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
        #
        # ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
        pickles = self._getPickles()
        for pk in pickles:
            print("processing------", pk)
            with open(pk, "rb") as target:
                tmp = pickle.load(target)
                # tmpdict = dict()
                # for k, v in tmp.items():
                #     tmpdict['word'] = k
                #     for kk, vv in v.items():
                #         tmpdict[kk] = vv
                # cl.store(tmpdict)
                # cl.store(tmp)
                # pprint(tmp)
                for k, v in tmp.items():
                    cl.store(v)
            print("done")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# sum up the whole procedule
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main(args):
    picklepath = os.sep.join([dirpath, "wordsdump"])
    sw = StoreWords(picklepath)
    sw.toDB(dbname="English.db", collectionname="gre3000")
    return 0


if __name__ == "__main__":
    try:
        import sys

        sys.exit(main(sys.argv))
    except Exception as e:
        logging.error(e)
