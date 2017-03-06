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

def FilterWheel_Control(FilterNumber):
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
    hPosition = 1
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


FilterWheel_Control(1)