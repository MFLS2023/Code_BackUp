from PyQt5.QtWidgets import (
    QInputDialog,
    QMessageBox,
    QLineEdit,
    QPushButton,
    QDialog,
    QFormLayout,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
import pymysql

# --- 添加企业对话框 ---
class AddEnterpriseDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("添加企业")
        self.db = db

        self.layout = QFormLayout(self)
        self.fields = {}
        # 创建输入框
        for label in [
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
        ]:
            self.fields[label] = QLineEdit(self)
            self.layout.addRow(label, self.fields[label])

        # 按钮
        self.save_button = QPushButton("保存", self)
        self.save_button.clicked.connect(self.save_enterprise)
        self.layout.addRow(self.save_button)

    def save_enterprise(self):
        try:
            cur = self.db.cursor()
            # 从输入框获取数据
            data = [self.fields[label].text() for label in self.fields]
            sql = """
                INSERT INTO EnterpriseInformation 
                    (Name, Address, Contact_Person, Phone, Registered_Capital, Business_License_Number, Account, Password, Main_Business, Registration_Date) 
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, data)
            self.db.commit()

            QMessageBox.information(self, "提示", "企业添加成功!", QMessageBox.Yes)
            self.accept()

        except pymysql.Error as e:
            self.db.rollback()
            QMessageBox.critical(self, "错误", f"数据库操作失败: {e}", QMessageBox.Ok)


# --- 修改企业信息对话框 ---
class ModifyEnterpriseDialog(QDialog):
    def __init__(self, db, enterprise_data):
        super().__init__()
        self.setWindowTitle("修改企业信息")
        self.db = db
        self.enterprise_data = enterprise_data

        self.layout = QFormLayout(self)
        self.fields = {}

        field_labels = [
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
        # 创建输入框，并用现有数据填充
        for i, label in enumerate(field_labels):
            self.fields[label] = QLineEdit(self)
            self.fields[label].setText(str(enterprise_data[i]))  # 设置初始值
            self.layout.addRow(label, self.fields[label])

        self.save_button = QPushButton("保存修改", self)
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addRow(self.save_button)

    def save_changes(self):
        try:
            cur = self.db.cursor()
            # 从输入框获取数据
            data = [self.fields[label].text() for label in self.fields]
            sql = """
                UPDATE EnterpriseInformation 
                SET Name=%s, Address=%s, Contact_Person=%s, Phone=%s, 
                    Registered_Capital=%s, Business_License_Number=%s, 
                    Account=%s, Password=%s, Main_Business=%s, 
                    Registration_Date=%s 
                WHERE ID=%s
            """
            cur.execute(sql, data)
            self.db.commit()
            QMessageBox.information(self, "提示", "企业信息修改成功!", QMessageBox.Yes)
            self.accept()
        except pymysql.Error as e:
            self.db.rollback()
            QMessageBox.critical(self, "错误", f"数据库操作失败: {e}", QMessageBox.Ok)


# --- 删除企业 ---
def delete_enterprise(db, license_number, window):
    reply = QMessageBox.question(
        window,
        "确认删除",
        f"确定要删除营业执照号为 {license_number} 的企业吗？",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if reply == QMessageBox.Yes:
        try:
            cur = db.cursor()
            sql = f"DELETE FROM EnterpriseInformation WHERE Business_License_Number = '{license_number}'"
            cur.execute(sql)
            db.commit()
            QMessageBox.information(window, "提示", "企业已成功删除！", QMessageBox.Yes)
            # 更新显示
            window.update_enterprise_display()
        except pymysql.Error as e:
            db.rollback()
            QMessageBox.critical(
                window, "错误", f"数据库操作失败: {e}", QMessageBox.Ok
            )


# --- 查询企业 ---
def search_enterprise(db, window):
    license_number, ok = QInputDialog.getText(
        window, "查询企业", "请输入要查询企业的营业执照号:"
    )
    if ok and license_number:
        try:
            cur = db.cursor()
            sql = (
                f"SELECT * FROM EnterpriseInformation WHERE Business_License_Number = '{license_number}'"
            )
            cur.execute(sql)
            result = cur.fetchall()  # 使用 fetchall() 获取所有匹配结果
            cur.close()  # 关闭游标

            if result:
                # 创建一个新的窗口，用表格展示查询结果
                query_window = QDialog(window)
                query_window.setWindowTitle("查询结果")
                query_layout = QVBoxLayout(query_window)

                table_widget = QTableWidget(query_window)
                table_widget.setColumnCount(len(result[0]))
                table_widget.setHorizontalHeaderLabels(
                    [
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
                )
                table_widget.setRowCount(len(result))
                for row_index, row_data in enumerate(result):
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        table_widget.setItem(row_index, col_index, item)
                query_layout.addWidget(table_widget)
                query_window.exec_()

            else:
                QMessageBox.information(window, "提示", "未找到该企业！", QMessageBox.Yes)

        except pymysql.Error as e:
            QMessageBox.critical(
                window, "错误", f"数据库操作失败: {e}", QMessageBox.Ok
            )