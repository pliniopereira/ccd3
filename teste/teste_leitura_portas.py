from time import sleep

import comtypes.client as cc

#Create SMIHost object and interface
smi = cc.CreateObject('SMIEngine.SMIHost')
cc.GetModule('IntegMotorInterface.dll')

import comtypes.gen.INTEGMOTORINTERFACELib

CommInterface = smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
CommInterface.BaudRate = 9600
CommInterface.OpenPort("Com2")
CommInterface.AddressMotorChain() #Address SmartMotors in the RS232 daisy chain
CommInterface.WriteCommand("UBO")  #Make sure USER Bit B is output bit (UBO)
CommInterface.WriteCommand("d=-1 GOSUB1")
while CommInterface.ReadResponse() != 'SHTR:???':



sleep(2)

#Make an SMIMotor object
# Motor = CommInterface.GetMotor(1)
#Send command to close shutter  'GOSUB 1 - SMARTMOTOR
#CommInterface.WriteCommand("UBO")  #Make sure USER Bit B is output bit (UBO)
#CommInterface.WriteCommand("UB=0") #Make sure shutter is in the closed state
#CommInterface.WriteCommand("UB=1")
