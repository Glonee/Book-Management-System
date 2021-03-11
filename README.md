# 图书管理系统 Python+MySQL
## 环境依赖
Python 3.5+   
MySQL 8.0  
MySQL Connector for Python
## 部署步骤
1. 在MySQL中创建一个名为bbs数据库
    ```sql
    create database bbs;
    ```
2. 在数据库中创建user,book,borrow三个表
    ```sql
    use bbs;
    create table user(
        name varchar(20) NOT NULL,
        id bigint NOT NULL,
        sex char(1),
        password char(40) NOT NULL
    );
    create table book(
        book_id varchar(20) NOT NULL,
        author varchar(20) NOT NULL,
        book_name varchar(30) NOT NULL,
        book_press varchar(20) NOT NULL,
        book_amount int
    );
    create table borrow(
        id int NOT NULL,
        user_name varchar(20) NOT NULL,
        user_id bigint NOT NULL,
        book_name varchar(30) NOT NULL,
        book_id varchar(20) NOT NULL
    );
    ```
3. 将bbs.py中连接数据库所使用的参数更改为所需要的参数。  
   ```python
   db=mysql.connector.connect(
       host="localhost"     #你的数据库主机地址
       user="root"          #你的用户名
       passwd="admin"       #你的密码
       database="bbs"       #使用的数据库
   )
   ```

**PS：交作业前一天熬夜写的代码**