import requests
import json

a= requests.get('http://dynamic.zol.com.cn/channel/index.php?c=Ajax_MobileData&a=MobileNews&cid=74&page=1')
b= a.text.strip('()')
c= json.loads(b)
d= c.get('data')
for e in d:
       print(e.get('title'))