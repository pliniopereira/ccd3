from time import sleep

import comtypes.client as cc

from src import Leitura_portas


#Create SMIHost object and interface
smi = cc.CreateObject('SMIEngine.SMIHost')
cc.GetModule('IntegMotorInterface.dll')

import comtypes.gen.INTEGMOTORINTERFACELib

CommInterface = smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
CommInterface.BaudRate = 9600

serial_var = Leitura_portas.serial_ports()
count_aux = int(len(serial_var))

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

CommInterface.AddressMotorChain() #Address SmartMotors in the RS232 daisy chain
#Make an SMIMotor object
Motor = CommInterface.GetMotor(1)


def open_shutter():
    CommInterface.WriteCommand("UB=1")  # Make sure shutter is in the closed state


def close_shutter():
    CommInterface.WriteCommand("UB=0")


def home_reset():
    '''
    GOSUB5 - SMARTMOTOR
    '''
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
        CommInterface.WriteCommand("g=-1")

        return hPosition

    except Exception as e:
        print(e)


def get_filtro_atual():
    CommInterface.WriteCommand("g=-1 GOSUB4")
    resposta = CommInterface.ReadResponse()
    return resposta[-1]


def FilterWheel_Control(FilterNumber):
    '''
    :param FilterNumber:
    :return:
    '''
    hPosition = int(get_filtro_atual())
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

    CommInterface.WriteCommand(command)       #Send filter position
    g = FilterNumber                            #Filter position
    h = hPosition                               #Present position

    if h == 1: #Present position is 3333
        if g < 5:
            CommInterface.WriteCommand("P=g*3333")
        if g == 5: #Move in opposite direction
            CommInterface.WriteCommand("P=-3333")
        if g == 6: #Move in opposite direction
            CommInterface.WriteCommand("P=0")

    if h == 2: #Present position is 6666
        if g < 6:
            CommInterface.WriteCommand("P=g*3333")
        if g == 6: #Move in opposite direction
            CommInterface.WriteCommand("P=0")

    if h == 3: #Present position is 9999
        CommInterface.WriteCommand("P=g*3333")

    if h == 4: #Present position is 13332
        CommInterface.WriteCommand("P=g*3333")

    if h == 5: #Present position is 16665
        if g == 1:
            CommInterface.WriteCommand("P=23333")
        if g == 2:
            CommInterface.WriteCommand("P=-26666")
        if g > 2:
            CommInterface.WriteCommand("P=g*3333")

    if h == 6: #Present position is 20000
        if g == 1:
            CommInterface.WriteCommand("P=23333")
        if g == 2:
            CommInterface.WriteCommand("P=26666")
        if g > 2:
            CommInterface.WriteCommand("P=g*3333")

    CommInterface.WriteCommand("G") #Make the filter move to next position
    sleep(1.5) #Wait until the trajectory is finished

    CommInterface.WriteCommand("h=g") #Reset the present filter position
    CommInterface.WriteCommand("O=h*3333") #And reset the present origin
    CommInterface.WriteCommand("END")
    hPosition = FilterNumber #h receive g for VB use
    return FilterNumber

hPosition_var = home_reset()

print(hPosition_var)


'''
open_shutter()
close_shutter()
hPosition_var = FilterWheel_Control(4, hPosition_var)
print(hPosition_var)
hPosition_var = FilterWheel_Control(2, hPosition_var)
print(hPosition_var)
close_shutter()
open_shutter()

hPosition_var = FilterWheel_Control(3, hPosition_var)
print(hPosition_var)
hPosition_var = FilterWheel_Control(5, hPosition_var)
print(hPosition_var)
hPosition_var = FilterWheel_Control(6, hPosition_var)
print(hPosition_var)
hPosition_var = FilterWheel_Control(1, hPosition_var)
print(hPosition_var)
hPosition_var = FilterWheel_Control(6, hPosition_var)
print(hPosition_var)
'''