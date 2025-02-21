import pymongo
from tkinter import *
from tkinter.font import Font



client = pymongo.MongoClient('mongodb://localhost:27017/')
DB = client['ByPy']
DBOrder = DB.Order

def UI():

    global BillPage
    BillPage = Tk(className='bill')
    BillPage.config(bg='black')


    SmallPageFont = Font(BillPage,family='Comic Sans MS',size=11)
    HugePageFont = Font(BillPage,family='Comic Sans MS',size=13)
    
    Padx = 10
    Pady = 5

    Label(BillPage,text='Thanks for buying !',font=HugePageFont,fg='white',bg='black').grid(column=0,row=0,padx=Padx,pady=Pady)

    global BillLabel
    BillLabel = Label(BillPage,font=SmallPageFont,fg='white',bg='black')
    BillLabel.grid(column=0,row=1,padx=Padx,pady=Pady)

    
    global TotalLabel
    TotalLabel = Label(BillPage,font=HugePageFont,fg='white',bg='black')
    TotalLabel.grid(column=0,row=2,padx=Padx,pady=Pady)


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




DBOrder.delete_many({})