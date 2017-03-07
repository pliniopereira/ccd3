import glob
import sys
from datetime import datetime

import comtypes.client as cc
import serial


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    serial_var = serial_ports()
    count_aux = int(len(serial_var))
    smi = cc.CreateObject('SMIEngine.SMIHost')
    cc.GetModule('IntegMotorInterface.dll')

    import comtypes.gen.INTEGMOTORINTERFACELib

    CommInterface = smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
    CommInterface.BaudRate = 9600
    resposta = ''
    count = 0
    for count in range(0, count_aux):
        print("Search for " + serial_var[count] + " link to Motors!")
        try:
            CommInterface.OpenPort(serial_var[count])
            CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain
            CommInterface.WriteCommand("UBO")  # Make sure USER Bit B is output bit (UBO)
            CommInterface.WriteCommand("d=-1 GOSUB1")
            resposta = CommInterface.ReadResponse()
            if resposta == 'SHTR:???':
                print(serial_var[count] + " - Established a link to Motors!")
                break
        except Exception as e:
            print(serial_var[count] + " - Cannot establish a link to Motors")

    print(datetime.now())

