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
        hPosition_var = Main.FilterWheel_Control(6)
        lb["text"] = "              " + str(hPosition_var)
        sleep(1)
    except Exception as e:
        print(e)


def get_filter():
    try:
        resp = Main.get_filtro_atual()
        lb["text"] = "              " + str(resp)
        sleep(1)
    except Exception as e:
        print(e)


janela = Tk()

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

bt9 = Button(janela, text="GET FILTER", command=get_filter, bg="red")
#bt4.place(x=100, y=100)
bt9.pack()

lb = Label(janela)
lb.place(x=100, y=260)

# wxh+4+t
janela.geometry("300x300+200+200")

janela.mainloop()
