import sut_new_login
import requests

username = ""
password = ""

res = sut_new_login.login(username, password)

if res['code'] == 1:
    session = res['session']
else:
    print(res['msg'])
