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

import datetime
import logging
import os
import sys

import click
from flask import Flask, abort, json, jsonify, make_response, redirect, request, session, url_for

import config
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

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
app = Flask(__name__)
app.config["ADMIN_NAME"] = "ULRIC YANG"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.root_path, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "abc"
db = SQLAlchemy(app)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# DATA
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class Note(db.Model):
    """docstring for Node."""

    noteId = db.Column(db.Integer, primary_key=True)
    noteBody = db.Column(db.Text)

    def __repr__(self):
        return "<note: {}>".format(self.noteBody)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# LOGIC
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ================================================================
# PURPOSE：
# ================================================================
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


api.add_resource(HelloWorld, "/")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.cli.command()
def initdb():
    db.create_all()
    click.echo("initialized database")


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route("/hi", methods=["GET", "POST"])
def hi():
    name = request.args.get("name", "Flask")
    return "<h2>hi,{}</h2>".format(name)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route("/greet", defaults={"name": "programmer"})
@app.route("/greet/<name>")
def greet(name):
    return "<h3>hello {}!</h3>".format(name)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route("/goback/<int:year>")
def goback(year):
    print(year)
    return "welcome back to {}".format(2019 - year)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route("/hey")
def hey():
    # return "", 302, {"Location": "http://www.baidu.com", "cnm": 1}
    return redirect("http://www.sogou.com")


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route("/404")
def not_found():
    abort(404)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route("/foo")
def foo():
    data = {"name": "Ulric", "gender": "male"}
    # rsp = make_response(json.dumps(data))
    # rsp.mimetype = "application/json"
    # return rsp
    return jsonify(data)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route("/set/<name>")
def cookie_set(name):
    rsp = make_response(redirect(url_for("hello")))
    rsp.set_cookie("name", name)
    return rsp


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route("/hello")
def hello():
    name = request.args.get("name")
    if not name:
        name = request.cookies.get("name", "Human")
        rsp = "hello,{}".format(name)
    login_status = "[authenticated]" if "logged_in" in session else "[un-authenticated]"
    return rsp + login_status


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route("/login")
def login():
    session["logged_in"] = True
    return redirect(url_for("hello"))


@app.route("/logout")
def logout():
    if "logged_in" in session:
        session.pop("logged_in")
    return redirect(url_for("hello"))


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.before_request
def my_before_request():
    print("start - {}".format(datetime.datetime.now()))


@app.after_request
def my_after_request(response):
    print("stop  - {}".format(datetime.datetime.now()))
    return response


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MAIN
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main(args):
    app.run(host="0.0.0.0", port=5000, debug=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
