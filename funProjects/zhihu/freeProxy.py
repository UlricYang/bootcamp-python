#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  freeProxy.py
#
#  Copyright 2016 Unknown <ulric@ulric-pc>
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
"""
作者：一起学习Python
链接：https://zhuanlan.zhihu.com/p/21535440
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


import requests
from lxml import etree


def get_proxies_from_site():
    """

	"""
    url = "http://proxy.ipcn.org/country/"
    xpath = "/html/body/div[last()]/table[last()]/tr/td/text()"

    r = requests.get(url)
    tree = etree.HTML(r.text)

    results = tree.xpath(xpath)
    proxies = [line.strip() for line in results]

    return proxies


# 使用http://lwons.com/wx网页来测试代理主机是否可用
def get_valid_proxies(proxies, count):
    """

	"""
    url = "http://lwons.com/wx"
    results = []
    cur = 0
    for p in proxies:
        proxy = {"http": "http://" + p}
        succeed = False
        try:
            r = requests.get(url, proxies=proxy)
            if r.text == "default":
                succeed = True
        except Exception as e:
            print("error:", p)
            succeed = False
        if succeed:
            print("succeed:", p)
            results.append(p)
            cur += 1
            if cur >= count:
                break


def main(args):
    print("get " + str(len(get_valid_proxies(get_proxies_from_site(), 20))) + " proxies")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
