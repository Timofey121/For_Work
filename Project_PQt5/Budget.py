import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QAction, QLabel, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sqlite3


def main():
    global con, cur

    # Подключение к БД
    con = sqlite3.connect("PyQt5.sqlite")

    # Создание курсора
    cur = con.cursor()


def return_password(login_id):
    global con, cur
    try:
        main()
        cur.execute(f"SELECT login_id, password_id FROM registaration WHERE login_id = '{login_id}'")
        rows = cur.fetchall()
        for row in rows:
            return row[1]
        con.close()
    except:
        return False


def return_login(login_id):
    global con, cur
    try:
        main()
        cur.execute(f"SELECT login_id, password_id FROM registaration WHERE login_id = '{login_id}'")
        rows = cur.fetchall()
        for row in rows:
            return row[0]
        con.close()
    except:
        return False


def add_in_registaration(login_id, password_id):
    global con, cur
    main()
    cur.execute(f"INSERT INTO registaration (login_id, password_id) VALUES ('{login_id}', '{password_id}')")
    con.commit()
    con.close()


def feedback(login_id, feedback):
    global con, cur
    main()
    cur.execute(f"INSERT INTO feedback (login_id, feedback) VALUES ('{login_id}', '{feedback}')")
    con.commit()


def return_summer(login_id):
    global con, cur
    try:
        main()
        cur.execute(f"SELECT login_id, monthly_sum FROM monthly_amount WHERE login_id = '{login_id}'")
        rows = cur.fetchall()
        for row in rows:
            return row[1]
        con.close()
    except:
        return False


def update_sum(login_id, monthly_sum):
    global con, cur
    main()
    cur.execute(
        f"UPDATE monthly_amount set monthly_sum = {monthly_sum} where login_id = '{login_id}'")
    con.commit()
    con.close()


def add_setting(login_id, monthly_sum):
    global con, cur
    main()
    cur.execute(f"INSERT INTO monthly_amount (login_id, monthly_sum) VALUES ('{login_id}', {monthly_sum})")
    con.commit()


def add_purchase(login_id, buy, summ, datta):
    global con, cur
    main()
    cur.execute(
        f"INSERT INTO purchase (login_id, buy, summ, datta) VALUES ('{login_id}', '{buy}', {summ}, '{datta}')")
    con.commit()


def return_pur(login_id, datta):
    global con, cur
    try:
        main()
        cur.execute(
            f"SELECT buy FROM purchase WHERE login_id = '{login_id}' AND datta = '{datta}'")
        rows = cur.fetchall()
        return rows
        con.close()
    except:
        return False


def return_pur_s(login_id, datta):
    global con, cur
    try:
        main()
        cur.execute(
            f"SELECT summ FROM purchase WHERE login_id = '{login_id}' AND datta = '{datta}'")
        rows = cur.fetchall()
        return rows
        con.close()
    except:
        return False


def return_sum_in_ed(login_id):
    global con, cur
    try:
        main()
        cur.execute(f"SELECT summ FROM spending_every_day WHERE login_id = '{login_id}'")
        rows = cur.fetchall()
        return rows
        con.close()
    except:
        return False


def return_sum_in_ed_p(login_id):
    global con, cur
    try:
        main()
        cur.execute(f"SELECT purchase FROM spending_every_day WHERE login_id = '{login_id}'")
        rows = cur.fetchall()
        return rows
        con.close()
    except:
        return False


def add_sum_in_ed(login_id, purchase, summ):
    global con, cur
    main()
    cur.execute(
        f"INSERT INTO spending_every_day (login_id, purchase, summ) VALUES ('{login_id}', '{purchase}', {summ})")
    con.commit()
    con.close()


def del_sum_in_ed(login_id):
    global con, cur
    main()
    cur.execute(
        f"DELETE FROM spending_every_day WHERE login_id ='{login_id}'")
    con.commit()
    con.close()


