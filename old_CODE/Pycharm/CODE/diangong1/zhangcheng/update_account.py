import pymysql

# 数据库连接信息 (与主程序文件保持一致)
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'zhenghang'


def update_account(account_type, account_id,
                   new_name, new_value1, new_value2,  # 基础信息
                   new_contact_person=None, new_phone=None,
                   new_address=None, new_main_business=None,
                   new_registration_date=None):
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
                UPDATE EnterpriseInformation
                SET Name = %s, Registered_Capital = %s, Contact_Person = %s,
                    Phone = %s, Address = %s, Main_Business = %s, Registration_Date = %s
                WHERE Id = %s
            """
            cursor.execute(query, (new_name, new_value1, new_contact_person,
                                   new_phone, new_address, new_main_business,
                                   new_registration_date, account_id))

        elif account_type == '银行账户':
            query = """
                UPDATE BankAccount 
                SET BankName = %s, Balance = %s, MaxMonthlySpending = %s 
                WHERE Id = %s
            """
            cursor.execute(query, (new_name, new_value1, new_value2, account_id))

        else:
            return "账户类型错误"

        connection.commit()
        cursor.close()
        connection.close()
        return "更新成功"

    except pymysql.MySQLError as e:
        return f"更新失败: {e}"