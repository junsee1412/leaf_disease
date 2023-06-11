# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/app.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_App(object):
    def setupUi(self, App):
        App.setObjectName("App")
        App.resize(644, 493)
        self.centralwidget = QtWidgets.QWidget(App)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.linePath = QtWidgets.QLineEdit(self.groupBox)
        self.linePath.setReadOnly(True)
        self.linePath.setObjectName("linePath")
        self.gridLayout_2.addWidget(self.linePath, 1, 0, 1, 1)
        self.btn_predict = QtWidgets.QPushButton(self.groupBox)
        self.btn_predict.setObjectName("btn_predict")
        self.gridLayout_2.addWidget(self.btn_predict, 1, 1, 1, 1)
        self.btn_directory = QtWidgets.QPushButton(self.groupBox)
        self.btn_directory.setObjectName("btn_directory")
        self.gridLayout_2.addWidget(self.btn_directory, 2, 0, 1, 2)
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 2)
        App.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(App)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 644, 31))
        self.menubar.setObjectName("menubar")
        App.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(App)
        self.statusbar.setObjectName("statusbar")
        App.setStatusBar(self.statusbar)

        self.retranslateUi(App)
        QtCore.QMetaObject.connectSlotsByName(App)

    def retranslateUi(self, App):
        _translate = QtCore.QCoreApplication.translate
        App.setWindowTitle(_translate("App", "Leaf Doctor"))
        self.btn_predict.setText(_translate("App", "Predict"))
        self.btn_directory.setText(_translate("App", "Directory"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("App", "Image"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("App", "Path"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("App", "Disease"))