def password_level(password):
    if len(password) < 6:
        return "Слишком короткий пароль     "
    elif password.isdigit():
        return "Ненадежный пароль    "
    elif password.islower():
        return "В пароле должна быть хоть одна заглавная буква!    "
    elif password.islower():
        return "В пароле должна быть хоть одна маленькая буква!    "
    elif len(list(set(password))) <= 5:
        return 'Много повторяющихся символов       '
    else:
        return 'Надежный пароль'


dataaa = {
    'янв': 31,
    'фев': 30,
    'мар': 31,
    'апр': 30,
    'май': 31,
    'июн': 30,
    'июл': 31,
    'авг': 31,
    'сен': 30,
    'окт': 31,
    'ноя': 30,
    'дек': 31,
}


class ENTRANCE(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(573, 349)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 40, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 110, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 160, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(200, 110, 271, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(200, 160, 271, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 210, 361, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 573, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "ВХОД"))
        self.label_2.setText(_translate("MainWindow", "Логин:"))
        self.label_3.setText(_translate("MainWindow", "Пароль:"))
        self.pushButton.setText(_translate("MainWindow", "ВОЙТИ"))


class REGISTRATION(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(573, 345)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 110, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 160, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(190, 40, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(200, 110, 271, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(200, 160, 271, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 220, 361, 65))
        self.pushButton.setIcon(QIcon('reg.png'))
        self.pushButton.setIconSize(QSize(75, 75))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 573, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Логин:"))
        self.label_3.setText(_translate("MainWindow", "Пароль:"))
        self.label_4.setText(_translate("MainWindow", "Регистрация:"))


class GLAV_MAIN(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(783, 854)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(20, 10, 721, 266))
        self.calendarWidget.setObjectName("calendarWidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 380, 721, 301))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 690, 331, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 290, 701, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 310, 601, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 330, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 750, 721, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(390, 690, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 783, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "СОХРАНИТЬ"))
        self.label_2.setText(_translate("MainWindow",
                                        "Введите название покупки(для удобства)  и сумму в рублях через пробелы, пишите покупки в столбик:"))
        self.label_3.setText(_translate("MainWindow", "Пр: Макдональдс - 300"))
        self.label_4.setText(_translate("MainWindow", "      Кока-кола - 150"))
        self.pushButton_3.setText(_translate("MainWindow", "ПРОВЕРИТЬ, ЕСТЬ ЛИ ПОКУПКИ В ВЫБРАННЫЙ МНОЙ ДЕНЬ\n"
                                                           " ПРОВЕРИТЬ, УЛОЖИЛСЯ ЛИ В ДНЕВНУЮ СУММУ, ДОСТУПНО ТОЛЬКО ПОСЛЕ СОХРАНЕНИЯ"))
        self.pushButton_4.setText(_translate("MainWindow", "УДАЛИТЬ ПОКУПКИ В ЭТОТ ДЕНЬ"))


class LIST(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(190, 490, 421, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 60, 741, 411))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Список ежедневных покупок:"))
        self.pushButton.setText(_translate("MainWindow", "Сохранить"))


class Result(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 615)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 651, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 90, 751, 321))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 430, 611, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 490, 751, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "ИТОГ:"))


class SAVE(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(570, 293)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 501, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 80, 511, 31))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 130, 511, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 190, 511, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 570, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "НОВАЯ ЦЕНА:"))
        self.pushButton.setText(_translate("MainWindow", "СОХРАНИТЬ ИЗМЕНЕНИЯ"))
        self.pushButton_2.setText(_translate("MainWindow", "ВЕРНУТЬСЯ НАЗАД"))


class FEEDBACK_1(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(772, 447)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 320, 611, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(80, 20, 611, 281))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 772, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "ОСТАВИТЬ ОТЗЫВ"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


class TRAT(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(584, 276)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 541, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 100, 521, 41))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 521, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 160, 521, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 584, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Сумма на месяц с вычетам вынужденных трат(рубли):"))
        self.pushButton.setText(_translate("MainWindow", "ИЗМЕНИТЬ"))
        self.pushButton_2.setText(_translate("MainWindow", "ВЕРНУТЬСЯ НАЗАД"))


