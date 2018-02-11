from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import requests
import json
import re

def openUrl(url): #获取url信息
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        html = BeautifulSoup(html.read(), "html.parser")
    except AttributeError as e:
        return None
    return html


def getData(html, label, attr, attrData, rec=0): #得到数据
    if html is None:
        return None
    if rec == 0:
        data = html.findAll(label, {attr: attrData})
    else:
        data = html.findAll(label, {attr: re.compile(attrData)})
    return data

def getImage(url): #得到所有图片
    html = openUrl(url)
    datas = getData(html, "img", "src", "\/\/[A-Za-z0-9\.\/]+\.jpg", 1)
    imgs = []
    for data in datas:
        arr = re.compile("1\/([A-Za-z0-9/]+\.jpg)").split(data['src'])
        if len(arr) > 1:
            imgs.append("http://img.kangtingshop.com/TJKTImgService/upload/pi/N7//"+arr[1].replace("/", ""))
    fimgs = getData(html, "", "id", "divIntroduce")
    for fimg in fimgs:
        if fimg.p:
            ps = fimg.findAll("p")
            for p in ps:
                if p.img:
                    imgs.append(p.img['src'])
    return imgs

def getTitle(url): #得到商品名称
    html = openUrl(url)
    data = getData(html, "h1", "class", "details_r_h1")
    if data[0].p.text == "":
        text = data[0].text.replace(" ", "")
        text = text.replace("\n", "")
    else:
        text, _ = data[0].stripped_strings
    return text

def getPrice(url): #得到商品价格
    html = openUrl(url)
    data = getData(html, "div", "class", "details_money_l")
    text = data[0].em.text.replace("￥", "")
    return text

def getPv(url): #得到商品PV
    html = openUrl(url)
    data = getData(html, "div", "class", "details_money_l")
    text = data[0].p.text.replace("PV：", "")
    return text

def getParameter(url): #得到产品参数
    html = openUrl(url)
    data = getData(html, "div", "class", "details_parameter")
    lis= data[0].ul.findAll("li")
    i = 0
    parameter = []
    for li in lis:
        if i == 1 or i == 3:
            parameter.append(li.span.text)
        if i == 4:
            weight = li.span.text
            parameter.append(weight.replace("g", ""))
            break;
        i = i + 1
    return parameter

def getGoods(url): #得到商品信息
    print("开始爬虫："+url)
    goods = {}
    img = []
    if int(getPv(url)) == 0:
        return goods, img, 0
    imgs = getImage(url)
    for i in range(1, len(imgs)):
        img.append(imgs[i])
    pars = getParameter(url)
    title = getTitle(url)
    price = getPrice(url)
    goods['title'] = title
    goods['price'] = price
    goods['code'] = pars[0]
    goods['spe'] = pars[1]
    goods['weight'] = pars[2]
    goods['img'] = imgs[0]
    print("爬虫成功："+title)
    return goods, img, 1

def getPageUrl(): #得到页面url
    url = "http://kt.kangtingshop.com/TJKTNewMall/Product/ProductView?PID="
    postUrl = "http://kt.kangtingshop.com/TJKTNewMall/Product/BindProductList"
    datas = {
        "categoryID": 0,
        "brandID": 0,
        "searchKeyWord": "",
        "searchStartPrice":0,
        "searchEndPrice": 0,
        "searchStartPV": 0,
        "searchEndPV": 0,
        "type": 0,
        "sort": 0,
        "pageIndex": 1,
        "pageSize": 186
    }
    data = json.loads(requests.post(postUrl, data=datas).text)
    rows = data['PageData']
    urls = []
    ktIds = []
    for row in rows:
        urls.append(url+row['ProductID'])
        ktIds.append(row['ProductID'])
    return urls, ktIds
