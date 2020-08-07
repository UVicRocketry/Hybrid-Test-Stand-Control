# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hybrid_test_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

# CONTRIBUTORS: KRISTOPHER LEMEIUX
# PROJECT: ROCKTRY Hybrid Engine Test GUI

# VALUES FOR TESTING:(LEGEND)

# Nitrogen Flow VALVE (N2F) [ON/OFF]
# Nitesos Oxide Flow VALVE (N20F) [ON/OFF]
# Main Engine VALVE (MEV) [ON/OFF]
# Normally closed VALVE (NCV) [Toggle]
# Vent VALVE (VV) [ON/OFF]
# Relief VALVE (RV) [ON/OFF]
# Ignitor (IG) [Toggle]

# once button press is received

# ----------------------------------------------------NOTES:------------------------------------------------------------
#
# 1. Ignore errors in console with unknown property - code still runs perfectly fine those are for converting the
#    generation into code.
#
# 2. The class Ui_MainWindow first method is creating the objects that are displayed on the gui. SetupUI Follows a
#    pattern of creating the instance of the object from PyQt5, styling it, positioning it, maybe giving calling another
#    method when interacted with ie: ".clicked.connect(function call)". The method set_connection() had definition in it
#    originally which is syntactically OK however I ran into errors with scope so I moved the definitions outside and
#    changed them to calls.
#
# 3. Class ReceivedThread is an older class adapted to encompass new methods, some of which include functionality:
#    N2F, and N20F.
#
# 4.
#
#
#------------------------------------------------------------------------------------------------------------------------------#

from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import re
import datetime
from PyQt5.QtWidgets import QMessageBox

_AUTO_TEST_ENABLED = False


# ---------------------------------------------------#
#             Class: ReceiveThread                   #
#                                                    #
# Takes input from pi and process's them as commands #
#                                                    #
# ---------------------------------------------------#
class ReceiveThread(QtCore.QThread):
    conn_lost = QtCore.pyqtSignal(object)
    msg_received = QtCore.pyqtSignal(object)
    limit_state_received = QtCore.pyqtSignal(int, int, int, int, int, int, int, int, int, int)
    ignitor_state_received = QtCore.pyqtSignal(int)
    nc_valve_state_received = QtCore.pyqtSignal(int)

    lockout_state_received = QtCore.pyqtSignal(int)

    
    def __init__(self, sock):
        QtCore.QThread.__init__(self)
        self.sock = sock
        self.char_stream = ''

    def run(self):
        self.msg_received.emit('\nStarting receive thread...')
        while True:
            try:
                server_response = self.sock.recv(1024)
            except Exception as e:
                self.conn_lost.emit('\nReceive thread failed: %s' % str(e))
                return
            msg = str(server_response, "utf-8")
            if (msg == ''):
                self.conn_lost.emit('\nReceive thread connection lost!')
                return

            self.char_stream += msg

            while True:
                a = re.search(r'\b(END)\b', self.char_stream)
                if a is None:
                    break

                # getting the instructions
                instruction = self.char_stream[:a.start()]
                self.char_stream = self.char_stream[a.start() + 3:]

                # This list contains the instructions for the rocket.
                tokens = instruction.split()

                #string of try expect statement are just testing and sending if the command works.
                if tokens[0] == "STATEALL":
                    try:  # TODO get rid of velocity and encoder, add new tokens

                        mev_switch_open = tokens[1] == "1"
                        mev_switch_closed = tokens[2] == "1"
                        vent_switch_open = tokens[3] == "1"
                        vent_switch_closed = tokens[4] == "1"
                        n2o_switch_open = tokens[5] == "1"
                        n2o_switch_closed = tokens[6] == "1"
                        n2_switch_closed = tokens[7] == "1"
                        n2_switch_open = tokens[8] == "1"
                        rv_switch_closed = tokens[9] == "1"
                        rv_switch_open = tokens[10] == "1"
                        ignitor_on = tokens[11] == "1"

                        nc_valve_open = tokens[12] == '1'

                        lockout_armed = tokens[13] == '1'

                        self.limit_state_received.emit(mev_switch_open, mev_switch_closed, vent_switch_open,
                                                       vent_switch_closed, rv_switch_open, rv_switch_closed,
                                                       n2o_switch_open, n2o_switch_closed, n2_switch_open,
                                                       n2_switch_closed)
                        self.ignitor_state_received.emit(ignitor_on)
                        self.nc_valve_state_received.emit(nc_valve_open)
                        self.lockout_state_received.emit(lockout_armed)

                    # self.msg_received.emit('\nFrom server: %s' % msg)
                    except Exception as e:
                        self.msg_received.emit('\nInvalid state token: ' + str(e))
                elif tokens[0] == "LIMIT":
                    try:
                        switch_open = tokens[1] == "1"
                        switch_closed = tokens[2] == "1"
                        self.limit_state_received.emit(switch_open, switch_closed)
                    except Exception as e:
                        self.msg_received.emit('\nInvalid limit switch token: ' + str(e))
                elif tokens[0] == "IGNITOR":
                    try:
                        ignitor_on = tokens[1] == "1"
                        self.ignitor_state_received.emit(ignitor_on)
                    except Exception as e:
                        self.msg_received.emit('\nInvalid ignitor state token: ' + str(e))
                else:
                    self.msg_received.emit('\nFrom server: %s' % instruction)


# ------------------------------------------------#
#                                                 #
# Class holding all the display setting of the GUI#
#                                                 #
#  - This code is auto generated by a design      #
#    created in qt designer therefore most of     #
#    the code is not commented. Read Notes for    #
#    the pattern of setupUI.                      #
#                                                 #
# ------------------------------------------------#