class Example(QMainWindow, ENTRANCE):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        exitAction_2 = QAction('&Регистрация', self)
        exitAction_2.triggered.connect(self.registr)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu_2 = menubar.addMenu('&Регистрация')
        fileMenu_2.addAction(exitAction_2)
        self.setWindowTitle('ВХОД')
        self.pushButton.clicked.connect(self.hello)

    def hello(self):
        global login, passw
        if return_password(self.textEdit.toPlainText().strip()) is None:
            QMessageBox.about(self, "ERROR", f"Неверный пароль или логин!\n"
                                             f"Если вы тут в первый раз, то зарегиструетесь!")
        else:
            if return_password(self.textEdit.toPlainText().strip()) == self.textEdit_2.toPlainText().strip():
                login = self.textEdit.toPlainText()
                passw = self.textEdit_2.toPlainText()
                self.close()
                self.w2 = Main()
                self.w2.show()
            else:
                QMessageBox.about(self, "ERROR", "Неверный пароль или логин!       ")

    def registr(self):
        self.close()
        self.w2 = Registr()
        self.w2.show()


class Registr(QMainWindow, REGISTRATION):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        exitAction_2 = QAction('&Вход', self)
        exitAction_2.triggered.connect(self.entrance)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu_2 = menubar.addMenu('&Вход')
        fileMenu_2.addAction(exitAction_2)
        self.setWindowTitle('РЕГИСТРАЦИЯ')
        self.pushButton.clicked.connect(self.registration)

    def entrance(self):
        self.close()
        self.w2 = Example()
        self.w2.show()

    def registration(self):
        try:
            if return_password(self.textEdit.toPlainText().strip()) is not False and \
                    return_password(self.textEdit.toPlainText().strip()) == self.textEdit_2.toPlainText().strip():
                QMessageBox.about(self, "ERROR", "Вы уже зарегистрированы!    ")
                self.close()
                self.w2 = Example()
                self.w2.show()
            else:
                if return_login(self.textEdit.toPlainText().strip()) is not None:
                    QMessageBox.about(self, "ERROR", "Такой логин занят, используете другой!    ")
                else:
                    if password_level(self.textEdit_2.toPlainText()).strip() != "Надежный пароль":
                        QMessageBox.about(self, "ERROR", f"{password_level(self.textEdit_2.toPlainText())}")
                    else:
                        with open('people.txt', 'a', encoding='utf-8') as f:
                            f.write(
                                f"Новый пользователь: login - {self.textEdit.toPlainText()}; password - {self.textEdit_2.toPlainText()}\n")
                        add_in_registaration(self.textEdit.toPlainText(), self.textEdit_2.toPlainText())
                        QMessageBox.about(self, "ERROR", "Вы успешно зарегистрированы!    ")
                        self.close()
                        self.w2 = Example()
                        self.w2.show()
        except Exception as ex:
            pass


