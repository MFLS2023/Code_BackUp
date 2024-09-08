import mysql.connector

db=mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="zhenghang"
)

cursor=db.cursor()
def Log_in():
    Email_Address=input("请输入邮箱地址：")
    Password=input("请输入密码：")

    sql="select User_Name,Password,Age,Date_birthday,Email_Address,Phone_Number,Gender,Address,Career from t_user where email_address=%s and password=%s"
    cursor.execute(sql,(Email_Address,Password))

    result=cursor.fetchall()
    if len(result)>0:
        print("登陆成功")
    else:
        print("用户名或密码错误，请重新登录")

Log_in()

