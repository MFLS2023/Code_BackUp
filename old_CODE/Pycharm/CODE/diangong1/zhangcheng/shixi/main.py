# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle
import pymysql
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QMessageBox,
    QLabel,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QDialog,
    QFormLayout,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
)
from enterprise_window import EnterpriseWindow  # 导入企业窗口类
from bank_account_window import BankAccountWindow  # 导入银行账户窗口类


class AdminWindow(QDialog):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("管理员界面")
        self.db = db
        self.resize(800, 600)

        self.layout = QVBoxLayout(self)

        self.enterprise_button = QPushButton("查看所有企业信息", self)
        self.enterprise_button.clicked.connect(self.show_all_enterprises)
        self.layout.addWidget(self.enterprise_button)

        self.bank_account_button = QPushButton("查看所有银行账户信息", self)
        self.bank_account_button.clicked.connect(self.show_all_bank_accounts)
        self.layout.addWidget(self.bank_account_button)

    def show_all_enterprises(self):
        try:
            cur = self.db.cursor()
            sql = "SELECT * FROM EnterpriseInformation"
            cur.execute(sql)
            results = cur.fetchall()
            cur.close()

            self.show_data_in_table(results, [
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
            ], "所有企业信息")

        except pymysql.Error as e:
            QMessageBox.critical(self, "错误", f"数据库操作失败: {e}", QMessageBox.Ok)

    def show_all_bank_accounts(self):
        try:
            cur = self.db.cursor()
            sql = "SELECT * FROM BankAccount"
            cur.execute(sql)
            results = cur.fetchall()
            cur.close()

            self.show_data_in_table(results, [
                "ID",
                "银行名称",
                "余额",
                "最大月支出",
                "注册日期",
                "电话号码",
                "账号",
                "密码",
                "营业执照号",
            ], "所有银行账户信息")
        except pymysql.Error as e:
            QMessageBox.critical(self, "错误", f"数据库操作失败: {e}", QMessageBox.Ok)

    def show_data_in_table(self, data, headers, window_title):
        query_window = QDialog(self)
        query_window.setWindowTitle(window_title)
        query_layout = QVBoxLayout(query_window)

        table_widget = QTableWidget(query_window)
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                table_widget.setItem(row_index, col_index, item)
        query_layout.addWidget(table_widget)
        query_window.exec_()


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("bank.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )  # Replace "bank.png" if needed
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: #333333;")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 80, 341, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 210, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(340, 210, 231, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(180, 290, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: white;")
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(340, 290, 231, 41))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.radioButton1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton1.setGeometry(QtCore.QRect(250, 360, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton1.setFont(font)
        self.radioButton1.setStyleSheet("color: white;")
        self.radioButton1.setObjectName("radioButton1")
        self.radioButton1.setText("企业登录")
        self.radioButton1.setChecked(True)
        self.radioButton2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton2.setGeometry(QtCore.QRect(410, 360, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton2.setFont(font)
        self.radioButton2.setStyleSheet("color: white;")
        self.radioButton2.setObjectName("radioButton2")
        self.radioButton2.setText("银行账户登录")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 430, 93, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 430, 93, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect signals and slots
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.clear_inputs)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "企业网银系统"))
        self.label.setText(_translate("MainWindow", "企业网银登录系统"))
        self.label_2.setText(_translate("MainWindow", "账号/许可证号："))
        self.label_3.setText(_translate("MainWindow", "                    密码："))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.pushButton_2.setText(_translate("MainWindow", "重置"))

    def login(self):
        account = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # 检查管理员账户
        if account == "root" and password == "root":
            try:
                self.db = pymysql.connect(
                    host="localhost",
                    port=3306,
                    user="root",
                    password="root",
                    database="zhenghang",
                    charset="utf8",
                )
                self.admin_window = AdminWindow(self.db)
                self.admin_window.show()
                self.hide()
                return
            except pymysql.Error as e:
                QMessageBox.critical(self, "错误", f"数据库连接失败: {e}", QMessageBox.Ok)
            return

        if account == "" or password == "":
            QMessageBox.warning(self, "警告", "账号和密码不能为空!", QMessageBox.Yes)
            return

        try:
            self.db = pymysql.connect(
                host="localhost",
                port=3306,
                user="root",
                password="root",
                database="zhenghang",
                charset="utf8",
            )
            cur = self.db.cursor()

            if self.radioButton1.isChecked():
                # 企业登录 - 从 EnterpriseInformation 表查询
                sql = (
                    f"SELECT * FROM EnterpriseInformation WHERE Account='%s' AND Password='%s'" % (account, password)
                )
            else:
                # 银行账户登录 - 使用 Business_License_Number 和 Password 查询
                sql = (
                    f"SELECT * FROM BankAccount WHERE Business_License_Number = '{account}' AND Password = '{password}'"
                )

            cur.execute(sql)
            result = cur.fetchone()

            if result:
                # 登录成功
                QMessageBox.information(self, "提示", "登录成功！", QMessageBox.Yes)

                if self.radioButton1.isChecked():
                    # 企业登录成功，跳转到 EnterpriseWindow
                    self.enterprise_window = EnterpriseWindow(result)
                    self.enterprise_window.show()
                    self.hide()  # 隐藏登录窗口
                else:
                    # 银行账户登录成功 - 查询该企业的所有银行账户
                    license_number = account
                    sql = f"SELECT * FROM BankAccount WHERE Business_License_Number = '{license_number}'"
                    cur.execute(sql)
                    all_accounts = cur.fetchall()  # 获取所有匹配的账户
                    self.bank_account_window = BankAccountWindow(all_accounts)  # 将所有账户数据传递给 BankAccountWindow
                    self.bank_account_window.show()
                    self.hide()  # 隐藏登录窗口

            else:
                # 账号或密码错误
                QMessageBox.warning(self, "警告", "账号或密码错误！", QMessageBox.Yes)

        except pymysql.Error as e:
            QMessageBox.critical(self, "错误", f"数据库连接失败: {e}", QMessageBox.Ok)
        finally:
            cur.close()  # 关闭游标
            self.db.close()  # 关闭数据库连接

    def clear_inputs(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())