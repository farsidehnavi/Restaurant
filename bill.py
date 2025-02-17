import pymongo
from tkinter import *
from tkinter.font import Font



client = pymongo.MongoClient('mongodb://localhost:27017/')
DB = client['ByPy']
DBAdmin = DB.Restaurant
DBOrder = DB.Order

def UI():

    global BillPage
    BillPage = Tk(className='bill')

    PageFont = Font(BillPage,family='Playwrite GB S ExtraLight',size=11)

    Label(BillPage,text='Bill !',font=PageFont).grid(column=0,row=0)

    global BillLabel
    BillLabel = Label(BillPage,font=PageFont)
    BillLabel.grid(column=0,row=1)

    
    global TotalLabel
    TotalLabel = Label(BillPage,font=PageFont)
    TotalLabel.grid(column=0,row=1)


ORDER = [i for i in DBOrder.find()]
print(ORDER)


FOODLIST = [i for i in DBAdmin.find()]


def LoadBill():
    TotalCost = 0
    for i in ORDER:
        print(FOODLIST[i])
    # TotalLabel.config(text=TotalCost)




LoadBill()




