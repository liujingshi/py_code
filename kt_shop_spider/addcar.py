import requests
import sys
import MySql

mysql = MySql.MySql("localhost", "kcweshop", "kcweshop", "kcweshop")

headers = { #请求头数据
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}

def login(username, password, session): #登录
    loginPostUrl = "http://kt.kangtingshop.com/TJKTNewMall/Home/LoginForm" #登录验证地址
    checkCodeImgUrl = "http://kt.kangtingshop.com/TJKTNewMall/Home/GetValidateCode" #验证码图片地址
    session.get(checkCodeImgUrl, headers=headers) #获取验证码图片
    checkCode = session.cookies.get("MallCheckCode") #从cookie中读取验证码
    loginData = { #登录需要post的数据
        "Mobile": username, #手机号
        "Password": mysql.md5(password), #md5加密的密码
        "CheckCode": checkCode #4位验证码
    }
    t = session.post(loginPostUrl, loginData, headers=headers) #登录
    return t.text, session

def addCar(goodsId, num, session): #添加购物车
    addCarurl1 = "http://kt.kangtingshop.com/TJKTNewMall/Partial/GetCanAddCart" #验证是否可以加入购物车地址
    addCarurl2 = "http://kt.kangtingshop.com/TJKTNewMall/ShoppingCart/AddProduct" #加入购物车地址
    addCarurl3 = "http://kt.kangtingshop.com/TJKTNewMall/Partial/UpdateShoppingCart" #更新购物车地址
    data1 = { #加入购物车的数据
        "ProductID": goodsId, #产品ID
        "QTY": int(num) #数量
    }
    data2 = {} #更新购物车的数据
    t = session.post(addCarurl1, data1, headers=headers) #第一次验证是否可以加入购物车
    if t.text == "ok":
        t = session.post(addCarurl1, data1, headers=headers) #第二次验证是否可以加入购物车
        if t.text == "ok":
            t = session.post(addCarurl1, data1, headers=headers) #第三次验证是否可以加入购物车
            if t.text == "ok":
                t = session.post(addCarurl2, data1, headers=headers) #加入购物车
                if t.text == "ok":
                    session.post(addCarurl3, data2, headers=headers) #更新购物车
                    return "Add Car Ok"
    return "error"

session = requests.Session()
username = sys.argv[1]
password = sys.argv[2]
orderId = sys.argv[3]

t, session = login(username, password, session)
if t == "ok":
    sql = "select * from user_order_cont where order_id = "+str(orderId)
    rows = mysql.queryAll(sql)
    for row in rows:
        sql = "select * from goods where id = "+str(row['goods_id'])
        goods = mysql.query(sql)
        t = addCar(goods['kt_id'], row['num'], session)
        if t == "error":
            print("Add Car Error")
            exit()
    print("Ok")
else:
    print("Login Error")

