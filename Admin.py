import pymongo
from tkinter import *
from tkinter.font import Font
# from PIL import Image, ImageDraw, ImageTk


client = pymongo.MongoClient('mongodb://localhost:27017/')
DB = client['ByPy']
DB = DB.Restaurant

EntryList = []


def AddToDB(Name,Price,SourceOfPrice,DateOfPrice):
    DB.insert_one({
        'Name':Name,
        'Price':Price,
        'SourceOfPrice':SourceOfPrice,
        'DateOfPrice':DateOfPrice
    })

def CheckIfAnyItemIsActive():
    return bool(StockList.curselection())

def Add():
    AddToDB(*[i.get() for i in EntryList])
    for i in range(len(EntryList)):
        EntryTextRemover(i)
    UpdateStockList()
    AddButton.config(text='Add')

def RemoveThisItem(ActiveItem):
    ActiveItemNumber = StockList.curselection()[0]
    DB.delete_one(DB.find()[ActiveItemNumber])

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
        ActiveItem = DB.find()[ActiveItemNumber]
        ActiveItemProperties = [ActiveItem['Name'],ActiveItem['Price'],ActiveItem['SourceOfPrice'],ActiveItem['DateOfPrice']]
        for i in range(4):
            EntryTextAdder(i,ActiveItemProperties[i])
        Remove()
        AddButton.config(text='Save changes')
        

def CheckIfAnyItemIsActive():
    return bool(StockList.curselection())


def FullInfoLabelUpdater(event):
    if CheckIfAnyItemIsActive():
        FullInfoGenerator()
        


def FullInfoGenerator():
    ActiveItemNumber = StockList.curselection()[0]
    ActiveItem = DB.find()[ActiveItemNumber]
    GeneratedText = f'{ActiveItem['Name']} was {ActiveItem['Price']} in {ActiveItem['DateOfPrice']} in {ActiveItem['SourceOfPrice']}'
    SelectedItemInfo.config(text=GeneratedText)



Window = Tk(className='car store')
Window.configure(bg='black')


# def rounded_rectangle(width, height, radius, color):
#     img = Image.new('RGBA', (width, height), (255, 0, 0, 0))
#     draw = ImageDraw.Draw(img)
#     draw.rounded_rectangle([0, 0, width, height], radius, fill=color)
#     return ImageTk.PhotoImage(img)





PageFont = Font(Window,family='Comic Sans MS',size=11)

Padx = 10
Pady = 5



# img_tk = rounded_rectangle(200,35,35,'olive')


header = Label(Window,text='Admin !',font=PageFont,bg='black',fg='white')
header.grid(row=0,column=0,columnspan=2,pady=Pady)

StockList = Listbox(Window,font=PageFont,bg='olive',fg='white')
StockList.grid(row=2,column=0,rowspan=8,padx=Padx)
StockList.bind("<<ListboxSelect>>", FullInfoLabelUpdater)

AddButton = Button(Window,text='Add',cursor='hand2',command=Add,font=PageFont,borderwidth=0,compound='center',bg='black',fg='white')
AddButton.grid(row=9,column=1,sticky='E,W',padx=Padx,pady=Pady)

UpdateButton = Button(Window,text='Update this Item',cursor='hand2',command=Update,font=PageFont,compound='center',borderwidth=0,fg='white',bg='black')
UpdateButton.grid(row=10,column=0,sticky='E,W',padx=Padx,pady=Pady)

RemoveButton = Button(Window,text='Remove this Item',cursor='hand2',command=Remove,font=PageFont,border=0,relief='solid',compound='center',bg='black',fg='white')
RemoveButton.grid(row=10,column=1,sticky='E,W',padx=Padx,pady=Pady)

SelectedItemInfo = Label(Window,bg='black',fg='white',font=PageFont)
SelectedItemInfo.grid(row=11,column=0,columnspan=2)


def CreateEntry(Row):
    EntryList.append(Entry(Window,bg='olive',font=PageFont,fg='white'))
    EntryList[-1].grid(row=Row,column=1,padx=Padx)


def EntryGenerator():
    for i in range(2,9,2):
        CreateEntry(i)

EntryGenerator()



def CreateLabel(Text,Row,Column):
    Item = Label(Window,text=Text,font=PageFont,bg='black',fg='white')
    Item.grid(row=Row,column=Column)


def LabelGenerator():
    for i in [['Stock list',1,0],['Name',1,1],['Price $',3,1],['Source of price',5,1],['Date of price',7,1]]:
        CreateLabel(i[0],i[1],i[2])

LabelGenerator()





def ClearStockList():
    StockList.delete(0,END)




def RefillStockList():
    for i in DB.find():
        StockList.insert(END,i['Name']+' '+i['Price']+'$')

def UpdateStockList():
    ClearStockList()
    RefillStockList()



RefillStockList()







Window.mainloop()



