from tkinter import *
from tkinter.font import Font



def UI():
    global LoginPage
    LoginPage = Tk(className='login')
    LoginPage.config(bg='black')

    SmallPageFont = Font(LoginPage,family='Comic Sans MS',size=11)
    HugePageFont = Font(LoginPage,family='Comic Sans MS',size=13)

    Padx = 10
    Pady = 5

    Label(LoginPage,bg='black',fg='white',text='Login to Admin !',font=HugePageFont).grid(column=0,row=0,padx=Padx,pady=Pady)

    Username = Entry(LoginPage,font=SmallPageFont,fg='white',bg='olive')
    Username.grid(column=0,row=1,padx=Padx,pady=Pady)

    Password = Entry(LoginPage,font=SmallPageFont,fg='white',bg='olive')
    Password.grid(column=0,row=2,padx=Padx,pady=Pady)

    Button(LoginPage,activebackground='black',activeforeground='black',cursor='hand2',borderwidth=0,bg='black',fg='white',text='Login',font=HugePageFont,command=lambda: Login(Username.get(),Password.get())).grid(column=0,row=4,padx=Padx,pady=Pady,sticky='EW')

def Login(Username,Password):
    if Username == 'admin':
        if Password == 'admin':
            OpenAdmin()
        else:
            ShowLoginError()
    else:
        ShowLoginError()

def ShowLoginError():
    Label(LoginPage,text='Username or Password incorrect !',fg='red').grid(column=0,row=3)

def OpenAdmin():
    LoginPage.destroy()
    import Admin