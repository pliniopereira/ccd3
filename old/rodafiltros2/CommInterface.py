from time import sleep

import comtypes.client as cc

from src import Leitura_portas


def create_object():
    sleep(10)
    #Create SMIHost object and interface
    smi = cc.CreateObject('SMIEngine.SMIHost')
    cc.GetModule("IntegMotorInterface.dll")

    import comtypes.gen.INTEGMOTORINTERFACELib

    CommInterface = smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
    CommInterface.BaudRate = 9600

    serial_var = Leitura_portas.serial_ports()
    count_aux = int(len(serial_var))

    for count in range(0, count_aux):
        print("Search for " + serial_var[count] + " link to Motors!")
        try:
            CommInterface.OpenPort('COM2')
            CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain
            CommInterface.WriteCommand("UBO")  # Make sure USER Bit B is output bit (UBO)
            CommInterface.WriteCommand("d=-1 GOSUB1")
            resposta = CommInterface.ReadResponse()
            if resposta == 'SHTR:???':
                print(serial_var[count] + " - Established a link to Motors!")
                break
        except Exception as e:
            print(serial_var[count] + " - Cannot establish a link to Motors")

    CommInterface.AddressMotorChain() #Address SmartMotors in the RS232 daisy chain
    #Make an SMIMotor object
    Motor = CommInterface.GetMotor(1)

    return smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm), Motor
