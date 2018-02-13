import requests
from PIL import Image
from io import BytesIO
import pytesseract
import re
import sys

headers = { #请求头数据
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}

session = requests.session()

def login(UserName, PassWord):
    response = session.get("http://202.199.96.30/ACTIONVALIDATERANDOMPICTURE.APPPROCESS", headers=headers)
    image = Image.open(BytesIO(response.content))
    v = pytesseract.image_to_string(image)
    v = v.replace("\n", "")
    v = re.sub("\D", "", v)
    datas = {
        "WebUserNO":UserName,
        "Password":PassWord,
        "Agnomen":v,
        "submit.x":"27",
        "submit.y":"-1"
    }
    url = "http://202.199.96.30/ACTIONLOGON.APPPROCESS?mode=4"
    t = session.post(url, datas, headers=headers)
    return t.text

username = sys.argv[1]
password = sys.argv[2]

while True:
    t = login(username, password);
    if "请输入正确的附加码" in t:
        continue
    if "错误的用户名或者密码" in t:
        print("User Error")
        break
    if "您好!欢迎您登录教务处网络平台" in t:
        print("Success")
        break


