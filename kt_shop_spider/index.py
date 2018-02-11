import MySql
import function as func

print("开始连接数据库")
mysql = MySql.MySql("localhost", "root", "", "kcweshop")
print("数据库连接成功")
print("爬虫开始：")
print("开始获取所有商品链接")
urls,_ = func.getPageUrl()
print("链接获取成功")
i = 1
for url in urls:
    print("当前进度：", i, "/", len(urls))
    goods, imgs, error = func.getGoods(url)
    if error == 0:
        print("PV值为0已自动跳过\n")
    else:
        print("开始写入数据库")
        sql = "select * from goods where title = '" + goods['title'] + "'"
        sql = "insert into goods(title,price,code,spe,weight,sale,img,cont) values('"+goods['title']+"',"+goods['price']+",'"+goods['code']+"','"+goods['spe']+"',"+goods['weight']+",0,'"+goods['img']+"','')"
        mysql.exec(sql)
        sql = "select * from goods where title = '"+goods['title']+"'"
        row = mysql.query(sql)
        for img in imgs:
            sql = "insert into goods_img(goods_id, img) values("+str(row['id'])+", '"+img+"')"
            mysql.exec(sql)
        print("写入数据库成功\n")
    i = i + 1

print("爬虫结束")

