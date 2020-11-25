# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'daq_move_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from pymodaq.daq_utils.plotting.qled import QLED
from pyqtgraph import SpinBox
from pymodaq.ressources.QtDesigner_Ressources import QtDesigner_ressources_rc


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(298, 702)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setBaseSize(QtCore.QSize(200, 300))
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_main = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_main.sizePolicy().hasHeightForWidth())
        self.groupBox_main.setSizePolicy(sizePolicy)
        self.groupBox_main.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_main.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_main.setBaseSize(QtCore.QSize(0, 0))
        self.groupBox_main.setTitle("")
        self.groupBox_main.setFlat(False)
        self.groupBox_main.setObjectName("groupBox_main")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_main)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_main)
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.Move_Done_LED = QLED(self.groupBox_main)
        self.Move_Done_LED.setObjectName("Move_Done_LED")
        self.gridLayout_2.addWidget(self.Move_Done_LED, 6, 1, 1, 1)
        self.IniStage_pb = QtWidgets.QPushButton(self.groupBox_main)
        self.IniStage_pb.setCheckable(True)
        self.IniStage_pb.setChecked(False)
        self.IniStage_pb.setObjectName("IniStage_pb")
        self.gridLayout_2.addWidget(self.IniStage_pb, 4, 0, 1, 1)
        self.Ini_state_LED = QLED(self.groupBox_main)
        self.Ini_state_LED.setObjectName("Ini_state_LED")
        self.gridLayout_2.addWidget(self.Ini_state_LED, 4, 1, 1, 1)
        self.Current_position_sb = QtWidgets.QDoubleSpinBox(self.groupBox_main)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Current_position_sb.setFont(font)
        self.Current_position_sb.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.Current_position_sb.setReadOnly(True)
        self.Current_position_sb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Current_position_sb.setDecimals(6)
        self.Current_position_sb.setMinimum(-10000000.0)
        self.Current_position_sb.setMaximum(10000000.0)
        self.Current_position_sb.setObjectName("Current_position_sb")
        self.gridLayout_2.addWidget(self.Current_position_sb, 7, 0, 1, 2)
        self.Stage_type_combo = QtWidgets.QComboBox(self.groupBox_main)
        self.Stage_type_combo.setObjectName("Stage_type_combo")
        self.gridLayout_2.addWidget(self.Stage_type_combo, 2, 1, 1, 1)
        self.title_label = QtWidgets.QLabel(self.groupBox_main)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.gridLayout_2.addWidget(self.title_label, 0, 0, 1, 2)
        self.Quit_pb = QtWidgets.QPushButton(self.groupBox_main)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/close2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Quit_pb.setIcon(icon)
        self.Quit_pb.setObjectName("Quit_pb")
        self.gridLayout_2.addWidget(self.Quit_pb, 5, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.groupBox_main)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 6, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Abs_position_sb_bis = SpinBox(self.groupBox_main)
        self.Abs_position_sb_bis.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.Abs_position_sb_bis.setDecimals(6)
        self.Abs_position_sb_bis.setMinimum(-100000000.0)
        self.Abs_position_sb_bis.setMaximum(100000000.0)
        self.Abs_position_sb_bis.setObjectName("Abs_position_sb_bis")
        self.horizontalLayout_2.addWidget(self.Abs_position_sb_bis)
        self.Moveto_pb_bis = QtWidgets.QPushButton(self.groupBox_main)
        self.Moveto_pb_bis.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/go_to_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Moveto_pb_bis.setIcon(icon1)
        self.Moveto_pb_bis.setObjectName("Moveto_pb_bis")
        self.horizontalLayout_2.addWidget(self.Moveto_pb_bis)
        self.Moveto_pb_bis_2 = QtWidgets.QPushButton(self.groupBox_main)
        self.Moveto_pb_bis_2.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/go_to_2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Moveto_pb_bis_2.setIcon(icon2)
        self.Moveto_pb_bis_2.setObjectName("Moveto_pb_bis_2")
        self.horizontalLayout_2.addWidget(self.Moveto_pb_bis_2)
        self.fine_tuning_pb = QtWidgets.QPushButton(self.groupBox_main)
        self.fine_tuning_pb.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Add_Step.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fine_tuning_pb.setIcon(icon3)
        self.fine_tuning_pb.setCheckable(True)
        self.fine_tuning_pb.setObjectName("fine_tuning_pb")
        self.horizontalLayout_2.addWidget(self.fine_tuning_pb)
        self.parameters_pb = QtWidgets.QPushButton(self.groupBox_main)
        self.parameters_pb.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.parameters_pb.setIcon(icon4)
        self.parameters_pb.setCheckable(True)
        self.parameters_pb.setObjectName("parameters_pb")
        self.horizontalLayout_2.addWidget(self.parameters_pb)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.gridLayout_9.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_main)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_buttons = QtWidgets.QGridLayout()
        self.gridLayout_buttons.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_buttons.setObjectName("gridLayout_buttons")
        self.Move_Abs_pb = QtWidgets.QPushButton(self.groupBox)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Move.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Move_Abs_pb.setIcon(icon5)
        self.Move_Abs_pb.setObjectName("Move_Abs_pb")
        self.gridLayout_buttons.addWidget(self.Move_Abs_pb, 4, 1, 2, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_buttons.addWidget(self.label_3, 7, 0, 1, 1)
        self.Move_Rel_minus_pb = QtWidgets.QPushButton(self.groupBox)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/MoveDown.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Move_Rel_minus_pb.setIcon(icon6)
        self.Move_Rel_minus_pb.setObjectName("Move_Rel_minus_pb")
        self.gridLayout_buttons.addWidget(self.Move_Rel_minus_pb, 8, 1, 1, 1)
        self.Move_Rel_plus_pb = QtWidgets.QPushButton(self.groupBox)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/MoveUp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Move_Rel_plus_pb.setIcon(icon7)
        self.Move_Rel_plus_pb.setObjectName("Move_Rel_plus_pb")
        self.gridLayout_buttons.addWidget(self.Move_Rel_plus_pb, 7, 1, 1, 1)
        self.Stop_pb = QtWidgets.QPushButton(self.groupBox)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Stop_pb.setIcon(icon8)
        self.Stop_pb.setObjectName("Stop_pb")
        self.gridLayout_buttons.addWidget(self.Stop_pb, 11, 0, 1, 1)
        self.Abs_position_sb = SpinBox(self.groupBox)
        self.Abs_position_sb.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.Abs_position_sb.setDecimals(6)
        self.Abs_position_sb.setMinimum(-100000000.0)
        self.Abs_position_sb.setMaximum(100000000.0)
        self.Abs_position_sb.setObjectName("Abs_position_sb")
        self.gridLayout_buttons.addWidget(self.Abs_position_sb, 5, 0, 1, 1)
        self.Rel_position_sb = SpinBox(self.groupBox)
        self.Rel_position_sb.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.Rel_position_sb.setDecimals(6)
        self.Rel_position_sb.setMinimum(-10000000.0)
        self.Rel_position_sb.setMaximum(1000000.0)
        self.Rel_position_sb.setObjectName("Rel_position_sb")
        self.gridLayout_buttons.addWidget(self.Rel_position_sb, 8, 0, 1, 1)
        self.Get_position_pb = QtWidgets.QPushButton(self.groupBox)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Help_32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Get_position_pb.setIcon(icon9)
        self.Get_position_pb.setObjectName("Get_position_pb")
        self.gridLayout_buttons.addWidget(self.Get_position_pb, 11, 1, 1, 1)
        self.Find_Home_pb = QtWidgets.QPushButton(self.groupBox)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/home2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Find_Home_pb.setIcon(icon10)
        self.Find_Home_pb.setObjectName("Find_Home_pb")
        self.gridLayout_buttons.addWidget(self.Find_Home_pb, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_buttons.addWidget(self.label_5, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_buttons, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.StatusBarLayout = QtWidgets.QHBoxLayout()
        self.StatusBarLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.StatusBarLayout.setObjectName("StatusBarLayout")
        self.verticalLayout.addLayout(self.StatusBarLayout)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Actuator:"))
        self.Move_Done_LED.setText(_translate("Form", "TextLabel"))
        self.IniStage_pb.setText(_translate("Form", "Initialization"))
        self.Ini_state_LED.setText(_translate("Form", "TextLabel"))
        self.Stage_type_combo.setToolTip(_translate("Form", "Stage Type"))
        self.title_label.setText(_translate("Form", "DAQ Move"))
        self.Quit_pb.setText(_translate("Form", "Quit"))
        self.label_4.setText(_translate("Form", "Current value:"))
        self.Moveto_pb_bis.setToolTip(_translate("Form", "Move to position"))
        self.Moveto_pb_bis_2.setToolTip(_translate("Form", "Move to position 2"))
        self.fine_tuning_pb.setToolTip(_translate("Form", "Show more options"))
        self.parameters_pb.setToolTip(_translate("Form", "Show connection settings"))
        self.Move_Abs_pb.setText(_translate("Form", "Set Abs"))
        self.label_3.setText(_translate("Form", "Rel increment:"))
        self.Move_Rel_minus_pb.setText(_translate("Form", "Set Rel (-)"))
        self.Move_Rel_plus_pb.setText(_translate("Form", "Set Rel (+)"))
        self.Stop_pb.setText(_translate("Form", "Stop"))
        self.Get_position_pb.setText(_translate("Form", "Update Value?"))
        self.Find_Home_pb.setText(_translate("Form", "Find Home"))
        self.label_5.setText(_translate("Form", "Abs value:"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
