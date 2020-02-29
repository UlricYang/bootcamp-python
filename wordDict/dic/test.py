#
# Copyright (c) 2015 by Placeholder Corporation. All Rights Reserved.
#

import pickle
from pprint import pprint

import mydict

fpath = "/home/ulric/yr/workspace/python/dic/__pycache__/tofinish.pickup"

with open(fpath, "rb") as f:
    data = pickle.load(f)

pprint(data)

"""
for d in data:
    mydict.MyLookup(d).wholeThing()
"""
