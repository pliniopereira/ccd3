from time import sleep


def open_shutter(objeto):

    try:
        objeto.WriteCommand("UB=1")  # Make sure shutter is in the closed state
        sleep(1)
    except Exception as e:
        print(e)


def close_shutter(objeto):
    try:
        objeto.WriteCommand("UB=0")
        sleep(1)
    except Exception as e:
        print(e)