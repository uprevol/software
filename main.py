import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QDialog, QTableWidgetItem, QHeaderView
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem
from PyQt5.uic import loadUi
import images
import time
from qdictionarytree import DictionaryTreeDialog
import mysql.connector
from sql_q import sql_queries
import sql_q
import keyring

WINDOW_SIZE = 0
global adm_id, username, password, c, name, short_name, dash, rev, sus_d, sus_h, ver_d, ver_h, del_d, del_h

mydb = mysql.connector.connect(
    host="database-1.ck38lmrgzjqj.us-east-2.rds.amazonaws.com",
    user="admin",
    password="uprevol1234",
    database="uprevol"
)


class Login(QMainWindow):
    def __init__(self):
        global username, password, adm_id, c
        super(Login, self).__init__()
        loadUi('login.ui', self)
        self.sql_class = sql_queries()
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.pushButton.clicked.connect(self.dologin)
        if self.check_login():
            c = 1
            self.dologin()
        else:
            self.show()
            c = 0

    def check_login(self):
        global username, password
        try:
            username = keyring.get_password('uprevol', 'username')
            password = keyring.get_password('uprevol', 'password')
            if (username and password) is None:
                return False
            return True
        except:
            return False

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.dologin()

    def dologin(self):
        global username, password, adm_id, c, name, short_name
        if c == 0:
            username = self.email.text()
            password = self.password.text()
        y = self.sql_class.login(username, password)
        print(y)
        if "success" in y['result']:
            adm_id = y['adm_id']
            name = y['name']
            sname = name.split(" ")
            fname = list(sname[0])[0]
            try:
                lname = list(sname[1])[0]
                short_name = fname + lname
            except:
                short_name = fname
            keyring.set_password('uprevol', 'username', username)
            keyring.set_password('uprevol', 'password', password)
            self.label_2.setText("Loading...")
            self.runit()
        else:
            self.show()
            c = 0
            if "" == (self.email.text() or self.password.text()):
                self.error.setText("Type Email or Password")
            elif "@" in self.email.text():
                self.error.setText("Wrong Email or Password")
            else:
                self.error.setText("Invalid Email Id")

    def runit(self):
        self.main = Main()
        self.main.show()
        self.close()


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('Dashboard.ui', self)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.label_8.setText(short_name.upper())
        self.sql_class = sql_queries()
        self.sql_data()
        self.show()
        self.btn_close.clicked.connect(lambda: self.close())
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_maximize_restore.clicked.connect(lambda: self.window_size())
        self.pushButton_7.clicked.connect(self.verification_view)
        self.pushButton_9.clicked.connect(self.runit)
        self.pushButton_11.clicked.connect(self.suspicious_view)
        self.pushButton_12.clicked.connect(self.researh_view)
        self.pushButton_3.clicked.connect(self.show_action)
        self.pushButton_5.clicked.connect(self.show_action)
        self.pushButton_20.clicked.connect(self.show_verify)
        self.btn_toggle_menu.clicked.connect(self.menu)
        self.pushButton_5.clicked.connect(self.research)
        self.pushButton_16.clicked.connect(self.pass_to_admin)
        self.pushButton_19.clicked.connect(self.pass_to_admin)
        self.pushButton_21.clicked.connect(self.pass_to_admin)
        self.pushButton_18.clicked.connect(self.done_ver)
        self.pushButton_2.clicked.connect(self.done_sus)
        self.pushButton_6.clicked.connect(self.reload_data)
        # self.pushButton_4.clicked.connect(self.done_del)
        self.pushButton_10.clicked.connect(self.delete_view)
        self.pushButton_8.clicked.connect(self.support_view)
        self.dashboard()
        self.review()


        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        self.frame_label_top_btns.mouseMoveEvent = moveWindow
        self.frame_grip.mouseMoveEvent = moveWindow

    def reload_data(self):
        print("0")
        self.progressBar.setValue(0)
        print("0")
        self.sql_data()
        self.progressBar.setValue(100)


    def dashboard(self):
        global dash
        result = dash
        self.label.setText(str(result[0][0])+" / ")
        self.label_2.setText(str(result[0][1])+" / ")
        self.label_3.setText(str(result[0][2]) + " / ")
        self.label_16.setText(str(result[0][3]))
        self.label_18.setText(str(result[0][4]))
        self.label_20.setText(str(result[0][5]))
        self.label_5.setText(str(result[0][6])+" / ")
        self.label_6.setText(str(result[0][7])+" / ")
        self.label_7.setText(str(result[0][8]) + " / ")
        self.label_17.setText(str(result[0][9]))
        self.label_19.setText(str(result[0][10]))
        self.label_21.setText(str(result[0][11]))

    def window_size(self):
        if self.btn_maximize_restore.isChecked():
            self.restore_or_maximize_window()
            self.btn_maximize_restore.setStyleSheet("QPushButton {	border: none; background-position: center; background-color: transparent; background-image: url(:/16x16/icons/16x16/cil-window-restore.png);  background-repeat: no-repeat; } QPushButton:hover { background-color: rgb(52, 59, 72); } QPushButton:pressed {background-color: rgb(85, 170, 255); }")
        else:
            self.restore_or_maximize_window()
            self.btn_maximize_restore.setStyleSheet(
                "QPushButton {	border: none; background-position: center; background-color: transparent; background-image: url(:/16x16/icons/16x16/cil-window-maximize.png);  background-repeat: no-repeat; } QPushButton:hover { background-color: rgb(52, 59, 72); } QPushButton:pressed {background-color: rgb(85, 170, 255); }")

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def restore_or_maximize_window(self):
        global WINDOW_SIZE
        win_status = WINDOW_SIZE
        if win_status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
        else:
            WINDOW_SIZE = 0
            self.showNormal()

    def menu(self):
        global name, short_name
        if self.btn_toggle_menu.isChecked():
            self.frame_left_menu.setMaximumWidth(140)
            self.frame_toggle.setMaximumWidth(126)
            self.label_8.setText(name.capitalize())
        else:
            self.label_8.setText(short_name.upper())
            self.frame_left_menu.setMaximumWidth(60)
            self.frame_toggle.setMaximumWidth(60)

    def show_verify(self):
        self.verify = verification_widget()
        self.verify.show()

    def pass_to_admin(self):
        self.dialog = pass_to_admin(self.stackedWidget.currentIndex(), self.lineEdit_4.text())

    def show_action(self):
        if self.pushButton_3.isChecked():
            self.stackedWidget_2.setMaximumHeight(150)
        else:
            self.stackedWidget_2.setMaximumHeight(0)

    def researh_view(self):
        if self.pushButton_12.isChecked():
            self.stack_change()
            self.frame_20.setMaximumHeight(70)
            self.pushButton_12.setStyleSheet("background-image: url(:/16x16/icons/16x16/cil-minus.png);")
            self.frame_26.setStyleSheet("background-color: rgb(44, 49, 60);")
        else:
            self.frame_20.setMaximumHeight(0)
            self.pushButton_3.setChecked(False)
            self.show_action()
            self.stackedWidget.setMaximumHeight(16777215)
            self.pushButton_12.setStyleSheet("background-image: url(:/16x16/icons/16x16/cil-plus.png);")
            self.frame_26.setStyleSheet("background-color: rgb(27, 29, 35);")

    def stack_change(self):
        self.stackedWidget_2.setCurrentIndex(self.stackedWidget.currentIndex() - 2)

    def suspicious_view(self):
        if self.pushButton_11.isChecked():
            self.pushButton_7.setChecked(False)
            self.pushButton_10.setChecked(False)
            self.pushButton_8.setChecked(False)
            self.stackedWidget.setCurrentIndex(2)
            self.frame_21.setStyleSheet("background-color: rgb(44, 49, 60);")
            self.frame_22.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.frame_23.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.frame_24.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.stack_change()
            self.suspicious_table()
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.frame_21.setStyleSheet("background-color: rgb(27, 29, 35);")

    def verification_view(self):
        if self.pushButton_7.isChecked():
            self.pushButton_11.setChecked(False)
            self.pushButton_10.setChecked(False)
            self.pushButton_8.setChecked(False)
            self.stackedWidget.setCurrentIndex(3)
            self.frame_22.setStyleSheet("background-color: rgb(44, 49, 60);")
            self.frame_21.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.frame_23.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.frame_24.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.stack_change()
            self.verification_table()
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.frame_22.setStyleSheet("background-color: rgb(27, 29, 35);")

    def delete_view(self):
        if self.pushButton_10.isChecked():
            self.pushButton_7.setChecked(False)
            self.pushButton_11.setChecked(False)
            self.pushButton_8.setChecked(False)
            self.stackedWidget.setCurrentIndex(4)
            self.frame_23.setStyleSheet("background-color: rgb(44, 49, 60);")
            self.frame_22.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.frame_21.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.frame_24.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.stack_change()
            self.delete_table()
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.frame_23.setStyleSheet("background-color: rgb(27, 29, 35);")

    def support_view(self):
        if self.pushButton_8.isChecked():
            self.pushButton_7.setChecked(False)
            self.pushButton_11.setChecked(False)
            self.pushButton_10.setChecked(False)
            self.stackedWidget.setCurrentIndex(5)
            self.frame_24.setStyleSheet("background-color: rgb(44, 49, 60);")
            self.frame_22.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.frame_21.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.frame_23.setStyleSheet("background-color: rgb(27, 29, 35);")
            self.stack_change()
            self.widget.setUrl(QtCore.QUrl(f"https://app.hubspot.com/live-messages/20309523/inbox/"))
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.frame_24.setStyleSheet("background-color: rgb(27, 29, 35);")

    def sql_data(self):
        global dash, rev, sus_d, sus_h, ver_d, ver_h, del_d, del_h, adm_id
        sql_q.mydb_func()
        self.progressBar.setValue(5)
        dash = self.sql_class.dashboard(adm_id)
        self.progressBar.setValue(10)
        rev = self.sql_class.review(adm_id)
        self.progressBar.setValue(15)
        sus_d = self.sql_class.sus_display(adm_id)
        self.progressBar.setValue(20)
        sus_h = self.sql_class.sus_history(adm_id)
        self.progressBar.setValue(25)
        ver_d = self.sql_class.ver_display(adm_id)
        self.progressBar.setValue(30)
        ver_h = self.sql_class.ver_history(adm_id)
        self.progressBar.setValue(35)
        del_d = self.sql_class.del_display(adm_id)
        self.progressBar.setValue(40)
        del_h = self.sql_class.del_history(adm_id)
        self.progressBar.setValue(45)
        self.dashboard()
        self.progressBar.setValue(50)
        self.suspicious_table()
        self.progressBar.setValue(60)
        self.verification_table()
        self.progressBar.setValue(70)
        self.delete_table()
        self.progressBar.setValue(80)
        self.review()
        self.progressBar.setValue(100)

    def suspicious_table(self):
        global sus_d, sus_h
        # rows_dic = self.sql_class.sus_display(adm_id)
        colm_names = ['SN', 'ID', 'Recruiter', 'Worker', 'Message', "Assigned Date", "Review Message"]
        self.tableWidget_2.setRowCount(len(sus_d))
        self.tableWidget_2.setColumnCount(len(colm_names))
        self.tableWidget_2.setHorizontalHeaderLabels(colm_names)
        self.tableWidget_2.horizontalHeader().setMinimumSectionSize(100)
        row = 0
        for x2 in sus_d:
            colm1 = 0
            for x3 in x2:
                self.tableWidget_2.setItem(row, colm1, QTableWidgetItem(str(x3)))
                colm1 += 1
            row += 1
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # rows_dic = self.sql_class.sus_history(adm_id)
        colm_names = ['SN', 'ID', 'Recruiter', 'Worker', 'Notes',
                      'User Message', 'Passed Note', "Passed Date", "Action", "Action Date"]
        self.tableWidget_5.setRowCount(len(sus_h))
        self.tableWidget_5.setColumnCount(len(colm_names))
        self.tableWidget_5.setHorizontalHeaderLabels(colm_names)
        self.tableWidget_5.horizontalHeader().setMinimumSectionSize(100)
        row = 0
        for x2 in sus_h:

            colm1 = 0
            for x3 in x2:
                self.tableWidget_5.setItem(row, colm1, QTableWidgetItem(str(x3)))
                colm1 += 1
            row += 1
        self.tableWidget_5.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_5.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def review(self):
        global rev
        # rows_dic = self.sql_class.review(adm_id)
        colm_names = ["ID", "Review Message"]
        self.tableWidget_7.setRowCount(len(rev))
        self.tableWidget_7.setColumnCount(len(colm_names))
        self.tableWidget_7.setHorizontalHeaderLabels(colm_names)
        self.tableWidget_7.horizontalHeader().setMinimumSectionSize(100)
        row = 0
        for x2 in rev:
            colm1 = 0
            for x3 in x2:
                self.tableWidget_7.setItem(row, colm1, QTableWidgetItem(str(x3)))
                colm1 += 1
            row += 1
        self.tableWidget_7.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_7.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def verification_table(self):
        global ver_d, ver_h
        # rows_dic = self.sql_class.ver_display(adm_id)
        colm_names = ['SN', 'ID', 'Worker', 'Message', "Assigned Date", "Review Message"]
        self.tableWidget_3.setRowCount(len(ver_d))
        self.tableWidget_3.setColumnCount(len(colm_names))
        self.tableWidget_3.setHorizontalHeaderLabels(colm_names)
        self.tableWidget_3.horizontalHeader().setMinimumSectionSize(100)
        row = 0
        for x2 in ver_d:

            colm1 = 0
            for x3 in x2:
                self.tableWidget_3.setItem(row, colm1, QTableWidgetItem(str(x3)))
                colm1 += 1
            row += 1
        self.tableWidget_3.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # rows_dic = self.sql_class.ver_history(adm_id)
        colm_names = ['SN', 'ID', 'Worker', 'Notes', 'User Message', 'Passed Note', "Passed Date", "Action", "Action Date"]
        self.tableWidget_6.setRowCount(len(ver_h))
        self.tableWidget_6.setColumnCount(len(colm_names))
        self.tableWidget_6.setHorizontalHeaderLabels(colm_names)
        self.tableWidget_6.horizontalHeader().setMinimumSectionSize(100)
        row = 0
        for x2 in ver_h:

            colm1 = 0
            for x3 in x2:
                self.tableWidget_6.setItem(row, colm1, QTableWidgetItem(str(x3)))
                colm1 += 1
            row += 1
        self.tableWidget_6.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_6.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def delete_table(self):
        global del_d, del_h
        # rows_dic = self.sql_class.del_display(adm_id)
        colm_names = ['SN', 'ID', 'Recruiter', 'Worker', 'Message', "Assigned Date", "Review Message"]
        self.tableWidget_4.setRowCount(len(del_d))
        self.tableWidget_4.setColumnCount(len(colm_names))
        self.tableWidget_4.setHorizontalHeaderLabels(colm_names)
        self.tableWidget_4.horizontalHeader().setMinimumSectionSize(100)
        row = 0
        for x2 in del_d:
            colm1 = 0
            for x3 in x2:
                self.tableWidget_4.setItem(row, colm1, QTableWidgetItem(str(x3)))
                colm1 += 1
            row += 1
        self.tableWidget_4.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # rows_dic = self.sql_class.del_history(adm_id)
        colm_names = ['SN', 'ID', 'Recruiter', 'Worker', 'Notes', 'User Message', 'Passed Note', "Passed Date", "Action", "Action Date"]
        self.tableWidget_8.setRowCount(len(del_h))
        self.tableWidget_8.setColumnCount(len(colm_names))
        self.tableWidget_8.setHorizontalHeaderLabels(colm_names)
        self.tableWidget_8.horizontalHeader().setMinimumSectionSize(100)
        row = 0
        for x2 in del_h:
            colm1 = 0
            for x3 in x2:
                self.tableWidget_8.setItem(row, colm1, QTableWidgetItem(str(x3)))
                colm1 += 1
            row += 1
        self.tableWidget_8.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_8.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def research(self):
        self.pushButton_12.setCheckable(True)
        self.researh_view()
        rows_dic = self.sql_class.build_tree(self.lineEdit_4.text())
        print(rows_dic)
        tree = DictionaryTreeDialog(rows_dic)
        tree.edit()

    def done_ver(self):
        vid = self.lineEdit_4.text()
        message_to_user = self.textEdit_3.toPlainText()
        message = self.textEdit_4.toPlainText()
        ver_status = self.comboBox_4.currentIndex()
        self.sql_class.ver_action(ver_status, message, message_to_user, vid)

    def done_sus(self):
        sid = self.lineEdit_4.text()
        message_to_user = self.textEdit_2.toPlainText()
        message = self.textEdit.toPlainText()
        action = f"{self.comboBox_3.currentIndex()}-{self.comboBox_2.currentIndex()}"
        self.sql_class.sus_action(sid, message, message_to_user, action)

    def runit(self):
        keyring.delete_password('uprevol', 'username')
        keyring.delete_password('uprevol', 'password')
        self.main = Login()
        self.main.show()
        self.close()


class verification_widget(QDialog):
    def __init__(self):
        super(verification_widget, self).__init__()
        loadUi('verification-widget.ui', self)
        self.setWindowTitle("Consent Form")
        self.show()


class pass_to_admin(QDialog):
    def __init__(self, stack_index, uid):
        super(pass_to_admin, self).__init__()
        loadUi('pass_to_admin.ui', self)
        self.setWindowTitle("Pass to Admin")
        self.show()
        self.sql_class = sql_queries()
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(lambda: self.passed(stack_index, uid))

    def passed(self, stack_index, uid):
        note = self.textEdit.toPlainText()
        if stack_index == 0:
            self.sql_class.sus_passed(uid, note)
        elif stack_index == 1:
            self.sql_class.ver_passed(uid, note)
        else:
            self.sql_class.del_passed(uid, note)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()

    sys.exit(app.exec_())

# app = QtWidgets.QApplication(sys.argv)
# window = Login()
# widget=QtWidgets.QStackedWidget()
# widget.addWidget(window)
# widget.setFixedHeight(300)
# widget.setFixedWidth(300)
# widget.show()
# app.exec_()