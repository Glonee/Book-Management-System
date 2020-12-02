import mysql.connector
import hashlib
import random
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database="bbs"
)
def user_login(ind):
    cursor=db.cursor()
    sql="SELECT * FROM user WHERE id='%d'"%(ind)
    cursor.execute(sql)
    result = cursor.fetchall()
    if  result:
        res=result[0]
        password=input("请输入密码：\n")
        password=hashlib.sha1(password.encode('utf-8'))
        pwd = password.hexdigest()
        if pwd==res[3]:
            login_stuats = True
            print("登录成功\n")
        else:
            login_stuats = False
            print("密码错误！\n")
    else:
        print("用户不存在！\n")
        login_stuats = False
        res=[]
    return (login_stuats,res)
def user_create():
    cursor=db.cursor()
    name=input("用户名：\n")
    ind=int(input("学号：\n"))
    sex=input("性别(M/F):\n")
    password=input("密码：\n")
    password=hashlib.sha1(password.encode('utf-8'))
    pwd = password.hexdigest()
    sql="INSERT INTO user VALUES('%s','%d','%s','%s')"%(name,ind,sex,pwd)
    cursor.execute(sql)
    db.commit()
def book_select():
    cursor=db.cursor()
    while True:
        a=int(input("按以下关键字查找：\n[1]书名 [2]作者 [3]ISBN [4]出版社"))
        if a==1:
            x="book_name"
            y=input("请输入书名:\n")
            break
        elif a==2:
            x="author"
            y=input("请输入作者:\n")
            break
        elif a==3:
            x="book_id"
            y=input("请输入ISBN:\n")
            break
        elif a==4:
            x="book_press"
            y=input("请输入出版社:\n")
            break
        else:
            print("输入有误\n")
    sql="SELECT * FROM book WHERE %s='%s'"%(x,y)
    cursor.execute(sql)
    result=cursor.fetchall()
    if result:
        for i in result:
            print("书名:%s  作者:%s  ISBN:%s  出版社:%s 剩余数量:%d\n"%(i[2],i[1],i[0],i[3],i[4]))
    else:
        print("查无此书\n")
def borrow(resu):
    cursor=db.cursor()
    book_id=input("请输入图书ISBN:\n")
    sql="SELECT * FROM book WHERE book_id='%s'"%(book_id)
    cursor.execute(sql)
    result=cursor.fetchall()
    if result:
        res=result[0]
        if res[4]==0:
            print("抱歉，图书已全部借出\n")
        else:
            sql="UPDATE book SET book_amount=book_amount-1 WHERE book_id='%s'"%(book_id)
            cursor.execute(sql)
            db.commit()
            while True:
                borrow_id=random.randint(0,2147483647)
                sql="SELECT * FROM borrow WHERE id='%d'" %(borrow_id)
                cursor.execute(sql)
                p=cursor.fetchall()
                if not p:
                    sql="INSERT INTO borrow (id,user_name,user_id,book_name,book_id) VALUES(%d,'%s',%d,'%s','%s')"%(borrow_id,resu[0],resu[1],res[2],res[0])
                    cursor.execute(sql)
                    db.commit()
                    print("成功借出！\n")
                    sql="SELECT * FROM borrow WHERE id='%d'"%(borrow_id)
                    cursor.execute(sql)
                    b=cursor.fetchall()
                    b=b[0]
                    print("借阅号:%d\n"%(b[0]))
                    break
    else:
        print("查无此书\n")
def back(user):
    cursor=db.cursor()
    sql="SELECT * FROM borrow WHERE user_id='%d'"%(user[1])
    cursor.execute(sql)
    result=cursor.fetchall()
    if result:
        print("您有如下借阅记录:\n")
        for i in result:
            print("借阅号:%d   书名：%s    ISBN:%s\n"%(i[0],i[3],i[4]))
        back_id=int(input("请输入需要归还的图书借阅号:\n"))
        sql="SELECT * FROM borrow WHERE id='%d'"%(back_id)
        cursor.execute(sql)
        l=cursor.fetchall()
        if l and l[0][1]==user[0]:
            sql="UPDATE book SET book_amount=book_amount+1 WHERE book_id='%s'"%(l[0][4])
            cursor.execute(sql)
            db.commit()
            sql="DELETE FROM borrow WHERE id='%d'"%(back_id)
            cursor.execute(sql)
            db.commit()
            print("还书成功！\n")
        else:
            print("借阅号有误\n")
    else:
        print("您没有借阅记录！\n")
print("欢迎使用图书管理系统！\n")
while True:
    s=int(input("[1]登录    [2]注册    [3]退出\n"))
    if s==3:
        exit(0)
    elif s==1:
        ind=int(input("请输入学号:\n"))
        s=user_login(ind)
        if s[0]:
            break
    elif s==2:
        user_create()
user=s[1]
while True:
    s=int(input("[1]查询   [2]借书   [3]还书   [4]退出\n"))
    if s==4:
        exit(0)
    elif s==1:
        book_select()
    elif s==2:
        borrow(user)
    elif s==3:
        back(user)