class Main(QMainWindow, GLAV_MAIN):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        exitAction = QAction('&Настройки', self)
        exitAction.triggered.connect(self.settings)
        exitAction_1 = QAction('&Оставить отзыв', self)
        exitAction_1.triggered.connect(self.feedback)
        exitAction_2 = QAction('&Список ежедневных покупок', self)
        exitAction_2.triggered.connect(self.ed)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Настройки')
        fileMenu_1 = menubar.addMenu('&Оставить отзыв')
        fileMenu_2 = menubar.addMenu('&Список ежедневных покупок')
        fileMenu.addAction(exitAction)
        fileMenu_1.addAction(exitAction_1)
        fileMenu_2.addAction(exitAction_2)
        self.setWindowTitle('Бюджет')
        self.pushButton_2.clicked.connect(self.save)
        self.pushButton_3.clicked.connect(self.check)
        self.pushButton_4.clicked.connect(self.delete)

    def delete(self):
        self.close()
        name, ok_pressed = QInputDialog.getItem(
            self, "Удаление", "Хотите ли Вы удалить покупки в выбранный Вами день?",
            ("Да", "Нет"), 1, False)
        if ok_pressed:
            self.close()
            self.w2 = Main()
            self.w2.show()
            if name == "Да":
                try:
                    global con, cur
                    main()
                    cur.execute(
                        f"DELETE FROM purchase WHERE login_id = '{login}' AND datta = '{self.calendarWidget.selectedDate().toString()}'")
                    con.commit()
                    con.close()
                    QMessageBox.about(self, "ERROR", f"УДАЛЕНИЕ ПРОШЛО УСПЕШНО!")
                except Exception as ex:
                    QMessageBox.about(self, "ERROR", f"СЕГОДНЯ НЕ БЫЛО ПОКУПОК!")

    def ed(self):
        self.close()
        self.w2 = List()
        self.w2.show()

    def save(self):
        global login, passw, der
        l = []
        # print(return_pur(login, rt))
        a = self.textEdit.toPlainText().split("\n")
        for i in range(len(a)):
            b = a[i].split(" ")
            self.w = 0
            for j in range(len(b)):
                try:
                    self.w += int(b[j])
                    del b[j]
                except:
                    pass
            if self.w != 0:
                add_purchase(login, " ".join(b), self.w, str(self.calendarWidget.selectedDate().toString()))
        self.textEdit.clear()

    def check(self):
        global rt
        rt = self.calendarWidget.selectedDate().toString()
        self.close()
        self.w2 = RESULT()
        self.w2.show()

    def settings(self):
        self.close()
        self.w2 = SETTINGS()
        self.w2.show()

    def feedback(self):
        self.close()
        self.w2 = FEEDBACK()
        self.w2.show()


class RESULT(QMainWindow, Result):
    def __init__(self):
        global rt
        super().__init__()
        self.setupUi(self)
        exitAction_2 = QAction('&Главная страница', self)
        exitAction_2.triggered.connect(self.main_window)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu_2 = menubar.addMenu('&Главная страница')
        fileMenu_2.addAction(exitAction_2)
        self.label.setText(f"Список продуктов на {str(rt)}")
        # print(return_summer(login))
        # print(return_sum_in_ed_p(login).split("AND"))
        if return_pur(login, rt) == "[]":
            self.textEdit.setText("В этот день нет покупок")
        else:
            # print(return_summer(login))
            if return_summer(login) is None or return_summer(login) == " ":
                self.label_3.setText("Сначала введите сумму на месяц с вычетам вынужденных трат(рубли) в настройках!")
            else:
                d = []
                c = 0
                try:
                    self.w = 0
                    b = return_pur(login, rt)
                    a = return_pur_s(login, rt)
                    d = []
                    d.append("Список покупок сегодня:")
                    for i in range(len(b)):
                        self.w += int(a[i][0])
                        d.append(f'{"".join(b[i])}')
                        c += 1
                    if c == 0:
                        del d[0]
                        d.append("Сегодня не было покупок!")
                    if return_sum_in_ed(login) is not False:
                        d.append("\nСписок постоянных покупок:")
                        a = return_sum_in_ed(login)
                        b = return_sum_in_ed_p(login)
                        for i in range(len(b)):
                            d.append(f'{"".join(b[i])}')
                            self.w += int(a[i][0])

                    d.append("\nСумма, потраченная сегодня:")
                    d.append(str(self.w))
                    self.textEdit.setText("\n".join(d))

                    self.fgh = (int(return_summer(login)) / int(dataaa[rt.split(" ")[1]])) - self.w

                    if self.fgh > 0:
                        self.label_3.setText('Сегодня Вы сэкономили +' + str(self.fgh))
                        self.label_3.setStyleSheet("background-color: lightgreen")
                    else:
                        if self.fgh == 0:
                            self.label_3.setText('Сегодня Вы потратили ровно дневную сумму')
                        else:
                            self.label_3.setText('Сегодня Вы потратили лишнего, на ' + str(self.fgh))
                            self.label_3.setStyleSheet("background-color: #FF0000")

                except Exception as ex:
                    pass

    def main_window(self):
        self.close()
        self.w2 = Main()
        self.w2.show()


