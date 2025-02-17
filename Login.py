from tkinter import *
from tkinter.font import Font



def UI():
    global LoginPage
    LoginPage = Tk(className='login')
    
    PageFont = Font(LoginPage,family='Playwrite GB S ExtraLight',size=11)

    Label(LoginPage,text='Login to Admin !',font=PageFont).grid(column=0,row=0)

    Username = Entry(LoginPage,font=PageFont)
    Username.grid(column=0,row=1)

    Password = Entry(LoginPage,font=PageFont)
    Password.grid(column=0,row=2)

    Button(LoginPage,text='Login',font=PageFont,command=lambda: Login(Username.get(),Password.get())).grid(column=0,row=4)

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
    import Admin
    # Admin.Window.mainloop()