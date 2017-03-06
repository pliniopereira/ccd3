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