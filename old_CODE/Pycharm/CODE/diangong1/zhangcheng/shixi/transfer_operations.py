from PyQt5.QtWidgets import (
    QInputDialog,
    QMessageBox,
    QLineEdit,
    QPushButton,
    QDialog,
    QFormLayout,
)
import pymysql


class TransferDialog(QDialog):
    def __init__(self, db, current_account_number):
        super().__init__()
        self.setWindowTitle("转账")
        self.db = db
        self.current_account_number = current_account_number  # 当前账号

        self.layout = QFormLayout(self)
        self.fields = {}

        for label in [
            "目标账号",
            "转账金额",
            "转账用途",
            "支付密码",
        ]:
            self.fields[label] = QLineEdit(self)
            self.layout.addRow(label, self.fields[label])

        self.transfer_button = QPushButton("确认转账", self)
        self.transfer_button.clicked.connect(self.transfer)
        self.layout.addRow(self.transfer_button)

    def transfer(self):
        target_account = self.fields["目标账号"].text()
        amount = self.fields["转账金额"].text()
        purpose = self.fields["转账用途"].text()
        password = self.fields["支付密码"].text()

        if not all([target_account, amount, password]):
            QMessageBox.warning(self, "警告", "目标账号、转账金额和支付密码不能为空！", QMessageBox.Ok)
            return

        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "警告", "转账金额必须是数字！", QMessageBox.Ok)
            return

        try:
            cur = self.db.cursor()

            # 检查支付密码是否正确
            sql = f"SELECT Password FROM BankAccount WHERE Account = '{self.current_account_number}'"
            cur.execute(sql)
            result = cur.fetchone()
            if result is None or result[0] != password:
                QMessageBox.warning(self, "错误", "支付密码错误！", QMessageBox.Ok)
                return

            # 检查余额是否充足
            sql = f"SELECT Balance FROM BankAccount WHERE Account = '{self.current_account_number}'"
            cur.execute(sql)
            current_balance = cur.fetchone()[0]
            if current_balance < amount:
                QMessageBox.warning(self, "错误", "余额不足！", QMessageBox.Ok)
                return

            # 检查目标账户是否存在
            sql = f"SELECT ID FROM BankAccount WHERE Account = '{target_account}'"
            cur.execute(sql)
            target_account_id = cur.fetchone()
            if target_account_id is None:
                QMessageBox.warning(self, "错误", "目标账户不存在！", QMessageBox.Ok)
                return

            # 更新转出账户余额
            sql = f"UPDATE BankAccount SET Balance = Balance - {amount} WHERE Account = '{self.current_account_number}'"
            cur.execute(sql)

            # 更新目标账户余额
            sql = f"UPDATE BankAccount SET Balance = Balance + {amount} WHERE Account = '{target_account}'"
            cur.execute(sql)

            # 记录转账信息
            sql = """
                INSERT INTO TransactionRecord (Source_Account, Target_Account, Amount, Purpose, Transfer_Time)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cur.execute(sql, (self.current_account_number, target_account, amount, purpose))
            self.db.commit()

            QMessageBox.information(self, "提示", "转账成功！", QMessageBox.Ok)
            self.accept()
        except pymysql.Error as e:
            self.db.rollback()
            QMessageBox.critical(self, "错误", f"数据库操作失败: {e}", QMessageBox.Ok)