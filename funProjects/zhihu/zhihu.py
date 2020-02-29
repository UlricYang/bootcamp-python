import re
import time
from subprocess import Popen

import requests

headers = {
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http://www.zhihu.com",
    "Accept-Language": "zh-CN",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/5.0(Windows NT 6.1;WOW64;Trident/7.0;rv:11.0)like Gecko",
    "Host": "www.zhihu.com",
}

s = requests.session()
r = s.get("http://www.zhihu.com", headers=headers)


def getXSRF(r):
    cer = re.compile('name="_xsrf" value="(.*)"', flags=0)
    strlist = cer.findall(r.text)
    return strlist[0]


_xsrf = getXSRF(r)

print(r.request.headers)
print(str(int(time.time() * 1000)))

Captcha_URL = "http://www.zhihu.com/captcha.gif?r=" + str(int(time.time() * 1000))
r = s.get(Captcha_URL, headers=headers)

with open("code.gif", "wb") as f:
    f.write(r.content)
Popen("code.gif", shell=True)
captcha = input("captcha: ")
login_data = {
    "_xsrf": _xsrf,
    "email": "rebelregister@163.com",
    "password": "lovingyou0228",
    "remember_me": "true",
    "captcha": captcha,
}

s.post("http://www.zhihu.com/#signin", data=login_data, headers=headers)
r = s.get("http://www.zhihu.com")
print(r.text)
