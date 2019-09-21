import requests
from PIL import Image
from io import BytesIO
import pytesseract
import base64

def encoding(username, password):  # 学号密码加密
    username = str(base64.b64encode(username.encode("utf-8")), encoding="utf-8")
    password = str(base64.b64encode(password.encode("utf-8")), encoding="utf-8")
    return "{0}{1}{1}{1}{2}".format(username, "%", password)

def login(username, password):
    res = {
        "code": 0,  # -1错误 1成功 0未定义
        "msg": "",  # 为何错误
        "session": None # 成功的session
    }
    headers = { #请求头数据
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }
    session = requests.session()
    code_url = "http://202.199.100.156/jsxsd/verifycode.servlet"
    login_url = "http://202.199.100.156/jsxsd/xk/LoginToXk"
    encoded = encoding(username, password)  # 加密处理学号密码
    while True:
        response = session.get(code_url, headers=headers)
        image = Image.open(BytesIO(response.content))
        image = image.convert("L")  # 验证码图片灰度处理
        table = [1] * 256
        for i in range(256):
            table[i] = 0
            if i > 115:
                break
        image = image.point(table, "1")  # 验证码图片二值化处理
        v = pytesseract.image_to_string(image)
        v = v.replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", "")
        if len(v) == 4:
            datas = {
                'userAccount': username,  # 学号可有可无
                'userPassword': '',  # 密码 直接留空就好
                'RANDOMCODE': v,  # 验证码 得正确
                'encoded': encoded  # 学号base64加密%%%密码base64加密
            }
            t = session.post(login_url, datas, headers=headers)
            if "验证码错误" in t.text:
                continue
            if "用户名或密码错误" in t.text:
                res['code'] = -1
                res['msg'] = "用户名或密码错误"
            if "用户名或密码不能为空" in t.text:
                res['code'] = -1
                res['msg'] = "用户名或密码不能为空"
            if "教学一体化服务平台" in t.text:
                res['code'] = 1
                res['msg'] = "登陆成功"
                res['session'] = session
            return res

