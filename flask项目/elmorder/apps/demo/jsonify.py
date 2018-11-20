import json

from flask import jsonify


search_info = {'id': 132, 'user_role': 3}
print(type(search_info))  # 输出 <type 'dict'>)
# 转为string用dumps
print(type(json.dumps(search_info)), json.dumps(search_info))  # 输出 <type 'str'>
# string转 dict用 loads()
print(type(json.loads(json.dumps(search_info))))  # 输出  <type 'dict'>
