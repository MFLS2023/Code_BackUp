import pymysql

# 数据库连接信息 (与主程序文件保持一致)
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'zhenghang'


def query_accounts(username, account_type):
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8'
        )
        cursor = connection.cursor()

        if account_type == '企业管理员':
            query = """
                SELECT  Name, Registered_Capital, Contact_Person, Registration_Date, Phone, Address, Account 
                FROM EnterpriseInformation 
                WHERE Account = %s 
            """
        elif account_type == '总管理员':
            query = """
                SELECT Name, Registered_Capital, Contact_Person, Registration_Date, Phone, Address, Account
                FROM EnterpriseInformation 
            """
        elif account_type == '银行账户':
            query = """
                SELECT Bank_Name, Balance, Max_Monthly_Spending, Registration_Date, PhoneNumber, Account, Business_License_Number 
                FROM BankAccount
                WHERE Account = %s
            """
        else:
            return []

        if account_type in ['企业管理员', '银行账户']:
            cursor.execute(query, (username,))
        else:
            cursor.execute(query)

        results = cursor.fetchall()
        cursor.close()
        connection.close()

        return results
    except pymysql.MySQLError as e:
        print(f"Error querying database: {e}")
        return []