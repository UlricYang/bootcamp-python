#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  getTrainTicket.py
#
#  Copyright 2015 ulric <ulric@ulric-mint>
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


import traceback
from time import sleep

from splinter.browser import Browser

###容错做的不好，考虑的情况也不够多，大家见谅

# 用户名，密码
usernm = "ulric_yr@163.com"
passwd = "lovingyou"
# cookies值得自己去找, 下面两个分别是changsha, xian
starts = "%u957F%u6C99%2CCSQ"
ends = "%u897F%u5B89%2CXAY"
# 时间格式2016-01-31
dtime = "2016-09-01"
# 车次，选择第几趟，0则从上之下依次点击
order = 0
###乘客名
passenger = "杨瑞"

"""网址"""
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"


def login():
    b.find_by_text("登录").click()
    sleep(3)
    b.fill("loginUserDTO.user_name", usernm)
    sleep(1)
    b.fill("userDTO.password", passwd)
    sleep(1)
    print("等待验证码，自行输入...")
    while True:
        if b.url != initmy_url:
            sleep(1)
        else:
            break


def huoche():
    global b
    b = Browser(driver_name="chrome")
    b.visit(ticket_url)

    while b.is_text_present("登录"):
        sleep(1)
        login()
        if b.url == initmy_url:
            break

    try:
        print("购票页面...")
        # 跳回购票页面
        b.visit(ticket_url)

        # 加载查询信息
        b.cookies.add({"_jc_save_fromStation": starts})
        b.cookies.add({"_jc_save_toStation": ends})
        b.cookies.add({"_jc_save_fromDate": dtime})
        b.reload()

        sleep(2)

        count = 0
        # 循环点击预订
        if order != 0:
            while b.url == ticket_url:
                b.find_by_text("查询").click()
                count += 1
                print("循环点击查询... 第 %s 次" % count)
                sleep(1)
                try:
                    b.find_by_text("预订")[order - 1].click()
                except:
                    print("还没开始预订")
                    continue
        else:
            while b.url == ticket_url:
                b.find_by_text("查询").click()
                count += 1
                print("循环点击查询... 第 %s 次" % count)
                sleep(1)
                try:
                    for i in b.find_by_text("预订"):
                        i.click()
                except:
                    print("还没开始预订")
                    continue
        sleep(1)
        b.find_by_text(passenger)[1].click()
        print("能做的都做了.....不再对浏览器进行任何操作")
    except Exception as e:
        print(traceback.print_exc())


if __name__ == "__main__":
    huoche()
