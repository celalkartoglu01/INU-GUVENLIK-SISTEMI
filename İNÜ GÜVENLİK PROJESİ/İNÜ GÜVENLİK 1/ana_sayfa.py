# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'anasayfa.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(996, 715)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-10, -40, 1011, 761))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Adsız.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setGeometry(QtCore.QRect(270, 100, 96, 0))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(270, 20, 491, 41))
        self.label_7.setObjectName("label_7")
        self.splitter_5 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_5.setGeometry(QtCore.QRect(120, 90, 781, 541))
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName("splitter_5")
        self.splitter_3 = QtWidgets.QSplitter(self.splitter_5)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.misafirgiris = QtWidgets.QPushButton(self.splitter_3)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../xampp/htdocs/İNÜ GÜVENLİK/guest.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.misafirgiris.setIcon(icon)
        self.misafirgiris.setObjectName("misafirgiris")
        self.ogrencigiris = QtWidgets.QPushButton(self.splitter_3)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../../../../xampp/htdocs/İNÜ GÜVENLİK/student-thin.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ogrencigiris.setIcon(icon1)
        self.ogrencigiris.setObjectName("ogrencigiris")
        self.akademisyengiris = QtWidgets.QPushButton(self.splitter_3)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../../../../xampp/htdocs/İNÜ GÜVENLİK/professor.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.akademisyengiris.setIcon(icon2)
        self.akademisyengiris.setObjectName("akademisyengiris")
        self.splitter_4 = QtWidgets.QSplitter(self.splitter_5)
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.misafircikis = QtWidgets.QPushButton(self.splitter_4)
        self.misafircikis.setIcon(icon)
        self.misafircikis.setObjectName("misafircikis")
        self.ogrencicikis = QtWidgets.QPushButton(self.splitter_4)
        self.ogrencicikis.setIcon(icon1)
        self.ogrencicikis.setObjectName("ogrencicikis")
        self.akademisyencikis = QtWidgets.QPushButton(self.splitter_4)
        self.akademisyencikis.setIcon(icon2)
        self.akademisyencikis.setObjectName("akademisyencikis")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 996, 21))
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
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:600;\">ANA SAYFA</span></p></body></html>"))
        self.misafirgiris.setText(_translate("MainWindow", "Misafir Girişi"))
        self.ogrencigiris.setText(_translate("MainWindow", "Öğrenci Girişi"))
        self.akademisyengiris.setText(_translate("MainWindow", "Akademisyen Girişi"))
        self.misafircikis.setText(_translate("MainWindow", "Misafir Çıkışı"))
        self.ogrencicikis.setText(_translate("MainWindow", "Öğrenci Çıkışı"))
        self.akademisyencikis.setText(_translate("MainWindow", "Akademisyen Çıkışı"))
