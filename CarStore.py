import pymongo
from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageDraw, ImageTk


client = pymongo.MongoClient('mongodb://localhost:27017/')
DB = client['ByPy']

EntryList = []


def AddToDB(Brand,Model,PowerHP,Cost):
    DB.Cars.insert_one({
        'Brand':Brand,
        'Model':Model,
        'PowerHP':PowerHP,
        'Cost':Cost
    })

def CheckIfAnyItemIsActive():
    return bool(StockList.curselection())

def Add():
    AddToDB(*[i.get() for i in EntryList])
    for i in range(len(EntryList)):
        EntryTextRemover(i)
    UpdateStockList()

def RemoveThisItem(ActiveItem):
    ActiveItemNumber = StockList.curselection()[0]
    DB.Cars.delete_one(DB.Cars.find()[ActiveItemNumber])

def Remove():
    if CheckIfAnyItemIsActive():
        RemoveThisItem(StockList.curselection()[0])
    UpdateStockList()


def EntryTextAdder(Index,NewText):
    EntryList[Index].delete(0, END)
    EntryList[Index].insert(0, NewText)

def EntryTextRemover(Index):
    EntryList[Index].delete(0, END)

def Update():
    if CheckIfAnyItemIsActive():
        ActiveItemNumber = StockList.curselection()[0]
        ActiveItem = DB.Cars.find()[ActiveItemNumber]
        ActiveItemProperties = [ActiveItem['Brand'],ActiveItem['Model'],ActiveItem['PowerHP'],ActiveItem['Cost']]
        for i in range(4):
            EntryTextAdder(i,ActiveItemProperties[i])
        Remove()


def FullInfoLabelUpdater(event):
    if CheckIfAnyItemIsActive():
        FullInfoGenerator()


def FullInfoGenerator():
    ActiveItemNumber = StockList.curselection()[0]
    ActiveItem = DB.Cars.find()[ActiveItemNumber]
    GeneratedText = f'{ActiveItem['Brand']+' '+ActiveItem['Model']} with {ActiveItem['PowerHP']} HP and the cost of {ActiveItem['Cost']}$'
    FullInfoLabel.config(text=GeneratedText)





Window = Tk(className='car store')
Window.configure(bg='black')


def rounded_rectangle(width, height, radius, color):
    img = Image.new('RGBA', (width, height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, width, height], radius, fill=color)
    return ImageTk.PhotoImage(img)





PageFont = Font(Window,family='Playwrite GB S ExtraLight',size=11)

Padx = 10
Pady = 5



img_tk = rounded_rectangle(200,35,35,'olive')


header = Label(Window,text='Car store',font=PageFont,bg='black',fg='white')
header.grid(row=0,column=0,columnspan=2,pady=Pady)

StockList = Listbox(Window,font=PageFont,bg='olive',fg='white')
StockList.grid(row=2,column=0,rowspan=8,padx=Padx)
StockList.bind("<<ListboxSelect>>", FullInfoLabelUpdater)

AddButton = Button(Window,text='Add',cursor='hand2',command=Add,font=PageFont,image=img_tk,borderwidth=0,compound='center',bg='black',fg='white')
AddButton.grid(row=9,column=1,sticky='E,W',padx=Padx,pady=Pady)

UpdateButton = Button(Window,text='Update this Item',cursor='hand2',command=Update,font=PageFont,image=img_tk,compound='center',borderwidth=0,fg='white',bg='black')
UpdateButton.grid(row=10,column=0,sticky='E,W',padx=Padx,pady=Pady)

RemoveButton = Button(Window,text='Remove this Item',cursor='hand2',command=Remove,font=PageFont,border=0,relief='solid',image=img_tk,compound='center',bg='black',fg='white')
RemoveButton.grid(row=10,column=1,sticky='E,W',padx=Padx,pady=Pady)

FullInfoLabel = Label(Window,font=PageFont,bg='black',fg='white')
FullInfoLabel.grid(row=15,column=0,columnspan=2,pady=Pady,padx=Padx)











def CreateEntry(Row,Column):
    EntryList.append(Entry(Window,bg='olive',font=PageFont,fg='white'))
    EntryList[-1].grid(row=Row,column=Column,padx=Padx)


def EntryGenerator():
    for i in [[2,1],[4,1],[6,1],[8,1]]:
        CreateEntry(i[0],i[1])

EntryGenerator()



def CreateLabel(Text,Row,Column):
    Item = Label(Window,text=Text,font=PageFont,bg='black',fg='white')
    Item.grid(row=Row,column=Column)


def LabelGenerator():
    for i in [['Stock list',1,0],['Brand',1,1],['Model',3,1],['Hourse Power',5,1],['Cost $',7,1]]:
        CreateLabel(i[0],i[1],i[2])

LabelGenerator()












def ClearStockList():
    StockList.delete(0,END)




def RefillStockList():
    for i in DB.Cars.find():
        StockList.insert(END,i['Brand']+' '+i['Model'])

def UpdateStockList():
    ClearStockList()
    RefillStockList()



RefillStockList()















Window.mainloop()



