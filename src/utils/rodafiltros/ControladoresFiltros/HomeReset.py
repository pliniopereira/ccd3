from time import sleep


def home_reset(objeto, motor):
    '''
    GOSUB5 - SMARTMOTOR
    '''
    objeto = CommInterface
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
