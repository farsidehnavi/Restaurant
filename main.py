import pymongo
from tkinter import *
from tkinter.font import Font


client = pymongo.MongoClient('mongodb://localhost:27017/')
DB = client['ByPy']
# DB.create_collection('Restaurant')
# DB.create_collection('Order')
DBAdmin = DB.Restaurant
DBOrder = DB.Order



def UI():

    global HomePage
    HomePage = Tk(className='restaurant')
    HomePage.config(bg='black')

    SmallPageFont = Font(HomePage,family='Comic Sans MS',size=11)
    HugePageFont = Font(HomePage,family='Comic Sans MS',size=13)
    
    Padx = 10
    Pady = 5

    Label(HomePage,fg='white',bg='black',text='Welcome to our Restaurant !',font=HugePageFont,padx=10,pady=10).grid(row=0,column=0,columnspan=2)
    Label(HomePage,fg='white',bg='black',text='Stock',font=SmallPageFont,padx=10,pady=10).grid(row=1,column=0)
    Label(HomePage,fg='white',bg='black',text='Cart',font=SmallPageFont,padx=10,pady=10).grid(row=1,column=1)


    global StockListBox
    StockListBox = Listbox(HomePage,fg='white',bg='olive',font=SmallPageFont)
    StockListBox.grid(column=0,row=2,rowspan=1,padx=Padx,pady=Pady)
    StockListBox.bind("<<ListboxSelect>>", FullInfoLabelUpdater)

    global CartListBox
    CartListBox = Listbox(HomePage,fg='white',bg='olive',font=SmallPageFont)
    CartListBox.grid(column=1,row=2,padx=Padx,pady=Pady)
    
    
    global EmptyCartError
    EmptyCartError = Label(HomePage,font=SmallPageFont,text='At least you need to choose a product !',fg='red')

    global NothingIsSelectedError
    NothingIsSelectedError = Label(HomePage,font=SmallPageFont,text='No Item is selected !',fg='red')

    Button(HomePage,activebackground='black',activeforeground='black',font=HugePageFont,padx=Padx,pady=Pady,cursor='hand2',borderwidth=0,bg='black',fg='white',text='Add to Cart',command=AddToCart).grid(column=0,row=5,sticky='ew')
    Button(HomePage,activebackground='black',activeforeground='black',font=HugePageFont,padx=Padx,pady=Pady,cursor='hand2',borderwidth=0,bg='black',fg='white',text='Remove from cart',command=RemoveFromCart).grid(column=1,row=5,sticky='ew')
    Button(HomePage,activebackground='black',activeforeground='black',font=HugePageFont,padx=Padx,pady=Pady,cursor='hand2',borderwidth=0,bg='black',fg='white',text='Admin page',command=OpenLoginPage).grid(column=0,row=6,sticky='ew')
    Button(HomePage,activebackground='black',activeforeground='black',font=HugePageFont,padx=Padx,pady=Pady,cursor='hand2',borderwidth=0,bg='black',fg='white',text='Place order',command=PlaceOrder).grid(column=1,row=6,sticky='ew')
    
    global SelectedItemInfo
    SelectedItemInfo = Label(HomePage,bg='black',fg='white',font=SmallPageFont)
    SelectedItemInfo.grid(row=7,column=0,columnspan=2)


def _idRemover(inp):
    del inp['_id']
    return inp

FOODS = [_idRemover(i) for i in DBAdmin.find()]
ORDERS = [_idRemover(i) for i in DBOrder.find()]
Stock = []
Cart = []


class Food:
    def __init__(self,Name,Price):
        self.Name = Name
        self.Price = Price

    def AddToStockListBox(self):
        StockListBox.insert(END,'  '+self.Name+'  '+str(self.Price)+'$  ')

    def RemoveFromStockListBox(self):
        StockListBox.delete(self)

    def AddToCart(self):
        Cart.append(self)
        CartListBox.insert(END,'  '+self.Name+'  '+str(self.Price)+'$  ')

    def RemoveFromCart(self,ID):
        global Cart
        for i in range(len(Cart)):
            if Cart[i] == self:
                del Cart[i]
                break
        CartListBox.delete(ID)

    def ToDictFromDBAdmin(self,ID):
        ActiveItem = list(DBAdmin.find())[ID]
        return {
            'Name':ActiveItem['Name'],
            'Price':ActiveItem['Price'],
            'DateOfPrice':ActiveItem['DateOfPrice'],
            'SourceOfPrice':ActiveItem['SourceOfPrice']
        }
    
    def ToDictFromDBOrder(self,ID):
        ActiveItem = list(DBOrder.find())[ID]
        return {
            'Name':ActiveItem['Name'],
            'Price':ActiveItem['Price'],
            'DateOfPrice':ActiveItem['DateOfPrice'],
            'SourceOfPrice':ActiveItem['SourceOfPrice']
        }

    def AddToDBOrder(self,ID):
        DBOrder.insert_one(self.ToDictFromDBAdmin(ID))
        

    def RemoveFromDBOrder(self,ID):
        DBOrder.delete_one(self.ToDictFromDBOrder(ID))








def GenerateFoods():
    global Stock
    for i in FOODS:
        Stock.append(Food(i['Name'],i['Price']))
    for i in Stock:
        i.AddToStockListBox()


def GenerateOrders():
    for i in ORDERS:
        if i in FOODS:
            for j in Stock:
                if i['Name'] == j.Name and i['Price'] == j.Price:
                    j.AddToCart()
        else:
            DBOrder.delete_one({'Name':i['Name'],'Price':i['Price']})
            







def AddToCart():
    selected_indices = StockListBox.curselection()
    if selected_indices:
        Stock[selected_indices[0]].AddToCart()
        Stock[selected_indices[0]].AddToDBOrder(selected_indices[0])
    else:
        StockListBox.config(highlightbackground='red',highlightcolor='red')
        NothingIsSelectedError.grid(column=0,row=3,columnspan=2)

def RemoveFromCart():
    selected_indices = CartListBox.curselection()
    if selected_indices:
        Cart[selected_indices[0]].RemoveFromDBOrder(selected_indices[0])
        Cart[selected_indices[0]].RemoveFromCart(selected_indices[0])
    else:
        CartListBox.config(highlightbackground='red',highlightcolor='red')
        NothingIsSelectedError.grid(column=0,row=3,columnspan=2)



def OpenLoginPage():
    import Login
    Login.UI()
    HomePage.destroy()
    Login.LoginPage.mainloop()



def PlaceOrder():
    if len(Cart) != 0:
        import bill
        bill.Controller()
        bill.BillPage.mainloop()
        DBOrder.drop()
    else:
        CartListBox.config(highlightbackground='red',highlightcolor='red')
        EmptyCartError.grid(column=0,row=4,columnspan=2)
    
    
    
    
def CheckIfAnyItemIsActive():
    return bool(StockListBox.curselection())


def FullInfoLabelUpdater(event):
    if CheckIfAnyItemIsActive():
        FullInfoGenerator()
        


def FullInfoGenerator():
    ActiveItemNumber = StockListBox.curselection()[0]
    ActiveItem = DBAdmin.find()[ActiveItemNumber]
    GeneratedText = f'{ActiveItem['Name']} was {ActiveItem['Price']} in {ActiveItem['DateOfPrice']} in {ActiveItem['SourceOfPrice']}'
    SelectedItemInfo.config(text=GeneratedText)










def Controller():
    UI()
    GenerateFoods()
    GenerateOrders()
    HomePage.mainloop()
Controller()












