from time import sleep

import comtypes.client as cc

smi = cc.CreateObject('SMIEngine.SMIHost')
#print(dir(smi))
cc.GetModule('IntegMotorInterface.dll')

import comtypes.gen.INTEGMOTORINTERFACELib

CommInterface = smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
#print(dir(CommInterface))
CommInterface.BaudRate = 9600
CommInterface.OpenPort("Com2")
CommInterface.AddressMotorChain()
Motor = CommInterface.GetMotor(1)
CommInterface.WriteCommand("UBO")  #Make sure USER Bit B is output bit (UBO)
CommInterface.WriteCommand("UB=0") #Make sure shutter is in the closed state
#CommInterface.WriteCommand("UB=1") #Make sure shutter is in the closed state


#Home Reset
def home_reset():
    try:
        CommInterface.DefaultMotor = 1
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

        #Sets velocity and acceleration of the motor

        CommInterface.WriteCommand("A=250")
        CommInterface.WriteCommand("V=25000")
        command = "a=UAI Ra"
        i = CommInterface.GetResponseOf(command)
        if i == 0:

            CommInterface.WriteCommand("i=@P-500")
            CommInterface.WriteCommand("P=i")
            CommInterface.WriteCommand("MP")
            CommInterface.WriteCommand("G") #Make the filter move to next position
            Motor.WaitForStop()

        CommInterface.WriteCommand("MV")
        CommInterface.WriteCommand("UAI")
        CommInterface.WriteCommand("G")         #Make the filter move to next position

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
        CommInterface.WriteCommand("G") #Make the filter move to position

        while i == 1:
            command = "a=UAI Ra"
            i = CommInterface.GetResponseOf(command)

        CommInterface.WriteCommand("A=2000")
        CommInterface.WriteCommand("X")
        #Call
        Motor.WaitForStop()
        CommInterface.WriteCommand("WAIT=400")
        CommInterface.WriteCommand("O=1798")
        CommInterface.WriteCommand("MP")

        CommInterface.WriteCommand("A=250")
        CommInterface.WriteCommand("V=400000")
        CommInterface.WriteCommand("P=3333")
        CommInterface.WriteCommand("G") #Make the filter move to position
        #Call
        Motor.WaitForStop()
        CommInterface.WriteCommand("WAIT=500")
        CommInterface.WriteCommand("h=1")
        CommInterface.WriteCommand("RETURN")
        hPosition = 1

    except Exception as e:
        print(e)


home_reset()


        #['AddNetMotor', 'AddRef', 'AddressMotorChain', 'AddressServos', 'BaudRate', 'BytesAvailable', 'CharDelay', 'ClearBuffer',
#  'ClearEEPROM', 'ClosePort', 'DefaultMotor', 'DetectNetMotors', 'DetectRS232', 'DetectRS485', 'DetectUSBMotors',
#  'Download', 'Echo', 'EchoTimeoutConst', 'EchoTimeoutMul', 'EngineVersion', 'EstablishChain', 'ForceUpload',
#  'GetIDsOfNames', 'GetMotor','GetResponseOf', 'GetTypeInfo', 'GetTypeInfoCount', 'InitEthernet', 'InitRS485', 'InitUSB',
#  'InitializeNotification', 'Invoke', 'IsRS485', 'LogFileName', 'LogFlags', 'MaxMotors', 'NoOfMotors', 'OpenPort',
#  'Parity', 'PortHandle', 'PortName', 'QueryInterface', 'ReadResponse', 'ReadString', 'Release', 'ReorderMotors',
#  'Timeout', 'TxMaxRetry', 'TxTimeoutConst', 'TxTimeoutMul', 'Upload', 'Wait', 'WriteCmd', 'WriteCommand', 'WriteString',