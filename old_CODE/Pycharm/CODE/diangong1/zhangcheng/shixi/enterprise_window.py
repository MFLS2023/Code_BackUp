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
from enterprise_operations import (
    AddEnterpriseDialog,
    ModifyEnterpriseDialog,
    delete_enterprise,
    search_enterprise,
)

class EnterpriseWindow(QtWidgets.QMainWindow):
    def __init__(self, enterprise_data):
        super().__init__()
        self.setWindowTitle("企业信息")
        self.setGeometry(100, 100, 600, 500)

        self.enterprise_data = enterprise_data
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

        # 显示企业信息的 QLabel
        self.field_labels = [
            "ID",
            "名称",
            "地址",
            "联系人",
            "电话",
            "注册资本",
            "营业执照号",
            "账户",
            "密码",
            "主营业务",
            "注册日期",
        ]
        self.labels = []
        for i, data in enumerate(enterprise_data):
            label = QLabel(f"{self.field_labels[i]}: {data}", self.central_widget)
            label.setGeometry(QtCore.QRect(20, 30 + i * 30, 350, 20))
            self.labels.append(label)

        # 添加按钮
        self.add_button = QPushButton("添加企业", self.central_widget)
        self.add_button.setGeometry(QtCore.QRect(400, 30, 150, 30))
        self.add_button.clicked.connect(self.add_enterprise)

        self.delete_button = QPushButton("删除企业", self.central_widget)
        self.delete_button.setGeometry(QtCore.QRect(400, 70, 150, 30))
        self.delete_button.clicked.connect(
            lambda: delete_enterprise(self.db, self.enterprise_data[6], self)
        )

        self.modify_button = QPushButton("修改企业信息", self.central_widget)
        self.modify_button.setGeometry(QtCore.QRect(400, 110, 150, 30))
        self.modify_button.clicked.connect(self.modify_enterprise)

        self.search_button = QPushButton("查询企业", self.central_widget)
        self.search_button.setGeometry(QtCore.QRect(400, 150, 150, 30))
        self.search_button.clicked.connect(
            lambda: search_enterprise(self.db, self)
        )

    # --- 添加企业 ---
    def add_enterprise(self):
        dialog = AddEnterpriseDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            # 更新显示
            self.update_enterprise_display()

    # --- 修改企业信息 ---
    def modify_enterprise(self):
        dialog = ModifyEnterpriseDialog(self.db, self.enterprise_data)
        if dialog.exec_() == QDialog.Accepted:
            # 更新显示
            self.update_enterprise_display()

    def update_enterprise_display(self):
        try:
            cur = self.db.cursor()
            sql = f"SELECT * FROM EnterpriseInformation WHERE ID = {self.enterprise_data[0]}"
            cur.execute(sql)
            updated_data = cur.fetchone()
            cur.close()

            if updated_data:
                self.enterprise_data = updated_data
                # 更新 QLabel 显示
                for i, data in enumerate(updated_data):
                    self.labels[i].setText(f"{self.field_labels[i]}: {data}")
            else:
                QMessageBox.warning(self, "警告", "企业信息已删除！", QMessageBox.Ok)
                self.close()
        except pymysql.Error as e:
            QMessageBox.critical(self, "错误", f"数据库操作失败: {e}", QMessageBox.Ok)