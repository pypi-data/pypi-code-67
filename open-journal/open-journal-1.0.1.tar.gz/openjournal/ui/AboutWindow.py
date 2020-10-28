# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutWindow(object):
    def setupUi(self, AboutWindow):
        AboutWindow.setObjectName("AboutWindow")
        AboutWindow.resize(620, 495)
        AboutWindow.setMinimumSize(QtCore.QSize(620, 495))
        AboutWindow.setMaximumSize(QtCore.QSize(620, 495))
        self.centralwidget = QtWidgets.QWidget(AboutWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(140, 0, 331, 91))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/resources/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.info = QtWidgets.QLabel(self.centralwidget)
        self.info.setGeometry(QtCore.QRect(20, 110, 581, 341))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.info.setFont(font)
        self.info.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.info.setObjectName("info")
        AboutWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AboutWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 620, 22))
        self.menubar.setObjectName("menubar")
        AboutWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AboutWindow)
        self.statusbar.setObjectName("statusbar")
        AboutWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AboutWindow)
        QtCore.QMetaObject.connectSlotsByName(AboutWindow)

    def retranslateUi(self, AboutWindow):
        _translate = QtCore.QCoreApplication.translate
        AboutWindow.setWindowTitle(_translate("AboutWindow", "About Open Journal"))
        self.info.setText(_translate("AboutWindow", "<html><head/><body><p>Open Journal v1.0.0</p><p><br/></p><p>Simple, private, open-source journal for linux.</p><p><br/></p><p>For more information visit: </p><p><a href=\"https://github.com/Optimizer-Prime/open-journal\"><span style=\" text-decoration: underline; color:#eeeeec;\">https://github.com/Optimizer-Prime/open-journal</span></a></p><p><br/>Licensed under GPL-3.0</p><p><span style=\" color:#000000;\">Copyright 2020 Stuart Clayton</span></p></body></html>"))

import openjournal.ui.resources_rc
