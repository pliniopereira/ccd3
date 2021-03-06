from time import sleep

import comtypes.client as cc
import comtypes.gen.INTEGMOTORINTERFACELib
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

# from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.utils.Singleton import Singleton
from src.utils.rodafiltros import Leitura_portas


class FilterControl(metaclass=Singleton):
    def __init__(self):
        # self.console = ConsoleThreadOutput()
        self.smi = None
        self.CommInterface = None
        self.motor_door = None
        self.connect_state = None
        self.shutter_open = None
        if self.connect_state:
            self.CommInterface.AddressMotorChain()

    def connect(self):
        self.smi = cc.CreateObject('SMIEngine.SMIHost')
        cc.GetModule('IntegMotorInterface.dll')
        self.CommInterface = self.smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
        self.motor_door = None
        self.establish_link()

    def establish_link(self):
        sleep(1)
        self.CommInterface.BaudRate = 9600
        serial_list = Leitura_portas.serial_ports()
        count_aux = int(len(serial_list))
        for count in range(0, count_aux):
            print("Search for " + serial_list[count] + " link to Motors!")
            try:
                self.CommInterface.OpenPort(serial_list[count])
                self.CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain
                self.CommInterface.WriteCommand("UBO")  # Make sure USER Bit B is output bit (UBO)
                self.CommInterface.WriteCommand("d=-1 GOSUB1")
                answer = self.CommInterface.ReadResponse()
                if answer == 'SHTR:???':
                    print(serial_list[count] + " - Established a link to Motors!\n")
                    # self.console.raise_text(str(serial_list[count]) + " - Established a link to Motors!\n", 1)

                    self.smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
                    self.connect_state = True
                    self.motor_door = serial_list[count]

                    print("Shutter has been closed.")
                    # self.console.raise_text("Shutter has been closed.", 1)
                    self.close_shutter()

                    self.home_reset()

                    break
            except Exception as e:
                print(serial_list[count] + " - Cannot establish a link to Motors -> {}".format(e))

    def open_shutter(self):
        try:
            if not self.shutter_open:
                # self.console.raise_text("Shutter has been opened.", 1)
                self.CommInterface.WriteCommand("UB=1")  # Make sure shutter is in the closed state
                sleep(1)
                self.shutter_open = True
        except Exception as e:
            print("Open Shutter ERROR -> {}".format(e))

    def close_shutter(self):
        try:
            # self.console.raise_text("Shutter has been closed.", 1)
            if self.shutter_open:
                self.CommInterface.WriteCommand("UB=0")
                sleep(1)
                self.shutter_open = False
        except Exception as e:
            print("Close Shutter ERROR -> {}".format(e))

    def home_reset(self):
        self.close_shutter()

        # self.console.raise_text("Instrument has been reset. Waiting for HOME position", 1)

        QGuiApplication.setOverrideCursor(Qt.WaitCursor)

        self.CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain
        # Make an SMIMotor object
        motor = self.CommInterface.GetMotor(1)

        # GOSUB5 - SMARTMOTOR
        try:
            self.CommInterface.WriteCommand("DOUTA0,b=7")
            self.CommInterface.WriteCommand("DOUTA0,b=3")
            self.CommInterface.WriteCommand("DOUTA0,b=7")
            self.CommInterface.WriteCommand("WAIT=500")

            # Initialize SMARTMOTOR variables
            self.CommInterface.WriteCommand("AMPS=100")
            self.CommInterface.WriteCommand("MP")
            self.CommInterface.WriteCommand("KGON")
            self.CommInterface.WriteCommand("KGOFF")
            self.CommInterface.WriteCommand("KP175")
            self.CommInterface.WriteCommand("KI=60")
            self.CommInterface.WriteCommand("F")

            # Sets velocity and acceleration of the motor

            self.CommInterface.WriteCommand("A=250")
            self.CommInterface.WriteCommand("V=25000")
            command = "a=UAI Ra"
            i = self.CommInterface.GetResponseOf(command)
            if i == '0':
                self.CommInterface.WriteCommand("i=@P-500")
                self.CommInterface.WriteCommand("P=i")
                self.CommInterface.WriteCommand("MP")
                self.CommInterface.WriteCommand("G")  # Make the filter move to next position
                motor.WaitForStop()

            self.CommInterface.WriteCommand("MV")
            self.CommInterface.WriteCommand("UAI")
            self.CommInterface.WriteCommand("G")  # Make the filter move to next position

            command = "a=UAI Ra"
            i = self.CommInterface.GetResponseOf(command)

            while i == '1':
                command = "a=UAI Ra"
                i = self.CommInterface.GetResponseOf(command)
            while i == '0':
                command = "a=UAI Ra"
                i = self.CommInterface.GetResponseOf(command)

            self.CommInterface.WriteCommand("A=200")
            self.CommInterface.WriteCommand("V=-750")
            self.CommInterface.WriteCommand("G")  # Make the filter move to position

            while i == '1':
                command = "a=UAI Ra"
                i = self.CommInterface.GetResponseOf(command)

            self.CommInterface.WriteCommand("A=2000")
            self.CommInterface.WriteCommand("X")
            # Call
            motor.WaitForStop()
            self.CommInterface.WriteCommand("WAIT=400")
            self.CommInterface.WriteCommand("O=1798")
            self.CommInterface.WriteCommand("MP")

            self.CommInterface.WriteCommand("A=250")
            self.CommInterface.WriteCommand("V=400000")
            self.CommInterface.WriteCommand("P=3333")
            self.CommInterface.WriteCommand("G")  # Make the filter move to position
            # Call
            motor.WaitForStop()
            self.CommInterface.WriteCommand("WAIT=500")
            self.CommInterface.WriteCommand("h=1")
            self.CommInterface.WriteCommand("RETURN")
            h_position = 1
            self.CommInterface.WriteCommand("g=-1")
            sleep(5)
            return h_position

        except Exception as e:
            print("Home reset ERROR -> {}".format(e))
        finally:
            QGuiApplication.restoreOverrideCursor()
            # self.console.raise_text("Instrument HOME position has been found.", 1)

    def get_current_filter(self):
        if self.connect_state:
            self.CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain

            sleep(0.5)
            self.CommInterface.WriteCommand("g=-1 GOSUB4")
            answer = self.CommInterface.ReadResponse()
            sleep(0.5)

            return answer[-1]
        else:
            return "None"

    def clear_buffer(self):
        self.CommInterface.ClearBuffer()

    def close_port(self):
        self.CommInterface.ClosePort()

    def filter_wheel_control(self, filter_number):
        # self.console.raise_text("Changing to filter #" + str(filter_number), 1)
        QGuiApplication.setOverrideCursor(Qt.WaitCursor)

        self.CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain

        h_position = int(self.get_current_filter())

        if filter_number == 1:
            command = "g=1"
        if filter_number == 2:
            command = "g=2"
        if filter_number == 3:
            command = "g=3"
        if filter_number == 4:
            command = "g=4"
        if filter_number == 5:
            command = "g=5"
        if filter_number == 6:
            command = "g=6"

        sleep(0.5)
        self.CommInterface.WriteCommand(command)  # Send filter position
        sleep(0.5)

        g = filter_number  # Filter position
        h = h_position  # Present position

        if h == 1:  # Present position is 3333
            if g < 5:
                self.CommInterface.WriteCommand("P=g*3333")
            if g == 5:  # Move in opposite direction
                self.CommInterface.WriteCommand("P=-3333")
            if g == 6:  # Move in opposite direction
                self.CommInterface.WriteCommand("P=0")

        if h == 2:  # Present position is 6666
            if g < 6:
                self.CommInterface.WriteCommand("P=g*3333")
            if g == 6:  # Move in opposite direction
                self.CommInterface.WriteCommand("P=0")

        if h == 3:  # Present position is 9999
            self.CommInterface.WriteCommand("P=g*3333")

        if h == 4:  # Present position is 13332
            self.CommInterface.WriteCommand("P=g*3333")

        if h == 5:  # Present position is 16665
            if g == 1:
                self.CommInterface.WriteCommand("P=23333")
            if g == 2:
                self.CommInterface.WriteCommand("P=26666")
            if g > 2:
                self.CommInterface.WriteCommand("P=g*3333")

        if h == 6:  # Present position is 20000
            if g == 1:
                self.CommInterface.WriteCommand("P=23333")
            if g == 2:
                self.CommInterface.WriteCommand("P=26666")
            if g > 2:
                self.CommInterface.WriteCommand("P=g*3333")

        self.CommInterface.WriteCommand("G")  # Make the filter move to next position
        sleep(1.5)  # Wait until the trajectory is finished

        self.CommInterface.WriteCommand("h=g")  # Reset the present filter position
        self.CommInterface.WriteCommand("O=h*3333")  # And reset the present origin
        self.CommInterface.WriteCommand("END")

        # self.console.raise_text("Filter position #" + str(filter_number), 1)

        QGuiApplication.restoreOverrideCursor()

        return filter_number
