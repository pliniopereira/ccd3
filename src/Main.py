from time import sleep

import comtypes.client as cc
from tkinter import *

smi = cc.CreateObject('SMIEngine.SMIHost')
#print(dir(smi))
cc.GetModule('IntegMotorInterface.dll')

import comtypes.gen.INTEGMOTORINTERFACELib

smiCom = smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
#print(dir(smiCom))
smiCom.BaudRate = 9600

try:
    smiCom.OpenPort("Com2")
except Exception as e:
    print(e)

#smiCom.AddressMotorChain

#['AddNetMotor', 'AddRef', 'AddressMotorChain', 'AddressServos', 'BaudRate', 'BytesAvailable', 'CharDelay', 'ClearBuffer',
#  'ClearEEPROM', 'ClosePort', 'DefaultMotor', 'DetectNetMotors', 'DetectRS232', 'DetectRS485', 'DetectUSBMotors',
#  'Download', 'Echo', 'EchoTimeoutConst', 'EchoTimeoutMul', 'EngineVersion', 'EstablishChain', 'ForceUpload',
#  'GetIDsOfNames', 'GetMotor','GetResponseOf', 'GetTypeInfo', 'GetTypeInfoCount', 'InitEthernet', 'InitRS485', 'InitUSB',
#  'InitializeNotification', 'Invoke', 'IsRS485', 'LogFileName', 'LogFlags', 'MaxMotors', 'NoOfMotors', 'OpenPort',
#  'Parity', 'PortHandle', 'PortName', 'QueryInterface', 'ReadResponse', 'ReadString', 'Release', 'ReorderMotors',
#  'Timeout', 'TxMaxRetry', 'TxTimeoutConst', 'TxTimeoutMul', 'Upload', 'Wait', 'WriteCmd', 'WriteCommand', 'WriteString',
'''
try:
    smiCom.WriteCommand(u"UB=1")
except Exception as e:
    print(e)
finally:
    sleep(1)
    smiCom.WriteCommand(u"UB=0")
'''


def rojo():
    try:
        smiCom.WriteCommand(u"UB=1")
        sleep(1)
    except Exception as e:
        print(e)


def azul():
    try:
        smiCom.WriteCommand(u"UB=0")
        sleep(1)
    except Exception as e:
        print(e)


def verde():
    pass


def uno():
    pass


janela = Tk()

'''
root.title = "Interfaz comunicacion serial"

rojo = Tk.Button(root, text="Abrir", command=rojo, bg="red")
rojo.pack()
azul = Tk.Button(root, text="Fechar", command=azul, bg="blue")
azul.pack()
verde = Tk.Button(root, text="NULL", command=verde, bg="green")
verde.pack()
num1 = Tk.Button(root, text="NULL", command=uno)
num1.pack()
'''

bt1 = Button(janela, text="Abrir", command=rojo, bg="red")
#bt1.place(x=100, y=100)
bt1.pack()

bt2 = Button(janela, text="Fechar", command=azul, bg="blue")
#bt2.place(x=100, y=100)
bt2.pack()

bt3 = Button(janela, text="NULL", command=verde, bg="green")
#bt3.place(x=100, y=100)
bt3.pack()

bt4 = Button(janela, text="NULL", command=uno)
#bt4.place(x=100, y=100)
bt4.pack()

# wxh+4+t
janela.geometry("300x300+200+200")

janela.mainloop()
