# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle
import pymysql
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QLabel,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QDialog,
    QFormLayout,
    QComboBox,
)
from bank_account_operations import (
    AddBankAccountDialog,
    ModifyBankAccountDialog,
    delete_bank_account,
    search_bank_account,
)
from transfer_operations import TransferDialog  # 导入转账对话框

class BankAccountWindow(QtWidgets.QMainWindow):
    def __init__(self, accounts_data):
        super().__init__()
        self.setWindowTitle("银行账户信息")
        self.setGeometry(100, 100, 700, 500)

        self.accounts_data = accounts_data
        self.current_account_data = accounts_data[0] if accounts_data else None
        self.db = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="zhenghang",
            charset="utf8",
        )

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 下拉菜单选择银行账户
        self.account_selector = QComboBox(self)
        for account in accounts_data:
            self.account_selector.addItem(f"账号: {account[6]}")
        self.account_selector.currentIndexChanged.connect(self.select_account)
        self.layout.addWidget(self.account_selector)

        # 用于显示账户信息的 QLabel
        self.field_labels = [
            "ID",
            "银行名称",
            "余额",
            "最大月支出",
            "注册日期",
            "电话号码",
            "账号",
            "密码",
            "营业执照号",
        ]
        self.labels = []
        for i in range(len(self.field_labels)):
            label = QLabel("", self.central_widget)
            label.setGeometry(QtCore.QRect(20, 60 + i * 30, 350, 20))
            self.labels.append(label)

        # 初始化显示第一个账户的信息
        self.display_account_data(self.current_account_data)

        # 调整 "账号" 标签位置
        self.labels[6].setGeometry(QtCore.QRect(20, 300, 350, 20))  # 调整位置，避免重叠

        # 添加按钮
        self.add_button = QPushButton("添加银行账户", self.central_widget)
        self.add_button.setGeometry(QtCore.QRect(400, 60, 150, 30))
        self.add_button.clicked.connect(self.add_bank_account)

        self.delete_button = QPushButton("删除银行账户", self.central_widget)
        self.delete_button.setGeometry(QtCore.QRect(400, 100, 150, 30))
        self.delete_button.clicked.connect(
            lambda: delete_bank_account(self.db, self.current_account_data[6], self)
        )

        self.modify_button = QPushButton("修改银行账户信息", self.central_widget)
        self.modify_button.setGeometry(QtCore.QRect(400, 140, 150, 30))
        self.modify_button.clicked.connect(self.modify_bank_account)

        self.search_button = QPushButton("查询银行账户", self.central_widget)
        self.search_button.setGeometry(QtCore.QRect(400, 180, 150, 30))
        self.search_button.clicked.connect(
            lambda: search_bank_account(self.db, self)
        )

        # 添加转账按钮
        self.transfer_button = QPushButton("转账", self.central_widget)
        self.transfer_button.setGeometry(QtCore.QRect(400, 220, 150, 30))
        self.transfer_button.clicked.connect(self.open_transfer_dialog)

    # 显示选中的银行账户信息
    def display_account_data(self, account_data):
        if account_data:
            for i, data in enumerate(account_data):
                self.labels[i].setText(f"{self.field_labels[i]}: {data}")
        else:
            for i in range(len(self.field_labels)):
                self.labels[i].setText("")

    # 处理下拉菜单选择事件
    def select_account(self, index):
        self.current_account_data = self.accounts_data[index]
        self.display_account_data(self.current_account_data)

    # --- 添加银行账户 ---
    def add_bank_account(self):
        dialog = AddBankAccountDialog(self.db, self.current_account_data[8])
        if dialog.exec_() == QDialog.Accepted:
            # 更新显示
            self.update_account_display()

    # --- 修改银行账户 ---
    def modify_bank_account(self):
        dialog = ModifyBankAccountDialog(self.db, self.current_account_data)
        if dialog.exec_() == QDialog.Accepted:
            # 更新显示
            self.update_account_display()

    # 更新银行账户显示
    def update_account_display(self):
        try:
            cur = self.db.cursor()
            license_number = self.current_account_data[8]
            sql = f"SELECT * FROM bankaccount WHERE Business_License_Number = '{license_number}'"
            cur.execute(sql)
            self.accounts_data = cur.fetchall()
            cur.close()

            if self.accounts_data:
                self.account_selector.clear()
                for account in self.accounts_data:
                    self.account_selector.addItem(f"账号: {account[6]}")
                self.current_account_data = self.accounts_data[0]
                self.display_account_data(self.current_account_data)
            else:
                QMessageBox.warning(
                    self, "警告", "该企业名下没有银行账户！", QMessageBox.Ok
                )
                self.close()
        except pymysql.Error as e:
            QMessageBox.critical(
                self, "错误", f"数据库操作失败: {e}", QMessageBox.Ok
            )

    # 打开转账对话框
    def open_transfer_dialog(self):
        dialog = TransferDialog(self.db, self.current_account_data[6])  # 传递当前账号
        if dialog.exec_() == QDialog.Accepted:
            # 转账成功后更新显示
            self.update_account_display()