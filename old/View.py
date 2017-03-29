from time import sleep
from tkinter import *

from src import Main


def ABRIR():
    try:
        Main.open_shutter()
        sleep(1)
        lb["text"] = "Abriu shutter!!!"
    except Exception as e:
        print(e)


def FECHAR():
    try:
        Main.close_shutter()
        lb["text"] = "Fechou shutter!!!"

        sleep(1)
    except Exception as e:
        print(e)


def HOME_RESET():
    try:
        hPosition_var = Main.home_reset()
        print(hPosition_var)
        lb["text"] = "              " + str(hPosition_var)

        sleep(1)
    except Exception as e:
        print(e)


def F1():
    try:
        hPosition_var = Main.FilterWheel_Control(1)
        lb["text"] = "              " + str(hPosition_var)
        sleep(1)
    except Exception as e:
        print(e)


def F2():
    try:
        hPosition_var = Main.FilterWheel_Control(2)
        lb["text"] = "              " + str(hPosition_var)
        sleep(1)
    except Exception as e:
        print(e)


def F3():
    try:
        hPosition_var = Main.FilterWheel_Control(3)
        lb["text"] = "              " + str(hPosition_var)
        sleep(1)
    except Exception as e:
        print(e)


def F4():
    try:
        hPosition_var = Main.FilterWheel_Control(4)
        lb["text"] = "              " + str(hPosition_var)
        sleep(1)
    except Exception as e:
        print(e)


def F5():
    try:
        hPosition_var = Main.FilterWheel_Control(5)
        lb["text"] = "              " + str(hPosition_var)
        sleep(1)
    except Exception as e:
        print(e)


def F6():
    try:
        Main.clear_buffer()
        sleep(1)
        Main.closePort()
    except Exception as e:
        print(e)


def get_filter():
    try:
        Main.create_object()
        sleep(1)
    except Exception as e:
        print(e)


def test_loop():
    try:
        sleep(5)
        Main.open_shutter()
        sleep(5)
        Main.home_reset()
        sleep(5)

        lista = [5, 2, 3, 4, 5, 6, 5, 4]

        for x in lista:
            Main.FilterWheel_Control(x)
            sleep(10)

        sleep(1)
        Main.close_shutter()
        sleep(1)

        Main.clear_buffer()
        sleep(1)

        Main.closePort()
        sleep(1)
        print("END TEST LOOP")

    except Exception as e:
        print(e)


janela = Tk()

Main.home_reset()


janela.title = "Interface para testes"

bt1 = Button(janela, text="Abrir", command=ABRIR, bg="red")
#bt1.place(x=100, y=100)
bt1.pack()

bt2 = Button(janela, text="Fechar", command=FECHAR, bg="blue")
#bt2.place(x=100, y=100)
bt2.pack()

btHOME = Button(janela, text="HOME RESET", command=HOME_RESET, bg="green")
#bt3.place(x=100, y=100)
btHOME.pack()

bt3 = Button(janela, text="F1", command=F1, bg="white")
#bt3.place(x=100, y=100)
bt3.pack()

bt4 = Button(janela, text="F2", command=F2, bg="blue")
#bt4.place(x=100, y=100)
bt4.pack()

bt5 = Button(janela, text="F3", command=F3, bg="white")
#bt4.place(x=100, y=100)
bt5.pack()

bt6 = Button(janela, text="F4", command=F4, bg="blue")
#bt4.place(x=100, y=100)
bt6.pack()

bt7 = Button(janela, text="F5", command=F5, bg="white")
#bt4.place(x=100, y=100)
bt7.pack()

bt8 = Button(janela, text="F6", command=F6, bg="blue")
#bt4.place(x=100, y=100)
bt8.pack()

bt9 = Button(janela, text="Create Object", command=get_filter, bg="red")
#bt4.place(x=100, y=100)
bt9.pack()

bt10 = Button(janela, text="Test Loop", command=test_loop, bg="yellow")
#bt4.place(x=100, y=100)
bt10.pack()

lb = Label(janela)
lb.place(x=100, y=290)

# wxh+4+t
janela.geometry("320x320+250+250")

janela.mainloop()
