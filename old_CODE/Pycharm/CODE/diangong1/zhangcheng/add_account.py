import pymysql

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'zhenghang'


def add_account(account_type,  # 添加账户类型
                name, value1, value2, account, password,
                business_license=None, contact_person=None,
                phone=None, address=None, main_business=None,
                registration_date=None):
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

        if account_type == '企业账户':
            query = """
                INSERT INTO EnterpriseInformation (Name, Registered_Capital, Contact_Person, 
                                                    Account, Password, Business_License_Number,
                                                    Phone, Address, Main_Business, Registration_Date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, value1, contact_person, account, password,
                                   business_license, phone, address, main_business,
                                   registration_date))
        elif account_type == '银行账户':
            query = """
                INSERT INTO BankAccount (BankName, Balance, MaxMonthlySpending, Account, Password)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, value1, value2, account, password))
        else:
            return "账户类型错误"

        connection.commit()
        cursor.close()
        connection.close()
        return "添加成功"

    except pymysql.MySQLError as e:
        return f"添加失败: {e}"