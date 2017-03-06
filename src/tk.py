'''
try:
    CommInterface.WriteCommand(u"UB=1")
except Exception as e:
    print(e)
finally:
    sleep(1)
    CommInterface.WriteCommand(u"UB=0")



def rojo():
    try:
        CommInterface.WriteCommand(u"UB=1")
        sleep(1)
        lb["text"] = "Funcionou!!!"
    except Exception as e:
        print(e)


def azul():
    try:
        CommInterface.WriteCommand(u"UB=0")
        sleep(1)
    except Exception as e:
        print(e)


def verde():
    try:
        CommInterface.WriteCommand(u"UB=-1")
        sleep(1)
    except Exception as e:
        print(e)



def uno():
    try:
        CommInterface.WriteCommand(u"UB=0")
        sleep(1)
    except Exception as e:
        print(e)


janela = Tk()


janela.title = "Interface para testes"


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


lb = Label(janela, text="Fala galera!!!")
lb.place(x=100, y=150)

# wxh+4+t
janela.geometry("300x300+200+200")

janela.mainloop()
'''