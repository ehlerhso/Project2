# Form implementation generated from reading ui file 'workGUI.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_WorkGUI(object):
    def setupUi(self, WorkGUI):
        WorkGUI.setObjectName("WorkGUI")
        WorkGUI.resize(400, 300)
        self.workButton = QtWidgets.QPushButton(parent=WorkGUI)
        self.workButton.setGeometry(QtCore.QRect(150, 160, 111, 81))
        self.workButton.setObjectName("workButton")
        self.timeOffGainLabel = QtWidgets.QLabel(parent=WorkGUI)
        self.timeOffGainLabel.setGeometry(QtCore.QRect(30, 260, 351, 16))
        self.timeOffGainLabel.setObjectName("timeOffGainLabel")
        self.work1hourButton = QtWidgets.QPushButton(parent=WorkGUI)
        self.work1hourButton.setGeometry(QtCore.QRect(10, 160, 111, 81))
        self.work1hourButton.setObjectName("work1hourButton")
        self.EndShiftButton = QtWidgets.QPushButton(parent=WorkGUI)
        self.EndShiftButton.setGeometry(QtCore.QRect(280, 160, 111, 81))
        self.EndShiftButton.setObjectName("EndShiftButton")
        self.shiftLabel = QtWidgets.QLabel(parent=WorkGUI)
        self.shiftLabel.setGeometry(QtCore.QRect(10, 0, 241, 31))
        self.shiftLabel.setObjectName("shiftLabel")
        self.AmountWorkedLabel = QtWidgets.QLabel(parent=WorkGUI)
        self.AmountWorkedLabel.setGeometry(QtCore.QRect(10, 110, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.AmountWorkedLabel.setFont(font)
        self.AmountWorkedLabel.setObjectName("AmountWorkedLabel")
        self.UPTwarninglabel = QtWidgets.QLabel(parent=WorkGUI)
        self.UPTwarninglabel.setGeometry(QtCore.QRect(10, 30, 291, 16))
        self.UPTwarninglabel.setObjectName("UPTwarninglabel")
        self.shiftDayLabel = QtWidgets.QLabel(parent=WorkGUI)
        self.shiftDayLabel.setGeometry(QtCore.QRect(10, 60, 101, 16))
        self.shiftDayLabel.setObjectName("shiftDayLabel")

        self.retranslateUi(WorkGUI)
        QtCore.QMetaObject.connectSlotsByName(WorkGUI)

    def retranslateUi(self, WorkGUI):
        _translate = QtCore.QCoreApplication.translate
        WorkGUI.setWindowTitle(_translate("WorkGUI", "Work GUI"))
        self.workButton.setText(_translate("WorkGUI", "WORK 5 MIN"))
        self.timeOffGainLabel.setText(_translate("WorkGUI", "every hour worked = 5 upt, 3 pto, 1 vacation"))
        self.work1hourButton.setText(_translate("WorkGUI", "WORK 1 HOUR"))
        self.EndShiftButton.setText(_translate("WorkGUI", "END SHIFT"))
        self.shiftLabel.setText(_translate("WorkGUI", "Your shift = 12 hour shift 8:00 am - 8:00 pm"))
        self.AmountWorkedLabel.setText(_translate("WorkGUI", "Amount worked today: 0"))
        self.UPTwarninglabel.setText(_translate("WorkGUI", "Lose UPT for each increment of 15 minutes you don\'t work"))
        self.shiftDayLabel.setText(_translate("WorkGUI", "Day: Thursday"))