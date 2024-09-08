# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle  # Optional - if you want to use qdarkstyle later
import pymysql
from PyQt5.QtWidgets import QMainWindow, QMessageBox


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
        )  # Replace with your icon file
        MainWindow.setWindowIcon(icon)

        # Set solid background color (no transparency)
        MainWindow.setStyleSheet("background-color: #f0f0f0;")  # Light gray

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 80, 341, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 210, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.label_2.setFont(font)
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
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(340, 290, 231, 41))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")

        # Add radio buttons for login type selection
        self.radioButton1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton1.setGeometry(QtCore.QRect(250, 360, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton1.setFont(font)
        self.radioButton1.setObjectName("radioButton1")
        self.radioButton1.setText("企业登录")
        self.radioButton1.setChecked(True)  # Default to enterprise login

        self.radioButton2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton2.setGeometry(QtCore.QRect(410, 360, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton2.setFont(font)
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
            )  # Ensure correct database name
            cur = self.db.cursor()

            if self.radioButton1.isChecked():
                # Enterprise Login
                sql = f"SELECT * FROM enterprise WHERE unified_social_credit_code='{account}' AND password='{password}'"
            else:
                # Bank Account Login
                sql = f"SELECT * FROM account WHERE account_id='{account}' AND password='{password}'"

            cur.execute(sql)
            result = cur.fetchone()

            if result:
                # Successful login
                QMessageBox.information(self, "提示", "登录成功！", QMessageBox.Yes)
                # Transition to the relevant interface based on login type
            else:
                # Invalid credentials
                QMessageBox.warning(self, "警告", "账号或密码错误！", QMessageBox.Yes)

        except pymysql.Error as e:
            QMessageBox.critical(self, "错误", f"数据库连接失败: {e}", QMessageBox.Ok)

    def clear_inputs(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(
        qdarkstyle.load_stylesheet_pyqt5()
    )  # Optional: qdarkstyle
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())