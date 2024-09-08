from PyQt5.QtWidgets import (
    QInputDialog,
    QMessageBox,
    QLineEdit,
    QPushButton,
    QDialog,
    QFormLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
import pymysql


# --- 添加银行账户对话框 ---
class AddBankAccountDialog(QDialog):
    def __init__(self, db, license_number):  # 传递营业执照号
        super().__init__()
        self.setWindowTitle("添加银行账户")
        self.db = db
        self.license_number = license_number

        self.layout = QFormLayout(self)
        self.fields = {}

        for label in [
            "银行名称",
            "余额",
            "最大月支出",
            "注册日期",
            "电话号码",
            "账号",
            "密码",
        ]:
            self.fields[label] = QLineEdit(self)
            self.layout.addRow(label, self.fields[label])

        # 营业执照号不需要输入，直接使用传递进来的值
        self.fields["营业执照号"] = QLabel(self.license_number, self)
        self.layout.addRow("营业执照号", self.fields["营业执照号"])

        self.save_button = QPushButton("保存", self)
        self.save_button.clicked.connect(self.save_bank_account)
        self.layout.addRow(self.save_button)

    def save_bank_account(self):
        try:
            cur = self.db.cursor()
            # 从输入框获取数据，营业执照号直接使用传递进来的值
            data = [
                self.fields["银行名称"].text(),
                self.fields["余额"].text(),
                self.fields["最大月支出"].text(),
                self.fields["注册日期"].text(),
                self.fields["电话号码"].text(),
                self.fields["账号"].text(),
                self.fields["密码"].text(),
                self.license_number
            ]

            # 将 Bank_Name 修改为 BankName, Max_Monthly_Expenses 修改为 MaxMonthlySpending,
            # Registration_Date 修改为 Registration_Date,  Phone 修改为 PhoneNumber
            sql = """
                INSERT INTO bankaccount (BankName, Balance, MaxMonthlySpending, Registration_Date, PhoneNumber, Account, Password, Business_License_Number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, data)
            self.db.commit()
            QMessageBox.information(self, "提示", "银行账户添加成功!", QMessageBox.Yes)
            self.accept()
        except pymysql.Error as e:
            self.db.rollback()
            QMessageBox.critical(self, "错误", f"数据库操作失败: {e}", QMessageBox.Ok)


# --- 修改银行账户对话框 ---
class ModifyBankAccountDialog(QDialog):
    def __init__(self, db, account_data):
        super().__init__()
        self.setWindowTitle("修改银行账户信息")
        self.db = db
        self.account_data = account_data

        self.layout = QFormLayout(self)
        self.fields = {}

        # 创建输入框，并用现有数据填充
        field_labels = [
            "ID",
            "银行名称",
            "余额",
            "最大月支出",
            "注册日期",
            "电话号码",
            "账号",
            "密码",
            "营业执照号"
        ]
        for i, label in enumerate(field_labels):
            self.fields[label] = QLineEdit(self)
            self.fields[label].setText(str(account_data[i]))
            self.layout.addRow(label, self.fields[label])

        self.save_button = QPushButton("保存修改", self)
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addRow(self.save_button)

    def save_changes(self):
        try:
            cur = self.db.cursor()
            # 从输入框获取修改后的数据
            data = [
                self.fields["银行名称"].text(),
                self.fields["余额"].text(),
                self.fields["最大月支出"].text(),
                self.fields["注册日期"].text(),
                self.fields["电话号码"].text(),
                self.fields["账号"].text(),
                self.fields["密码"].text(),
                self.fields["营业执照号"].text(),  # 营业执照号
                self.fields["ID"].text()  # ID作为where条件
            ]
            # 将 Bank_Name 修改为 BankName, Max_Monthly_Expenses 修改为 MaxMonthlySpending,
            # Registration_Date 修改为 Registration_Date,  Phone 修改为 PhoneNumber
            sql = """
                UPDATE BankAccount 
                SET BankName=%s, Balance=%s, MaxMonthlySpending=%s, Registration_Date=%s, 
                    PhoneNumber=%s, Account=%s, Password=%s, Business_License_Number=%s 
                WHERE ID=%s
            """
            cur.execute(sql, data)
            self.db.commit()
            QMessageBox.information(self, "提示", "银行账户信息修改成功!", QMessageBox.Yes)
            self.accept()
        except pymysql.Error as e:
            self.db.rollback()
            QMessageBox.critical(self, "错误", f"数据库操作失败: {e}", QMessageBox.Ok)


# --- 删除银行账户 ---
def delete_bank_account(db, account_number, window):
    reply = QMessageBox.question(
        window,
        "确认删除",
        f"确定要删除账号为 {account_number} 的银行账户吗？",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if reply == QMessageBox.Yes:
        try:
            cur = db.cursor()
            # 将 Account_Number 修改为 Account
            sql = f"DELETE FROM bankaccount WHERE Account = '{account_number}'"
            cur.execute(sql)
            db.commit()
            QMessageBox.information(window, "提示", "银行账户已成功删除！", QMessageBox.Yes)
            window.update_account_display()  # 删除后更新银行账户显示
        except pymysql.Error as e:
            db.rollback()
            QMessageBox.critical(window, "错误", f"数据库操作失败: {e}", QMessageBox.Ok)


# --- 查询银行账户 ---
def search_bank_account(db, window):
    account_number, ok = QInputDialog.getText(
        window, "查询银行账户", "请输入要查询的银行账号:"
    )
    if ok and account_number:
        try:
            cur = db.cursor()
            # 将 Account_Number 修改为 Account
            sql = f"SELECT * FROM bankaccount WHERE Account = '{account_number}'"
            cur.execute(sql)
            result = cur.fetchall()  # 获取所有匹配结果
            cur.close()

            if result:
                # 创建一个新的窗口，用表格展示查询结果
                query_window = QDialog(window)
                query_window.setWindowTitle("查询结果")
                query_layout = QVBoxLayout(query_window)

                table_widget = QTableWidget(query_window)
                table_widget.setColumnCount(len(result[0]))  # 设置表格列数

                # 将列名修改为数据库中对应的名称
                table_widget.setHorizontalHeaderLabels(
                    [
                        "Id",
                        "BankName",
                        "Balance",
                        "MaxMonthlySpending",
                        "Registration_Date",
                        "PhoneNumber",
                        "Account",
                        "Password",
                        "Business_License_Number",
                    ]
                )
                table_widget.setRowCount(len(result))  # 设置表格行数
                for row_index, row_data in enumerate(result):
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        table_widget.setItem(row_index, col_index, item)
                query_layout.addWidget(table_widget)
                query_window.exec_()

            else:
                QMessageBox.information(window, "提示", "未找到该银行账户！", QMessageBox.Yes)

        except pymysql.Error as e:
            QMessageBox.critical(window, "错误", f"数据库操作失败: {e}", QMessageBox.Ok)