class FEEDBACK(QMainWindow, FEEDBACK_1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        exitAction_2 = QAction('&Главная страница', self)
        exitAction_2.triggered.connect(self.main_window)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu_2 = menubar.addMenu('&Главная страница')
        fileMenu_2.addAction(exitAction_2)
        self.setWindowTitle('Список ежедневных покупок')
        self.setWindowTitle('ОТЗЫВ')
        self.pushButton.clicked.connect(self.rtyu)

    def main_window(self):
        self.close()
        self.w2 = Main()
        self.w2.show()

    def rtyu(self):
        global login, passw
        try:
            feedback(login, self.textEdit.toPlainText())
            self.close()
            self.w2 = Main()
            self.w2.show()
        except Exception as ex:
            pass


class List(QMainWindow, LIST):
    def __init__(self):
        global login, passw
        super().__init__()
        self.setupUi(self)
        exitAction_2 = QAction('&Главная страница', self)
        exitAction_2.triggered.connect(self.main_window)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu_2 = menubar.addMenu('&Главная страница')
        fileMenu_2.addAction(exitAction_2)
        self.setWindowTitle('Список ежедневных покупок')
        self.pushButton.clicked.connect(self.rtu)
        if str(return_sum_in_ed(login)) != '[]':
            try:
                d = []
                a = return_sum_in_ed(login)
                b = return_sum_in_ed_p(login)
                for i in range(len(b)):
                    if int(a[i][0]) != 0:
                        d.append(f'{"".join(b[i])} {int(a[i][0])}')
                self.textEdit.setText("\n".join(d))
            except Exception as ex:
                print(ex)
        else:
            self.textEdit.setText("ПУСТО!!!")

    def main_window(self):
        self.close()
        self.w2 = Main()
        self.w2.show()

    def rtu(self):
        global login, passw, der
        l = []
        del_sum_in_ed(login)
        a = self.textEdit.toPlainText().split("\n")
        for i in range(len(a)):
            b = a[i].split(" ")
            self.w = 0
            for j in range(len(b)):
                try:
                    self.w += int(b[j])
                    del b[j]
                except:
                    pass
            if self.w != 0:
                add_sum_in_ed(login, " ".join(b), self.w)
        self.close()
        self.w2 = Main()
        self.w2.show()


class SETTINGS(QMainWindow, TRAT):
    def __init__(self):
        global login, passw
        super().__init__()
        self.setupUi(self)
        exitAction_2 = QAction('&Главная страница', self)
        exitAction_2.triggered.connect(self.main_window)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu_2 = menubar.addMenu('&Главная страница')
        fileMenu_2.addAction(exitAction_2)
        self.setWindowTitle('Список ежедневных покупок')
        self.setWindowTitle('ПРОВЕРИТЬ СУММУ')
        self.pushButton.clicked.connect(self.sum)
        self.pushButton_2.clicked.connect(self.sumwer)
        if return_summer(login) is None:
            self.label_2.setText('0' + ' P')
        else:
            self.label_2.setText(str(return_summer(login)) + " P")

    def main_window(self):
        self.close()
        self.w2 = Main()
        self.w2.show()

    def sum(self):
        self.close()
        self.w2 = SETT()
        self.w2.show()

    def sumwer(self):
        self.close()
        self.w2 = Main()
        self.w2.show()


class SETT(QMainWindow, SAVE):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('ИЗМЕНЕНИЕ СУММЫ')  # Устанавливаем название окна
        self.pushButton.clicked.connect(self.su)  # Вызов функции su принажатии на pushButton
        self.pushButton_2.clicked.connect(self.sure)  # Вызов функции sure принажатии на pushButton_2

    def su(self):  # сама функция su
        global login, passw  # вызов глобальных переменных
        if return_summer(login) != None:  # проверка на наличие суммы в месяц в БД
            update_sum(login, int(self.textEdit.toPlainText()))  # если да, то обновляем это значение
        else:
            add_setting(login, int(self.textEdit.toPlainText()))  # иначе, добавляем
        self.close()  # закрываем это окно
        self.w2 = Main()  # октрываем главное окно
        self.w2.show()  # делаем его видимым

    def sure(self):  # сама функция sure
        self.close()  # закрываем это окно
        self.w2 = SETTINGS()  # октрываем меню с настройками
        self.w2.show()  # октрываем главное окно


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
