import json
from datetime import date, datetime


"""
str,int,list,tuple,dict,bool,None这些数据类型都支撑json序列化操作。
但是datetime类型不支持json序列化，我们可以自定义datetime的序列化。
"""


class JsonToDatetime(json.JSONEncoder):
    """
    JSONEncoder不知道怎么去把这个数据转换成json字符串的时候，
    它就会调用default()函数，default()函数默认会抛出异常。
    所以，重写default()函数来处理datetime类型的数据。

    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H: %M: %S")
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


d = {"name": "ric", "age": 18, "data": datetime.now()}

print(json.dumps(d, cls=JsonToDatetime))
