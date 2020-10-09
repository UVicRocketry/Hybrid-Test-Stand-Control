from PyQt5 import QtWidgets, uic, QtCore
import sys

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        # Load the UI Page. uic is the thing that lets us use a .ui file
        # This only works if the .ui file is in the same directory
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('hybrid_test_gui.ui', self)

        # This will connect all the buttons to methods that are called when the
        # buttons are clicked by the user.
        self.setup_buttons_etc()
        
        ## STATES ##  
        # These will get updated by the GUI if the user clicks a button or
        # if the server changes something.
        self.state_connected = False
        self.state_igniter = False
        self.state_MEV = False
        self.state_N2OV = False
        self.state_N2O = False
        self.state_N2 = False
        self.state_NCV = False
        self.state_RV = False
        self.state_VV = False
        self.state_abort = False
        self.state_run = False


    def setup_buttons_etc(self):
        # Alright so basically since there is not a "loop" to put methods in that
        # you want to update based on things that have changed in the GUI,
        # PyQt has these things called signals and slots. They let you connect
        # changes or "signals" of objects in the GUI to methods.

        # For instance we can connect_btn is a QPushButton from QT Designer, 
        # which has a signal "clicked". We can "connect" this to a method that
        # we want to run when the button is clicked. 
        self.connect_btn.clicked.connect(self._connect_btn)

        # We do this for every button in the GUI. Each button gets a corresponding
        # method that has the same name as the button but with an _ in front
        
        # To add a new button:
            # Add the button to the GUI in QT Designer
            # Give it a nice name
            # Add a new line to this method in the form "self.button_name.clicked.connect(self._button_name)"
            # Add a new method in below setup_button_etc of the form "def _button_name(self):"
            # Any code in that method will be run when the button is clicked!
        self.disconnect_btn.clicked.connect(self._disconnect_btn)
        self.igniter_btn_toggle.clicked.connect(self._igniter_btn_toggle)
        self.MEV_btn_off.clicked.connect(self._MEV_btn_off)
        self.MEV_btn_on.clicked.connect(self._MEV_btn_on)
        self.N2OV_btn_off.clicked.connect(self._N2OV_btn_off)
        self.N2OV_btn_on.clicked.connect(self._N2OV_btn_on)
        self.N2O_btn_off.clicked.connect(self._N2O_btn_off)
        self.N2O_btn_on.clicked.connect(self._N2O_btn_on)
        self.N2_btn_off.clicked.connect(self._N2_btn_off)
        self.N2_btn_on.clicked.connect(self._N2_btn_on)
        self.NCV_btn_off.clicked.connect(self._NCV_btn_off)
        self.NCV_btn_on.clicked.connect(self._NCV_btn_on)
        self.RV_btn_off.clicked.connect(self._RV_btn_off)
        self.RV_btn_on.clicked.connect(self._RV_btn_on)
        self.VV_btn_off.clicked.connect(self._VV_btn_off)
        self.VV_btn_on.clicked.connect(self._VV_btn_on)
        self.abort_btn.clicked.connect(self._abort_btn)
        self.run_btn.clicked.connect(self._run_btn)

    def _connect_btn(self):
        self.state_connected = True        
        print(self.state_connected)
    
    def _disconnect_btn(self):
        self.state_connected = False
        print(self.state_connected)

    def _igniter_btn_toggle(self):
        print(self.state_igniter)

    def _MEV_btn_off(self):
        print(self.state_MEV)    

    def _MEV_btn_on(self):
        print(self.state_MEV)

    def _N2OV_btn_off(self):
        print(self.state_N2OV)
        
    def _N2OV_btn_on(self):
        print(self.state_N2OV)

    def _N2O_btn_off(self):
        print(self.state_N2O)

    def _N2O_btn_on(self):
        print(self.state_N2O)

    def _N2_btn_off(self):
        print(self.state_N2)

    def _N2_btn_on(self):
        print(self.state_N2)

    def _NCV_btn_off(self):
        print(self.state_NCV)

    def _NCV_btn_on(self):
        print(self.state_NCV)

    def _RV_btn_off(self):
        print(self.state_RV)

    def _RV_btn_on(self):
        print(self.state_RV)

    def _VV_btn_off(self):
        print(self.state_VV)

    def _VV_btn_on(self):
        print(self.state_VV)

    def _abort_btn(self):
        print(self.state_abort)

    def _run_btn(self):
        print(self.state_run)




    def send_to_server(self):
        print("")
    

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':      
    main()
