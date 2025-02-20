import pymongo
from tkinter import *
from tkinter.font import Font



client = pymongo.MongoClient('mongodb://localhost:27017/')
DB = client['ByPy']
DBOrder = DB.Order

def UI():

    global BillPage
    BillPage = Tk(className='bill')

    PageFont = Font(BillPage,family='Comic Sans MS',size=11)

    Label(BillPage,text='Bill !',font=PageFont).grid(column=0,row=0)

    global BillLabel
    BillLabel = Label(BillPage,font=PageFont)
    BillLabel.grid(column=0,row=1)

    
    global TotalLabel
    TotalLabel = Label(BillPage,font=PageFont)
    TotalLabel.grid(column=0,row=2)


ORDER = [i for i in DBOrder.find()]




def LoadItems():
    FullTabel = ''
    for i in ORDER:
        FullTabel += f'{i['Name']}    {i['Price']}$\n'
    BillLabel.config(text=FullTabel)





def CalculateTotalCost():
    TotalCost = 0
    for i in ORDER:
        TotalCost += float(i['Price'])*100
    TotalLabel.config(text=str(TotalCost/100)+'$')




def Controller():
    UI()
    LoadItems()
    CalculateTotalCost()




