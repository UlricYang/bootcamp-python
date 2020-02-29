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
import sys

import pymysql

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
logdirname = "logs"
not os.path.exists(logdirname) and os.makedirs(logdirname)
logfilename = os.path.join(logdirname, os.path.splitext(__file__)[0])
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
class MySQL(object):
    """docstring for MySQL."""

    def __init__(self):
        super(MySQL, self).__init__()
        self.host = "172.17.0.2"
        self.port = 3306
        self.user = "root"
        self.password = "yangrui"
        self.database = "test"

        self.db = None
        self.cursor = None

    def __enter__(self):
        self.db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.db.cursor()

        if self.db:
            logger.info("login successful")
            logger.info(
                "mysql://{}:{}@{}:{}/{}".format(
                    self.host, self.port, self.user, self.password, self.database
                )
            )

    def __exit__(self, *args):
        self.cursor.close()
        self.db.close()

        self.cursor = None
        self.db = None

        if not self.db:
            logger.info("logout successful.")

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def execute_sql(self, sql):
        res = None
        for each in [each.strip("\n") + ";" for each in sql.split(";") if each.strip("\n")]:
            logger.info("SQL: {}".format(each))
            res = self.cursor.execute(each)
            self.db.commit()
        return res

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def execute_sql_multi(self, sqls):
        for sql in sqls:
            self.execute_sql(sql)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# **=--=*=--=*=--=*=--=*=--=*=--=*=--=*=--=*=--=*=--=*=--=*=--=**
sql_initial = [
    """
drop table if exists student;
create table student(sid varchar(6), sname varchar(10), sage datetime, ssex varchar(10));
insert into student values('01' , 'ZL' , '1990-01-01' , 'M');
insert into student values('02' , 'QD' , '1990-12-21' , 'M');
insert into student values('03' , 'SF' , '1990-05-20' , 'M');
insert into student values('04' , 'LY' , '1990-08-06' , 'M');
insert into student values('05' , 'ZM' , '1991-12-01' , 'F');
insert into student values('06' , 'WL' , '1992-03-01' , 'F');
insert into student values('07' , 'ZZ' , '1989-07-01' , 'F');
insert into student values('08' , 'WJ' , '1990-01-20' , 'F')
""",
    """
drop table if exists sc;
create table sc(sid varchar(10), cid varchar(10), score decimal(18,1));
insert into sc values('01' , '01' , 80);
insert into sc values('01' , '02' , 90);
insert into sc values('01' , '03' , 99);
insert into sc values('02' , '01' , 70);
insert into sc values('02' , '02' , 60);
insert into sc values('02' , '03' , 80);
insert into sc values('03' , '01' , 80);
insert into sc values('03' , '02' , 80);
insert into sc values('03' , '03' , 80);
insert into sc values('04' , '01' , 50);
insert into sc values('04' , '02' , 30);
insert into sc values('04' , '03' , 20);
insert into sc values('05' , '01' , 76);
insert into sc values('05' , '02' , 87);
insert into sc values('06' , '01' , 31);
insert into sc values('06' , '03' , 34);
insert into sc values('07' , '02' , 89);
insert into sc values('07' , '03' , 98)
""",
    """
drop table if exists course;
create table course(cid varchar(10),cname varchar(10),tid varchar(10));
insert into course values('01' , 'Chinese' , '02');
insert into course values('02' , 'Math' , '01');
insert into course values('03' , 'English' , '03')
""",
    """
drop table if exists teacher;
create table teacher(tid varchar(10),tname varchar(10));
insert into teacher values('01' , 'Z3');
insert into teacher values('02' , 'L4');
insert into teacher values('03' , 'W5')
""",
]


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MAIN
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main(args):
    obj = MySQL()
    with obj:
        # obj.execute_sql_multi(sql_initial)
        with open("sqls/01.sql", "r") as f:
            sql = " ".join([each.strip("\n") for each in f.readlines()])
            # print(" ".join(sql.split("\n")))
            # print(sql)
        obj.execute_sql(sql)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
