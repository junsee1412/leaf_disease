# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/dialog_show.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.btn_close = QtWidgets.QPushButton(Dialog)
        self.btn_close.setObjectName("btn_close")
        self.gridLayout.addWidget(self.btn_close, 3, 2, 1, 1)
        self.label_disease = QtWidgets.QLabel(Dialog)
        self.label_disease.setObjectName("label_disease")
        self.gridLayout.addWidget(self.label_disease, 3, 0, 1, 1)
        self.label_display = QtWidgets.QLabel(Dialog)
        self.label_display.setObjectName("label_display")
        self.gridLayout.addWidget(self.label_display, 0, 0, 1, 3)

        self.retranslateUi(Dialog)
        self.btn_close.clicked.connect(Dialog.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Image"))
        self.btn_close.setText(_translate("Dialog", "Close"))
        self.label_disease.setText(_translate("Dialog", "TextLabel"))
        self.label_display.setText(_translate("Dialog", "TextLabel"))
