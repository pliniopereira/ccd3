from time import sleep

import comtypes.client as cc
import comtypes.gen.INTEGMOTORINTERFACELib
from PyQt5 import QtCore

from src.utils.rodafiltros import Leitura_portas


class FilterControl(QtCore.QThread):

    def __init__(self, parent=None):
        super(FilterControl, self).__init__(parent)
        self.smi = cc.CreateObject('SMIEngine.SMIHost')
        cc.GetModule('IntegMotorInterface.dll')
        self.CommInterface = self.smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
        self.create_object()

    def create_object(self):
        sleep(10)
        CommInterface = self.CommInterface
        smi = self.smi

        CommInterface.BaudRate = 9600

        serial_var = Leitura_portas.serial_ports()
        count_aux = int(len(serial_var))

        for count in range(0, count_aux):
            print("Search for " + serial_var[count] + " link to Motors!")
            try:
                CommInterface.OpenPort("COM2")
                CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain
                CommInterface.WriteCommand("UBO")  # Make sure USER Bit B is output bit (UBO)
                CommInterface.WriteCommand("d=-1 GOSUB1")
                resposta = CommInterface.ReadResponse()
                if resposta == 'SHTR:???':
                    print(serial_var[count] + " - Established a link to Motors!")
                    break
            except Exception as e:
                print(serial_var[count] + " - Cannot establish a link to Motors")

        return smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)

    def open_shutter(self):
        CommInterface = self.CommInterface

        try:
            CommInterface.WriteCommand("UB=1")  # Make sure shutter is in the closed state
            sleep(1)
        except Exception as e:
            print("open_shutter")
            print(e)

    def close_shutter(self):
        CommInterface = self.CommInterface

        try:
            CommInterface.WriteCommand("UB=0")
            sleep(1)
        except Exception as e:
            print("close_shutter")
            print(e)

    def home_reset(self):
        CommInterface = self.CommInterface
        CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain
        # Make an SMIMotor object
        Motor = CommInterface.GetMotor(1)
        '''
        GOSUB5 - SMARTMOTOR
        '''
        try:
            DefaultMotor = 1
            CommInterface.WriteCommand("DOUTA0,b=7")
            CommInterface.WriteCommand("DOUTA0,b=3")
            CommInterface.WriteCommand("DOUTA0,b=7")
            CommInterface.WriteCommand("WAIT=500")

            # Initializa SMARTMOTOR variables
            CommInterface.WriteCommand("AMPS=100")
            CommInterface.WriteCommand("MP")
            CommInterface.WriteCommand("KGON")
            CommInterface.WriteCommand("KGOFF")
            CommInterface.WriteCommand("KP175")
            CommInterface.WriteCommand("KI=60")
            CommInterface.WriteCommand("F")

            # Sets velocity and acceleration of the motor

            CommInterface.WriteCommand("A=250")
            CommInterface.WriteCommand("V=25000")
            command = "a=UAI Ra"
            i = CommInterface.GetResponseOf(command)
            if i == 0:
                CommInterface.WriteCommand("i=@P-500")
                CommInterface.WriteCommand("P=i")
                CommInterface.WriteCommand("MP")
                CommInterface.WriteCommand("G")  # Make the filter move to next position
                Motor.WaitForStop()

            CommInterface.WriteCommand("MV")
            CommInterface.WriteCommand("UAI")
            CommInterface.WriteCommand("G")  # Make the filter move to next position

            command = "a=UAI Ra"
            i = CommInterface.GetResponseOf(command)

            while i == 1:
                command = "a=UAI Ra"
                i = CommInterface.GetResponseOf(command)
            while i == 0:
                command = "a=UAI Ra"
                i = CommInterface.GetResponseOf(command)

            CommInterface.WriteCommand("A=200")
            CommInterface.WriteCommand("V=-750")
            CommInterface.WriteCommand("G")  # Make the filter move to position

            while i == 1:
                command = "a=UAI Ra"
                i = CommInterface.GetResponseOf(command)

            CommInterface.WriteCommand("A=2000")
            CommInterface.WriteCommand("X")
            # Call
            Motor.WaitForStop()
            CommInterface.WriteCommand("WAIT=400")
            CommInterface.WriteCommand("O=1798")
            CommInterface.WriteCommand("MP")

            CommInterface.WriteCommand("A=250")
            CommInterface.WriteCommand("V=400000")
            CommInterface.WriteCommand("P=3333")
            CommInterface.WriteCommand("G")  # Make the filter move to position
            # Call
            Motor.WaitForStop()
            CommInterface.WriteCommand("WAIT=500")
            CommInterface.WriteCommand("h=1")
            CommInterface.WriteCommand("RETURN")
            hPosition = 1
            CommInterface.WriteCommand("g=-1")
            sleep(5)

            return hPosition

        except Exception as e:
            print("------------------------------------")
            print("Home reset ERROR")
            print(e)
            print("------------------------------------")
        finally:
            print("Home Reset OK")
            print(hPosition)

    def get_filtro_atual(self):
        CommInterface = self.CommInterface

        sleep(2)
        CommInterface.WriteCommand("g=-1 GOSUB4")
        resposta = CommInterface.ReadResponse()
        sleep(2)

        return resposta[-1]

    def clear_buffer(self):
        CommInterface = self.CommInterface

        CommInterface.ClearBuffer()

    def closePort(self):
        CommInterface = self.CommInterface

        CommInterface.ClosePort()

    def FilterWheel_Control(self, FilterNumber):
        '''
        :param FilterNumber: 
        :return: 
        '''

        CommInterface = self.CommInterface

        CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain

        hPosition = int(self.get_filtro_atual())

        if FilterNumber == 1:
            command = "g=1"
        if FilterNumber == 2:
            command = "g=2"
        if FilterNumber == 3:
            command = "g=3"
        if FilterNumber == 4:
            command = "g=4"
        if FilterNumber == 5:
            command = "g=5"
        if FilterNumber == 6:
            command = "g=6"

        sleep(1)
        CommInterface.WriteCommand(command)  # Send filter position
        sleep(1)

        g = int(FilterNumber)  # Filter position
        h = int(hPosition)  # Present position

        if h == 1:  # Present position is 3333
            if g < 5:
                CommInterface.WriteCommand("P=g*3333")
            if g == 5:  # Move in opposite direction
                CommInterface.WriteCommand("P=-3333")
            if g == 6:  # Move in opposite direction
                CommInterface.WriteCommand("P=0")

        if h == 2:  # Present position is 6666
            if g < 6:
                CommInterface.WriteCommand("P=g*3333")
            if g == 6:  # Move in opposite direction
                CommInterface.WriteCommand("P=0")

        if h == 3:  # Present position is 9999
            CommInterface.WriteCommand("P=g*3333")

        if h == 4:  # Present position is 13332
            CommInterface.WriteCommand("P=g*3333")

        if h == 5:  # Present position is 16665
            if g == 1:
                CommInterface.WriteCommand("P=23333")
            if g == 2:
                CommInterface.WriteCommand("P=-26666")
            if g > 2:
                CommInterface.WriteCommand("P=g*3333")

        if h == 6:  # Present position is 20000
            if g == 1:
                CommInterface.WriteCommand("P=23333")
            if g == 2:
                CommInterface.WriteCommand("P=26666")
            if g > 2:
                CommInterface.WriteCommand("P=g*3333")

        CommInterface.WriteCommand("G")  # Make the filter move to next position
        sleep(1.5)  # Wait until the trajectory is finished

        CommInterface.WriteCommand("h=g")  # Reset the present filter position
        CommInterface.WriteCommand("O=h*3333")  # And reset the present origin
        CommInterface.WriteCommand("END")
        hPosition = FilterNumber  # h receive g for VB use
        print("----------------------------------------------------")

        print(FilterNumber)

        print("----------------------------------------------------")
        return FilterNumber
