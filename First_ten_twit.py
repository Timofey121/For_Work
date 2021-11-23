# -*- coding: utf8 -*-
from PyQt5 import QtWidgets, QtCore
from fpdf import FPDF
import sys
from random import randrange
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(541, 312)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(220, 0, 301, 31))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 181, 20))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 220, 91, 41))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 181, 20))
        self.label.setObjectName("label")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(220, 80, 301, 31))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_4.setGeometry(QtCore.QRect(220, 40, 301, 31))
        self.textEdit_4.setObjectName("textEdit_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 90, 141, 20))
        self.label_4.setObjectName("label_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(130, 150, 251, 41))
        self.textBrowser.setObjectName("textBrowser")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(220, 130, 51, 21))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 541, 21))
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
        self.label_2.setText(_translate("MainWindow", "Please enter the Person of internet:"))
        self.pushButton.setText(_translate("MainWindow", "Find"))
        self.label.setText(_translate("MainWindow", "Please enter the investigator\'s name:"))
        self.label_4.setText(_translate("MainWindow", "Please enter the Twitter ID:"))
        self.label_5.setText(_translate("MainWindow", "File Name"))


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.pars)

    def pars(self):
        name = self.textEdit_4.toPlainText()
        username = self.textEdit.toPlainText()
        id = self.textEdit_3.toPlainText()

        def get_html():
            final_result = []
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(options=chrome_options)

            driver.get(f'https://twitter.com/{name}')

            sleep(randrange(3, 5))

            final_result = get_data(driver.page_source)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            sleep(randrange(3, 5))

            final_result += get_data(driver.page_source)

            driver.close()
            driver.quit()

            result = []
            for post in final_result:
                if post not in result:
                    result.append(post)

            return result

        def get_data(html):
            posts_result = []
            soup = BeautifulSoup(html, 'lxml')

            posts_list = soup.findAll('div', {'class': 'none_a black'})

            return posts_list

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("times", size=30)
        pdf.cell(190, 10, txt=f"TWITTER ANALYSIS '{name}'", ln=1, align="L")

        pdf.set_font("times", size=24)
        pdf.cell(80, 25, txt=f"Analysis Information", ln=1, align="L")

        pdf.set_font("times", size=18)
        pdf.cell(110, -4, txt=f"Ivenstigator: {username}", ln=1, align="L")

        pdf.set_font("times", size=18)
        pdf.cell(85, 19, txt=f"Person of Internet: {name}", ln=1, align="L")

        pdf.set_font("times", size=18)
        pdf.cell(105, -4, txt=f"Twitter ID: {id}", ln=1, align="L")

        pdf.set_font("times", size=24)
        pdf.cell(64, 50, txt=f"Tweet Analysis", ln=1, align="L")

        pdf.set_font("times", size=14)
        x = 10
        y = 10
        final_result = get_html()
        for post in final_result:
            if len(post) > 65:
                if post[65] == ' ':
                    post = post[:65]
                elif post[66] == ' ':
                    post = post[:66]
                elif post[67] == ' ':
                    post = post[:67]
                elif post[68] == ' ':
                    post = post[:68]
                elif post[69] == ' ':
                    post = post[:69]
                elif post[70] == ' ':
                    post = post[:70]
                elif post[71] == ' ':
                    post = post[:71]
                elif post[64] == ' ':
                    post = post[:64]
            pdf.cell(x, y, txt=f"{post.split('.')[0]}...  -- {name}".replace('’', "'").replace('–', '-'),
                     ln=1, align="L")
        pdf.set_font("times", size=24)
        pdf.cell(40, 40, txt=f"Conclusion", ln=1, align="L")

        pdf.set_font("times", size=16)
        pdf.cell(10, 10, txt=f"This is the last 10 posts regarding to account https://twitter.com/{name}", ln=1,
                 align="L")
        pdf.cell(10, 10, txt=f"Twitter ID of President Biden page is --{id}", ln=1,
                 align="L")
        pdf.output("Twitter_Post.pdf").encode(encoding='utf-8', errors='ignore')
        self.textBrowser.setText('Создан файл "Twitter-Post.pdf".')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()