def set_date():
    date = datetime.datetime.now()
    return date


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1108, 1109)
        MainWindow.setStyleSheet("background-color: rgb(245, 245, 245);")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.sys_controls = QtWidgets.QFrame(self.centralwidget)
        self.sys_controls.setStyleSheet("background-color: rgb(253, 253, 253);")
        self.sys_controls.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sys_controls.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sys_controls.setObjectName("sys_controls")
        self.gridLayout = QtWidgets.QGridLayout(self.sys_controls)
        self.gridLayout.setObjectName("gridLayout")
        self.N2OV_frame = QtWidgets.QFrame(self.sys_controls)

        self.N2OV_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.N2OV_frame.setObjectName("N2OV_frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.N2OV_frame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        # self.N2OV_label = QtWidgets.QLabel(self.N2OV_frame)
        self.N2OV_frame.setStyleSheet("border: none;")
        # self.N2OV_label.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
        #                               "border: none;")
        # self.N2OV_label.setObjectName("label_PV_2")
        # self.verticalLayout_5.addWidget(self.N2OV_label)
        self.N2OV_btn_on = QtWidgets.QPushButton(self.N2OV_frame)
        self.N2OV_btn_on.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                       "display:inline-block;\n"
                                       "padding:0.2em 0.2em;\n"
                                       "border:0.1em solid #3f3f3f;\n"

                                       "border-radius:0.2em;\n"
                                       "box-sizing: border-box;\n"
                                       "text-decoration:none;\n"
                                       "font-family:\'Roboto\',sans-serif;\n"
                                       "font-weight:300;\n"
                                       "color: #545454;\n"
                                       "text-align:center;\n"
                                       "transition: all 0.2s;")
        self.N2OV_btn_on.setObjectName("N2OV_btn_on")
        self.verticalLayout_5.addWidget(self.N2OV_btn_on)
        self.N2OV_btn_on.clicked.connect(self.send_n2ov_open)  # todo make send_n2ov_open
        self.N2OV_btn_off = QtWidgets.QPushButton(self.N2OV_frame)
        self.N2OV_btn_off.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                        "display:inline-block;\n"
                                        "padding:0.2em 0.2em;\n"
                                        "border:0.1em solid #3f3f3f;\n"

                                        "border-radius:0.2em;\n"
                                        "box-sizing: border-box;\n"
                                        "text-decoration:none;\n"
                                        "font-family:\'Roboto\',sans-serif;\n"
                                        "font-weight:300;\n"
                                        "color: #545454;\n"
                                        "text-align:center;\n"
                                        "transition: all 0.2s;")
        self.N2OV_btn_off.setObjectName("N2OV_btn_off")
        self.verticalLayout_5.addWidget(self.N2OV_btn_off)
        self.N2OV_btn_off.clicked.connect(self.send_n2ov_close)  # TODO make send_n2ov_close

        self.gridLayout.addWidget(self.N2OV_frame, 7, 2, 1, 1)
        self.IG_frame = QtWidgets.QFrame(self.sys_controls)
        self.IG_frame.setStyleSheet("border: none;")
        self.IG_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.IG_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.IG_frame.setObjectName("IG_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.IG_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.IG_label = QtWidgets.QLabel(self.IG_frame)
        self.IG_label.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
                                    "border: none;")
        self.IG_label.setObjectName("label_PV_3")
        self.verticalLayout_3.addWidget(self.IG_label)
        self.IG_btn_toggle = QtWidgets.QPushButton(self.IG_frame)
        # self.IG_btn_toggle.setEnabled(False)
        self.IG_btn_toggle.clicked.connect(self.send_toggle_ignitor)
        self.IG_btn_toggle.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                         "display:inline-block;\n"
                                         "padding:0.2em 0.2em;\n"
                                         "border:0.1em solid #3f3f3f;\n"

                                         "border-radius:0.2em;\n"
                                         "box-sizing: border-box;\n"
                                         "text-decoration:none;\n"
                                         "font-family:\'Roboto\',sans-serif;\n"
                                         "font-weight:300;\n"
                                         "color: #545454;\n"
                                         "text-align:center;\n"
                                         "transition: all 0.2s;")
        self.IG_btn_toggle.setObjectName("NCV_btn_toggle_2")
        self.verticalLayout_3.addWidget(self.IG_btn_toggle)
        self.IG_btn_toggle.clicked.connect(self.send_toggle_ignitor)

        self.gridLayout.addWidget(self.IG_frame, 4, 2, 1, 1)
        self.N2O_frame = QtWidgets.QFrame(self.sys_controls)
        self.N2O_frame.setStyleSheet("border: none;")
        self.N2O_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.N2O_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.N2O_frame.setObjectName("N2O_frame")
        self.horizontalLayout = QtWidgets.QVBoxLayout(self.N2O_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.label_N2O = QtWidgets.QLabel(self.N2O_frame)
        # self.label_N2O.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
        #                              "border: none;")
        # self.label_N2O.setObjectName("label_N2O")
        # self.verticalLayout_2.addWidget(self.label_N2O)
        self.N2O_btn_off = QtWidgets.QPushButton(self.N2O_frame)
        self.N2O_btn_off.setEnabled(True)
        self.N2O_btn_off.setAutoFillBackground(False)
        self.N2O_btn_off.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                       "display:inline-block;\n"
                                       "padding:0.2em 0.2em;\n"
                                       "border:0.1em solid #3f3f3f;\n"

                                       "border-radius:0.2em;\n"
                                       "box-sizing: border-box;\n"
                                       "text-decoration:none;\n"
                                       "font-family:\'Roboto\',sans-serif;\n"
                                       "font-weight:300;\n"
                                       "color: #545454;\n"
                                       "text-align:center;\n"
                                       "transition: all 0.2s;")
        self.N2O_btn_off.setCheckable(False)
        self.N2O_btn_off.setObjectName("N2O_btn_off")
        self.horizontalLayout.addWidget(self.N2O_btn_off)
        self.N2O_btn_off.clicked.connect(self.send_N2OF_close)

        self.N2O_btn_on = QtWidgets.QPushButton(self.N2O_frame)
        self.N2O_btn_on.clicked.connect(self.send_N2OF_open)
        self.N2O_btn_on.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                      "display:inline-block;\n"
                                      "padding:0.2em 0.2em;\n"
                                      "border:0.1em solid #3f3f3f;\n"

                                      "border-radius:0.2em;\n"
                                      "box-sizing: border-box;\n"
                                      "text-decoration:none;\n"
                                      "font-family:\'Roboto\',sans-serif;\n"
                                      "font-weight:300;\n"
                                      "color: #545454;\n"
                                      "text-align:center;\n"
                                      "transition: all 0.2s;")
        self.N2O_btn_on.setObjectName("N2O_btn_on")
        self.N2O_btn_on.clicked.connect(self.send_N2OF_open)
        self.horizontalLayout.addWidget(self.N2O_btn_on)
        self.gridLayout.addWidget(self.N2O_frame, 4, 0, 1, 1)
        self.RV_frame = QtWidgets.QFrame(self.sys_controls)
        self.RV_frame.setStyleSheet("border: none;")
        self.RV_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.RV_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.RV_frame.setObjectName("RV_frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.RV_frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        # self.label_RV = QtWidgets.QLabel(self.RV_frame)
        # self.label_RV.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
        #                             "border: none;")
        # self.label_RV.setObjectName("label_RV")
        # self.verticalLayout_6.addWidget(self.label_RV)
        self.RV_btn_on = QtWidgets.QPushButton(self.RV_frame)
        self.RV_btn_on.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                     "display:inline-block;\n"
                                     "padding:0.2em 0.2em;\n"
                                     "border:0.1em solid #3f3f3f;\n"

                                     "border-radius:0.2em;\n"
                                     "box-sizing: border-box;\n"
                                     "text-decoration:none;\n"
                                     "font-family:\'Roboto\',sans-serif;\n"
                                     "font-weight:300;\n"
                                     "color: #545454;\n"
                                     "text-align:center;\n"
                                     "transition: all 0.2s;")
        self.RV_btn_on.setObjectName("RV_btn_on")
        self.verticalLayout_6.addWidget(self.RV_btn_on)
        self.RV_btn_on.clicked.connect(self.send_RV_open)

        self.RV_btn_off = QtWidgets.QPushButton(self.RV_frame)
        self.RV_btn_off.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                      "display:inline-block;\n"
                                      "padding:0.2em 0.2em;\n"
                                      "border:0.1em solid #3f3f3f;\n"

                                      "border-radius:0.2em;\n"
                                      "box-sizing: border-box;\n"
                                      "text-decoration:none;\n"
                                      "font-family:\'Roboto\',sans-serif;\n"
                                      "font-weight:300;\n"
                                      "color: #545454;\n"
                                      "text-align:center;\n"
                                      "transition: all 0.2s;")
        self.RV_btn_off.setObjectName("PV_btn_off")
        self.verticalLayout_6.addWidget(self.RV_btn_off)
        self.RV_btn_off.clicked.connect(self.send_RV_close)

        self.gridLayout.addWidget(self.RV_frame, 6, 2, 1, 1)
        self.sys_info_frame_2 = QtWidgets.QFrame(self.sys_controls)
        self.sys_info_frame_2.setAutoFillBackground(False)
        self.sys_info_frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sys_info_frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sys_info_frame_2.setLineWidth(3)
        self.sys_info_frame_2.setMidLineWidth(3)
        self.sys_info_frame_2.setObjectName("sys_info_frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.sys_info_frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.launch_btn = QtWidgets.QPushButton(self.sys_info_frame_2)
        self.launch_btn.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";\n"
                                      "background-color: rgb(76, 187, 23);\n"
                                      "display:inline-block;\n"
                                      "padding:0.5em 0.5em;\n"
                                      "border:0.1em solid  rgb(76, 187, 23);\n"
                                      "border-radius:0.2em;\n"
                                      "box-sizing: border-box;\n"
                                      "text-decoration:none;\n"
                                      "font-family:\'Roboto\',sans-serif;\n"
                                      "font-weight:300;\n"
                                      "color: white;\n"
                                      "text-align:center;\n"
                                      "transition: all 0.2s;")
        self.launch_btn.setObjectName("launch_btn")

        self.horizontalLayout_2.addWidget(self.launch_btn)
        self.abort_btn = QtWidgets.QPushButton(self.sys_info_frame_2)
        self.abort_btn.clicked.connect(self.send_abort)
        self.abort_btn.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";\n"
                                     "display:inline-block;\n"
                                     "padding:0.5em 0.5em;\n"
                                     "background-color: rgb(255,0,0);\n"
                                     "border:0.1em solid  rgb(255,0,0);\n"
                                     "border-radius:0.2em;\n"
                                     "box-sizing: border-box;\n"
                                     "text-decoration:none;\n"
                                     "font-family:\'Roboto\',sans-serif;\n"
                                     "font-weight:300;\n"
                                     "color: white;\n"
                                     "text-align:center;\n"
                                     "transition: all 0.2s;\n"
                                     "")
        self.abort_btn.setObjectName("abort_btn")

        self.horizontalLayout_2.addWidget(self.abort_btn)
        self.gridLayout.addWidget(self.sys_info_frame_2, 8, 0, 1, 3)
        self.VV_frame = QtWidgets.QFrame(self.sys_controls)
        self.VV_frame.setStyleSheet("border: none;")
        self.VV_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.VV_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.VV_frame.setObjectName("VV_frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.VV_frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        # self.label_VV = QtWidgets.QLabel(self.VV_frame)
        # self.label_VV.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
        #                             "border: none;")
        # self.label_VV.setObjectName("label_VV")
        # self.verticalLayout_8.addWidget(self.label_VV)
        self.VV_btn_off = QtWidgets.QPushButton(self.VV_frame)
        self.VV_btn_off.clicked.connect(self.send_vent_close)
        self.VV_btn_off.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                      "display:inline-block;\n"
                                      "padding:0.35em 1.2em;\n"
                                      "border:0.1em solid #3f3f3f;\n"

                                      "border-radius:0.2em;\n"
                                      "box-sizing: border-box;\n"
                                      "text-decoration:none;\n"
                                      "font-family:\'Roboto\',sans-serif;\n"
                                      "font-weight:300;\n"
                                      "color: #545454;\n"
                                      "text-align:center;\n"
                                      "transition: all 0.2s;")
        self.VV_btn_off.setObjectName("VV_btn_off")
        self.verticalLayout_8.addWidget(self.VV_btn_off)

        self.VV_btn_on = QtWidgets.QPushButton(self.VV_frame)

        self.VV_btn_on.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                     "display:inline-block;\n"
                                     "padding:0.35em 1.2em;\n"
                                     "border:0.1em solid #3f3f3f;\n"

                                     "border-radius:0.2em;\n"
                                     "box-sizing: border-box;\n"
                                     "text-decoration:none;\n"
                                     "font-family:\'Roboto\',sans-serif;\n"
                                     "font-weight:300;\n"
                                     "color: #545454;\n"
                                     "text-align:center;\n"
                                     "transition: all 0.2s;")
        self.VV_btn_on.setObjectName("VV_btn_on")
        self.verticalLayout_8.addWidget(self.VV_btn_on)
        self.VV_btn_on.clicked.connect(self.send_vent_open)
        self.gridLayout.addWidget(self.VV_frame, 5, 2, 1, 1)
        self.sys_control_label = QtWidgets.QLabel(self.sys_controls)
        self.sys_control_label.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";")
        self.sys_control_label.setObjectName("valve_control_label")
        self.gridLayout.addWidget(self.sys_control_label, 2, 0, 1, 1)
        self.test_parms_frame = QtWidgets.QFrame(self.sys_controls)
        self.test_parms_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.test_parms_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.test_parms_frame.setObjectName("test_parms_frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.test_parms_frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.BD_frame_2 = QtWidgets.QFrame(self.test_parms_frame)
        self.BD_frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BD_frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BD_frame_2.setObjectName("BD_frame_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.BD_frame_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.MEV_open_label = QtWidgets.QLabel(self.BD_frame_2)
        self.MEV_open_label.setObjectName("BD_label_2")
        self.horizontalLayout_6.addWidget(self.MEV_open_label)
        self.MEV_lineEdit = QtWidgets.QLineEdit(self.BD_frame_2)
        self.MEV_lineEdit.setObjectName("BD_lineEdit_2")
        self.horizontalLayout_6.addWidget(self.MEV_lineEdit)
        self.gridLayout_2.addWidget(self.BD_frame_2, 2, 1, 1, 1)
        self.BD_frame = QtWidgets.QFrame(self.test_parms_frame)
        self.BD_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BD_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BD_frame.setObjectName("BD_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.BD_frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.BD_label = QtWidgets.QLabel(self.BD_frame)
        self.BD_label.setObjectName("BD_label")
        self.horizontalLayout_3.addWidget(self.BD_label)
        self.BD_lineEdit = QtWidgets.QLineEdit(self.BD_frame)
        self.BD_lineEdit.setObjectName("BD_lineEdit")
        self.horizontalLayout_3.addWidget(self.BD_lineEdit)
        self.gridLayout_2.addWidget(self.BD_frame, 0, 1, 1, 1)
        self.ID_frame = QtWidgets.QFrame(self.test_parms_frame)
        self.ID_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ID_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ID_frame.setObjectName("ID_frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.ID_frame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ID_label = QtWidgets.QLabel(self.ID_frame)
        self.ID_label.setObjectName("ID_label")
        self.horizontalLayout_4.addWidget(self.ID_label)
        self.ID_lineEdit = QtWidgets.QLineEdit(self.ID_frame)
        self.ID_lineEdit.setObjectName("lineEdit_3")
        self.horizontalLayout_4.addWidget(self.ID_lineEdit)
        self.gridLayout_2.addWidget(self.ID_frame, 0, 2, 1, 1)
        self.BD_frame_3 = QtWidgets.QFrame(self.test_parms_frame)
        self.BD_frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BD_frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BD_frame_3.setObjectName("BD_frame_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.BD_frame_3)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.sys_open_label = QtWidgets.QLabel(self.BD_frame_3)
        self.sys_open_label.setObjectName("BD_label_3")
        self.horizontalLayout_7.addWidget(self.sys_open_label)
        self.SYS_open_lineEdit = QtWidgets.QLineEdit(self.BD_frame_3)
        self.SYS_open_lineEdit.setObjectName("BD_lineEdit_3")
        self.horizontalLayout_7.addWidget(self.SYS_open_lineEdit)
        self.gridLayout_2.addWidget(self.BD_frame_3, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.test_parms_frame, 1, 0, 1, 3)
        self.N2_frame = QtWidgets.QFrame(self.sys_controls)
        self.N2_frame.setStyleSheet("border: none;")
        self.N2_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.N2_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.N2_frame.setObjectName("N2_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.N2_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        # self.N2_label = QtWidgets.QLabel(self.N2_frame)
        # self.N2_label.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
        #                             "border: none;")
        # self.N2_label.setObjectName("label_N2")
        # self.verticalLayout.addWidget(self.N2_label)
        self.N2_btn_off = QtWidgets.QPushButton(self.N2_frame)
        self.N2_btn_off.clicked.connect(self.send_N2F_close)

        self.N2_btn_off.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                      "display:inline-block;\n"
                                      "padding:0.35em 1.2em;\n"
                                      "border:0.1em solid #3f3f3f;\n"

                                      "border-radius:0.2em;\n"
                                      "box-sizing: border-box;\n"
                                      "text-decoration:none;\n"
                                      "font-family:\'Roboto\',sans-serif;\n"
                                      "font-weight:300;\n"
                                      "color: #545454;\n"
                                      "text-align:center;\n"
                                      "transition: all 0.2s;")
        self.N2_btn_off.setObjectName("N2_btn_off")
        self.verticalLayout.addWidget(self.N2_btn_off)
        self.N2_btn_on = QtWidgets.QPushButton(self.N2_frame)
        self.N2_btn_on.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                     "display:inline-block;\n"
                                     "padding:0.35em 1.2em;\n"
                                     "border:0.1em solid #3f3f3f;\n"

                                     "border-radius:0.2em;\n"
                                     "box-sizing: border-box;\n"
                                     "text-decoration:none;\n"
                                     "font-family:\'Roboto\',sans-serif;\n"
                                     "font-weight:300;\n"
                                     "color: #545454;\n"
                                     "text-align:center;\n"
                                     "transition: all 0.2s;")
        self.N2_btn_on.setObjectName("N2_btn_on")
        self.verticalLayout.addWidget(self.N2_btn_on)
        self.N2_btn_on.clicked.connect(self.send_N2F_open)
        self.gridLayout.addWidget(self.N2_frame, 5, 0, 1, 1)
        self.MEV_frame = QtWidgets.QFrame(self.sys_controls)
        self.MEV_frame.setStyleSheet("border: none;")
        self.MEV_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MEV_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.MEV_frame.setObjectName("MEV_frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.MEV_frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        # self.label_MEV = QtWidgets.QLabel(self.MEV_frame)
        # self.label_MEV.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
        #                              "border: none;")
        # self.label_MEV.setObjectName("label_MEV")
        # self.verticalLayout_4.addWidget(self.label_MEV)
        self.MEV_btn_on = QtWidgets.QPushButton(self.MEV_frame)
        self.MEV_btn_on.clicked.connect(self.send_mev_open)
        self.MEV_btn_on.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                      "display:inline-block;\n"
                                      "padding:0.35em 1.2em;\n"
                                      "border:0.1em solid #3f3f3f;\n"

                                      "border-radius:0.2em;\n"
                                      "box-sizing: border-box;\n"
                                      "text-decoration:none;\n"
                                      "font-family:\'Roboto\',sans-serif;\n"
                                      "font-weight:300;\n"
                                      "color: #545454;\n"
                                      "text-align:center;\n"
                                      "transition: all 0.2s;")
        self.MEV_btn_on.setObjectName("MEV_btn_on")
        self.verticalLayout_4.addWidget(self.MEV_btn_on)
        self.MEV_btn_off = QtWidgets.QPushButton(self.MEV_frame)
        self.MEV_btn_off.clicked.connect(self.send_mev_close)
        self.MEV_btn_off.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                       "display:inline-block;\n"
                                       "padding:0.35em 1.2em;\n"
                                       "border:0.1em solid #3f3f3f;\n"

                                       "border-radius:0.2em;\n"
                                       "box-sizing: border-box;\n"
                                       "text-decoration:none;\n"
                                       "font-family:\'Roboto\',sans-serif;\n"
                                       "font-weight:300;\n"
                                       "color: #545454;\n"
                                       "text-align:center;\n"
                                       "transition: all 0.2s;")
        self.MEV_btn_off.setObjectName("MEV_btn_off")
        self.verticalLayout_4.addWidget(self.MEV_btn_off)
        self.gridLayout.addWidget(self.MEV_frame, 7, 0, 1, 1)
        self.NCV_frame = QtWidgets.QFrame(self.sys_controls)
        self.NCV_frame.setStyleSheet("border: none;\n"
                                     "")
        self.NCV_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.NCV_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.NCV_frame.setLineWidth(0)
        self.NCV_frame.setObjectName("NCV_frame")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.NCV_frame)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.NCV_label = QtWidgets.QLabel(self.NCV_frame)
        self.NCV_label.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
                                     "border: none;")
        self.NCV_label.setObjectName("label")
        self.verticalLayout_7.addWidget(self.NCV_label)
        self.NCV_btn_toggle = QtWidgets.QPushButton(self.NCV_frame)
        self.NCV_btn_toggle.clicked.connect(self.send_toggle_nc_valve)
        self.NCV_btn_toggle.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                          "display:inline-block;\n"
                                          "padding:0.35em 1.2em;\n"
                                          "border:0.1em solid #3f3f3f;\n"

                                          "border-radius:0.2em;\n"
                                          "box-sizing: border-box;\n"
                                          "text-decoration:none;\n"
                                          "font-family:\'Roboto\',sans-serif;\n"
                                          "font-weight:300;\n"
                                          "color: #545454;\n"
                                          "text-align:center;\n"
                                          "transition: all 0.2s;")
        self.NCV_btn_toggle.setObjectName("NCV_btn_toggle")
        self.verticalLayout_7.addWidget(self.NCV_btn_toggle)
        self.gridLayout.addWidget(self.NCV_frame, 6, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.sys_controls)
        self.line.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                "background-color: rgb(73, 73, 73);")
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 1, 4, 1)
        self.test_parms_label = QtWidgets.QLabel(self.sys_controls)
        self.test_parms_label.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";")
        self.test_parms_label.setObjectName("test_parms_label")
        self.gridLayout.addWidget(self.test_parms_label, 0, 0, 1, 1)
        self.horizontalLayout_5.addWidget(self.sys_controls)
        self.column2_frame = QtWidgets.QFrame(self.centralwidget)
        self.column2_frame.setStyleSheet("min-width: 300px;\n"
                                         "max-width: 500px;\n"
                                         "background-color: rgb(253, 253, 253);")
        self.column2_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.column2_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.column2_frame.setObjectName("column2_frame")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.column2_frame)
        self.verticalLayout_11.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_11.setContentsMargins(9, 0, -1, 0)
        self.verticalLayout_11.setSpacing(14)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.print_sys_frame = QtWidgets.QFrame(self.column2_frame)
        self.print_sys_frame.setFocusPolicy(QtCore.Qt.NoFocus)
        self.print_sys_frame.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.print_sys_frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.print_sys_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.print_sys_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.print_sys_frame.setObjectName("print_sys_frame")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.print_sys_frame)
        self.verticalLayout_9.setContentsMargins(-1, 9, -1, -1)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_sys_info = QtWidgets.QLabel(self.print_sys_frame)
        self.label_sys_info.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";")
        self.label_sys_info.setObjectName("label_sys_info")
        self.verticalLayout_9.addWidget(self.label_sys_info)
        #
        self.sys_info_frame = QtWidgets.QFrame(self.print_sys_frame)
        self.sys_info_frame.setAutoFillBackground(False)
        self.sys_info_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sys_info_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sys_info_frame.setObjectName("sys_info_frame")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.sys_info_frame)
        self.verticalLayout_10.setContentsMargins(-1, 9, -1, 9)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_3 = QtWidgets.QLabel(self.sys_info_frame)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_10.addWidget(self.label_3)
        #IP adress edit line
        self.lineEdit_IPadress = QtWidgets.QLineEdit(self.sys_info_frame)
        self.lineEdit_IPadress.setObjectName(
            "lineEdit_IPadress")  # TODO might have to change self.lineEdit_IPadress to connect to server
        self.lineEdit_IPadress.setPlaceholderText("IP address")
        self.lineEdit_IPadress.setText("10.42.0.171")
        self.verticalLayout_10.addWidget(self.lineEdit_IPadress)
        #disconnect button
        self.disconnect_btn = QtWidgets.QPushButton(self.sys_info_frame)
        self.disconnect_btn.clicked.connect(self.set_disconnect)
        self.disconnect_btn.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                          "display:inline-block;\n"
                                          "border:0.1em solid black;\n"
                                          "margin:0 0.3em 0.3em 0;\n"
                                          "border-radius:0.2em;\n"
                                          "box-sizing: border-box;\n"
                                          "text-decoration:none;\n"
                                          "font-family:\'Roboto\',sans-serif;\n"
                                          "font-weight:300;\n"
                                          "color: black;\n"
                                          "text-align:center;\n"
                                          "transition: all 0.2s;")
        self.disconnect_btn.setObjectName("disconnect_btn")
        self.verticalLayout_10.addWidget(self.disconnect_btn)
        self.connect_btn = QtWidgets.QPushButton(self.sys_info_frame)
        self.connect_btn.clicked.connect(self.set_connection)
        self.connect_btn.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                       "display:inline-block;\n"
                                       "border:0.1em solid black;\n"
                                       "margin:0 0.3em 0.3em 0;\n"
                                       "border-radius:0.2em;\n"
                                       "box-sizing: border-box;\n"
                                       "text-decoration:none;\n"
                                       "font-family:\'Roboto\',sans-serif;\n"
                                       "font-weight:300;\n"
                                       "color: black;\n"
                                       "text-align:center;\n"
                                       "transition: all 0.2s;")
        self.connect_btn.setObjectName("connect_btn")
        self.verticalLayout_10.addWidget(self.connect_btn)
        self.label_date = QtWidgets.QLabel(self.sys_info_frame)
        self.label_date.setObjectName("label_date")
        self.verticalLayout_10.addWidget(self.label_date)
        self.lineEdit_date = QtWidgets.QLineEdit(self.sys_info_frame)
        # while True:
        date = datetime.datetime.now()
        self.lineEdit_date.setText(str(date.strftime("%a, %b %d, %Y %I:%M:%S %p")))

        self.lineEdit_date.setObjectName("lineEdit_date")
        self.verticalLayout_10.addWidget(self.lineEdit_date)
        self.label_update = QtWidgets.QLabel(self.sys_info_frame)
        self.label_update.setObjectName("label_update")
        self.verticalLayout_10.addWidget(self.label_update)
        self.lineEdit_update = QtWidgets.QLineEdit(self.sys_info_frame)
        self.lineEdit_update.setText("")
        self.lineEdit_update.setObjectName("lineEdit_update")
        self.verticalLayout_10.addWidget(self.lineEdit_update)
        self.verticalLayout_9.addWidget(self.sys_info_frame)
        self.label_sys_status = QtWidgets.QLabel(self.print_sys_frame)
        self.label_sys_status.setStyleSheet("font: 75 18pt \"MS Shell Dlg 2\";")
        self.label_sys_status.setObjectName("label_sys_status")
        self.verticalLayout_9.addWidget(self.label_sys_status)
        self.print_sys_status_text = QtWidgets.QTextBrowser(self.print_sys_frame)
        self.print_sys_status_text.setObjectName("print_sys_status_text")
        self.verticalLayout_9.addWidget(self.print_sys_status_text)
        self.label_2 = QtWidgets.QLabel(self.print_sys_frame)
        self.label_2.setStyleSheet("float:right;")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../../../Users/lemie/Downloads/ENGR 120/uvic_rocketry_logo.png"))
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("width: 100px;\n z-index: 0;")
        self.verticalLayout_9.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.sys_info_frame.raise_()
        self.print_sys_status_text.raise_()
        self.label_sys_status.raise_()
        self.label_2.raise_()
        self.label_sys_info.raise_()
        self.verticalLayout_11.addWidget(self.print_sys_frame)
        self.horizontalLayout_5.addWidget(self.column2_frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1108, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):  # todo chage names of variables
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hybrid GUI"))
        # self.N2OV_label.setText(_translate("MainWindow", "N2O VENT VALVE"))
        self.N2OV_btn_on.setText(_translate("MainWindow", "N2OV (ON)"))
        self.N2OV_btn_off.setText(_translate("MainWindow", "N2OV (OFF)"))
        self.IG_label.setText(_translate("MainWindow", "IGNITOR"))
        self.IG_btn_toggle.setText(_translate("MainWindow", "IGNITOR (TOGGLE)"))
        # self.label_N2O.setText(_translate("MainWindow", "N2O FLOW"))
        self.N2O_btn_off.setText(_translate("MainWindow", "N2OF (OFF)"))
        self.N2O_btn_on.setText(_translate("MainWindow", "N2OF (ON)"))
        # self.label_RV.setText(_translate("MainWindow", "RELIEF VALVE "))
        self.RV_btn_on.setText(_translate("MainWindow", "RV (ON)"))
        self.RV_btn_off.setText(_translate("MainWindow", "RV (OFF)"))
        self.launch_btn.setText(_translate("MainWindow", "RUN"))
        self.abort_btn.setText(_translate("MainWindow", "ABORT"))
        # self.label_VV.setText(_translate("MainWindow", "VENT VALVE"))
        self.VV_btn_off.setText(_translate("MainWindow", "VV (OFF)"))
        self.VV_btn_on.setText(_translate("MainWindow", "VV (ON)"))
        self.sys_control_label.setText(_translate("MainWindow", " System Controls "))
        self.MEV_open_label.setText(_translate("MainWindow", "MEV OPEN (%)"))
        self.BD_label.setText(_translate("MainWindow", "BURN DURATION (s)"))
        self.ID_label.setText(_translate("MainWindow", "IGNITOR DELAY (s)"))
        self.sys_open_label.setText(_translate("MainWindow", "SYSTEM OPEN (%)"))
        # self.N2_label.setText(_translate("MainWindow", "N2 FLOW"))
        self.N2_btn_off.setText(_translate("MainWindow", " N2F (OFF)"))
        self.N2_btn_on.setText(_translate("MainWindow", "N2F (ON)"))
        # self.label_MEV.setText(_translate("MainWindow", "MAIN ENGINE VALVE"))
        self.MEV_btn_on.setText(_translate("MainWindow", "MEV (ON)"))
        self.MEV_btn_off.setText(_translate("MainWindow", "MEV (OFF)"))
        self.NCV_label.setText(_translate("MainWindow", "NORMALLY CLOSED VALVE"))
        self.NCV_btn_toggle.setText(_translate("MainWindow", "NCV (TOGGLE)"))
        self.test_parms_label.setText(_translate("MainWindow", "Test Parameters"))
        self.label_sys_info.setText(_translate("MainWindow", "System Information"))
        self.label_3.setText(_translate("MainWindow", "IP Adress"))
        self.disconnect_btn.setText(_translate("MainWindow", "Disconnect"))
        self.connect_btn.setText(_translate("MainWindow", "Connect"))
        self.label_date.setText(_translate("MainWindow", "Time/Date"))
        self.label_update.setText(_translate("MainWindow", "Last Update"))
        self.label_sys_status.setText(_translate("MainWindow", "System Status"))

    def disable_element(self, obj):
        obj.setEnabled(False)
        obj.setText(0)

    # Change variable names to match above
    # todo Add new stepper and limit switches

    # In this part of the code we need to connect using sockets
    def set_connection(self):  # todo functions are never used? How do we get them to be used
        # Answer? change them to calls and declare them outside of the class?
        # Answer? Completely restructure this method?
        if self.sock is None:
            self.sock = socket.socket()
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # establishing the socket connection
        try:
            self.sock.connect((self.lineEdit_IPadress.text(), 9999))
            self.print_sys_status_text.appendPlainText("\nCONNECTION IS ESTABLISHED!")

            if self.receiver is None:
                self.receiver = ReceiveThread(self.sock)
                self.receiver.msg_received.connect(self.on_msg_received)
                self.receiver.limit_state_received.connect(self.on_limit_state_received)
                self.receiver.ignitor_state_received.connect(self.on_ignitor_state_received)
                self.receiver.conn_lost.connect(self.on_conn_lost)
                self.receiver.nc_valve_state_received.connect(self.on_nc_valve_state_received)
                self.receiver.lockout_state_received.connect(self.on_lockout_state_received)
                self.receiver.start()

            self.connect_btn.setEnabled(False)
            if _AUTO_TEST_ENABLED:
                self.launch_btn.setEnabled(True)
            self.abort_btn.setEnabled(True)
            self.IG_btn_toggle.setEnabled(True)
            self.MEV_btn_on.setEnabled(True)
            self.MEV_btn_off.setEnabled(True)
            self.NCV_btn_toggle.setEnabled(True)
            self.VV_btn_on.setEnabled(True)
            self.VV_btn_off.setEnabled(True)
            # self.set_default_vel_button.setEnabled(False)
            self.N2O_btn_off.setEnabled(True)
            self.N2O_btn_on.setEnabled(True)
            self.N2_btn_off.setEnabled(True)
            self.N2_btn_on.setEnabled(True)
            self.N2OV_btn_on.setEnabled(True)
            self.N2OV_btn_off.setEnabled(True)

            self.lineEdit_IPadress.setEnabled(False)

            self.elapsed_timer = QElapsedTimer()
            self.elapsed_timer.start()

            self.status_timer.timeout.connect(self.on_status_timer)
            self.status_timer.start(1)

            self.mev_open_timer.start()

        except Exception as e:
            self.print_sys_status_text.appendPlainText("Connection failure:" + str(e))

        def on_status_timer(self):
            elapsed_time = self.elapsed_timer.elapsed()
            self.status_delay.setText(str(elapsed_time).zfill(3))
            if elapsed_time > 100:
                self.status_delay.setStyleSheet("background-color: red")
            else:
                self.status_delay.setStyleSheet("background-color: white")
            if self.mev_fully_open:
                self.mev_open_time.setText(str(self.mev_open_timer.elapsed()).zfill(3))

        # submit data to the  server
        def send_auparams(self):
            # Collecting alto_test_l of the variables from the textboxes
            mev_open_timing = self.MEV_lineEdit.text()
            burn_duration = self.BD_lineEdit.text()
            ignitor_timing = self.ID_lineEdit.text()
            sys_open_timing = self.SYS_open_lineEdit.text()
            valve_open_timing = self.valve_open_timing_box.text()
            valve_closing_time = self.valve_closing_time_box.text()
            # todo add SYSTEM OPEN % to all of the code

            auto_test_params = "AUTO_TEST_PARAMS " + launch_code + " " + burn_duration + " " + ignitor_timing + " " + valve_open_timing + " " + valve_closing_time
            if len(auto_test_params.split()) != 6:  # todo change params?
                self.on_msg_received("Auto test error: need 5 parameters\n")
                return

            try:
                self.send_to_server(auto_test_params)
            except Exception as e:
                self.print_sys_status_text.appendPlainText("Problem: " + str(e))
                return self.launch_btn.setEnabled(False)

    def set_disconnect(self):
        self.on_conn_lost("Disconnected")

    # abort
    def send_abort(self):
        self.send_to_server("ABORT")

    def send_toggle_nc_valve(self):
        self.send_to_server("NC_VALVE")

    # open valve
    def send_mev_open(self):
        self.send_to_server("MEV_OPEN")

    # valve closing
    def send_mev_close(self):
        self.send_to_server("MEV_CLOSE")

    def send_vent_open(self):
        self.send_to_server("VENT_OPEN")

    def send_vent_close(self):
        self.send_to_server("VENT_CLOSE")

    def send_N2OF_close(self):
        self.send_to_server("N20_CLOSE")

    def send_N2OF_open(self):
        self.send_to_server("N20_OPEN")

    def send_RV_open(self):
        self.send_to_server("RV_OPEN")

    def send_RV_close(self):
        self.send_to_server("RV_CLOSE")

    def send_N2F_open(self):
        self.send_to_server("N2_OPEN")

    def send_N2F_close(self):
        self.send_to_server("N2_CLOSE")

    def send_n2ov_open(self):
        self.send_to_server("N2OV_OPEN")

    def send_n2ov_close(self):
        self.send_to_server("N2OV_CLOSED")

    # ignition
    def send_toggle_ignitor(self):
        self.send_to_server("IGNITOR")

    def on_msg_received(self, msg):
        self.print_sys_status_text.appendPlainText(msg)

    def on_limit_state_received(self, mev_switch_open, mev_switch_closed, vent_switch_open, vent_switch_closed,
                                rv_switch_open, rv_switch_closed, n2o_switch_open, n2o_switch_closed, n2_switch_open,
                                n2_switch_closed):
        self.elapsed_timer.restart()
        if mev_switch_open:  # TODO check if frame change when limit switch is activated
            # self.mev_open_limit_indicator.setText("F. OPEN")
            self.MEV_frame.setStyleSheet("border: 2.5px solid #005493;\n")
            self.print_sys_status_text.appendPlainText("MEV Open state received")

            if not self.mev_fully_open:
                self.mev_open_timer.restart()
            self.mev_fully_open = True
        else:
            self.MEV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("MEV open NOT state received")
        if mev_switch_closed:
            self.MEV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("MEV close state received")
            self.mev_fully_open = False
        else:
            self.MEV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("MEV close state NOT received")

        if vent_switch_open:
            self.VV_frame.setStyleSheet("border:2.5px solid #005493;\n")
            self.print_sys_status_text.appendPlainText("Vent Valve Open state received")
        else:
            self.VV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("Vent Valve Open state NOT received")
        if vent_switch_closed:
            self.VV_frame.setStyleSheet("border: 2.5px solid green;")
            self.print_sys_status_text.appendPlainText("Vent Valve close state received")
        else:
            self.VV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("Vent Valve close state NOT received")

        if rv_switch_open:
            self.RV_frame.setStyleSheet("border:2.5px solid #005493;\n")
            self.print_sys_status_text.appendPlainText("Relief Valve open state received")
        else:
            self.RV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("Relief Valve open state NOT received")

        if rv_switch_closed:
            self.RV_frame.setStyleSheet("border:2.5px solid green;\n")
            self.print_sys_status_text.appendPlainText("Relief Valve close state received")

        else:
            self.RV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("Relief Valve close state NOT received")

        if n2o_switch_open:
            self.RV_frame.setStyleSheet("border:2.5px solid #005493;\n")
            self.print_sys_status_text.appendPlainText("N2O Valve open state received")

        else:
            self.RV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("N2O Valve open state NOT received")

        if n2o_switch_closed:
            self.RV_frame.setStyleSheet("border:2.5px solid #005493;\n")
            self.print_sys_status_text.appendPlainText("N2O Valve close state received")

        else:
            self.RV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("N2O Valve close state NOT received")

        if n2_switch_open:
            self.RV_frame.setStyleSheet("border:2.5px solid #005493;\n")
            self.print_sys_status_text.appendPlainText("N2 Valve open state received")

        else:
            self.RV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("N2 Valve open state NOT received")

        if n2_switch_closed:
            self.RV_frame.setStyleSheet("border:2.5px solid green;\n")
            self.print_sys_status_text.appendPlainText("N2 Valve close state received")

        else:
            self.RV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("N2 Valve close state NOT received")

    def on_ignitor_state_received(self, active):
        if active:
            self.IG_frame.setStyleSheet("border: 2.5px solid red;")
            self.print_sys_status_text.appendPlainText("Ignitor state received")
        else:
            self.IG_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("Ignitor NOT state received")

    def on_nc_valve_state_received(self, active):
        if active:
            self.NCV_frame.setStyleSheet("border: solid 2.5px red;")
            self.print_sys_status_text.appendPlainText("Normally closed Valve state received")

        else:
            self.NCV_frame.setStyleSheet("border: none;")
            self.print_sys_status_text.appendPlainText("Normally closed Valve state NOT received")

    def on_lockout_state_received(self, active):
        if active:
            self.print_sys_status_text.setText("Lock out: ARMED")
            self.lockout_button_indicator.setStyleSheet("background-color: red")
        else:
            self.print_sys_status_text.setText("Lock out: DISARMED")
            self.lockout_button_indicator.setStyleSheet("background-color: green")

    def set_all_indicator_buttons(self, msg, color):
        self.print_sys_status_text.setText("MEV closed limit" + msg)
        self.mev_close_limit_indicator.setStyleSheet(color)

        self.print_sys_status_text.setText("MEV open limit" + msg)
        self.mev_open_limit_indicator.setStyleSheet(color)

        self.print_sys_status_text.setText("Vent Valve closed limit" + msg)
        self.vent_close_limit_indicator.setStyleSheet(color)

        self.print_sys_status_text.setText("Vent Valve closed limit" + msg)
        self.vent_open_limit_indicator.setStyleSheet(color)

        self.print_sys_status_text.setText("Ignitor limit" + msg)
        self.ignitor_button_indicator.setStyleSheet(color)

        self.print_sys_status_text.setText("Normally Closed Valve limit" + msg)
        self.nc_valve_button_indicator.setStyleSheet(color)

        self.print_sys_status_text.setText("Lockout limit" + msg)
        self.lockout_button_indicator.setStyleSheet(color)

    def send_to_server(self, msg):
        msg += ' END\n'
        if self.sock is not None:
            try:
                self.sock.sendall(msg.encode())
            except Exception as e:
                print("Send to server failed: " + str(e))

    def display_about(self):
        QMessageBox.about(self, "About", "Hybrid Test Stand Control\n\nWritten for UVic Rocketry\n\n" \
                                         "Contributors:\n\nAndres Martinez\nAnar Kazimov\nAlexander "
                                         "Schell\nKristopher Lemieux\n\nLGPL Version 4")

    def on_conn_lost(self, msg=""):
        self.print_sys_status_text.appendPlainText(msg)
        self.set_all_indicator_buttons("Unknown", "background-color: gray")

        self.lineEdit_IPadress.setEnabled(True)

        if self.sock is not None:
            self.sock.close()
            self.sock = None

        self.connect_btn.setEnabled(True)
        self.abort_btn.setEnabled(False)
        self.IG_btn_toggle.setEnabled(False)
        self.MEV_btn_on.setEnabled(False)
        self.MEV_btn_off.setEnabled(False)
        self.launch_btn.setEnabled(False)
        self.NCV_btn_toggle.setEnabled(False)
        self.VV_btn_on.setEnabled(False)
        self.VV_btn_off.setEnabled(False)
        # self.set_default_vel_button.setEnabled(False)
        self.N2O_btn_off.setEnabled(False)
        self.N2O_btn_on.setEnabled(False)
        self.N2_btn_off.setEnabled(False)
        self.N2_btn_on.setEnabled(False)
        self.N2OV_btn_on.setEnabled(False)
        self.N2OV_btn_off.setEnabled(False)

        self.receiver = None


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
