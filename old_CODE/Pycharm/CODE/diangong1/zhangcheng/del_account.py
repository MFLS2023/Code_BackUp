import pymysql

# 数据库连接信息 (与主程序文件保持一致)
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'zhenghang'


def delete_account(account_id, account_type):  # 添加 account_type 参数
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
            query = "DELETE FROM EnterpriseInformation WHERE Id = %s"
        elif account_type == '银行账户':
            query = "DELETE FROM BankAccount WHERE Id = %s"
        else:
            return "账户类型错误"

        cursor.execute(query, (account_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return "删除成功"

    except pymysql.MySQLError as e:
        return f"删除失败: {e}"