import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pymysql

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录')
        self.setGeometry(100, 100, 600, 300)  # 设置窗口大小

        # 设置字体
        font = QFont('Arial', 16)

        # 标题
        self.title_label = QLabel('登录到您的帐户', self)
        self.title_label.setFont(QFont('Arial', 24))
        self.title_label.setAlignment(Qt.AlignCenter)

        # 账号输入框和标签
        self.username_label = QLabel('账号', self)
        self.username_label.setFont(font)
        self.username_input = QLineEdit(self)
        self.username_input.setFont(font)
        self.username_input.setPlaceholderText('请输入账号')

        # 密码输入框和标签
        self.password_label = QLabel('密码', self)
        self.password_label.setFont(font)
        self.password_input = QLineEdit(self)
        self.password_input.setFont(font)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('请输入密码')

        # 登录按钮
        self.login_button = QPushButton('登录', self)
        self.login_button.setFont(font)
        self.login_button.clicked.connect(self.handle_login)

        # 创建布局
        main_layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.addWidget(self.title_label)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.login_button)
        button_layout.addStretch(1)

        # 添加到主布局
        main_layout.addLayout(title_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(form_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.validate_login(username, password):
            QMessageBox.information(self, '成功', '登录成功')
        else:
            QMessageBox.warning(self, '错误', '账号或密码错误')

    def validate_login(self, username, password):
        # Database connection
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='zhenghang',
            charset='utf8'
        )
        cursor = connection.cursor()

        # Query to check if username and password match
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            return True
        else:
            return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
