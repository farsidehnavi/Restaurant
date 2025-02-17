import pymongo
from tkinter import *
from tkinter.font import Font


client = pymongo.MongoClient('mongodb://localhost:27017/')
DB = client['ByPy']
# DB.create_collection('Order')
DBAdmin = DB.Restaurant
DBOrder = DB.Order



def UI():

    global HomePage
    HomePage = Tk(className='restaurant')

    PageFont = Font(HomePage,family='Playwrite GB S ExtraLight',size=11)

    Label(HomePage,text='Welcome to our Restaurant !',font=PageFont,padx=10,pady=10).grid(row=0,column=0,columnspan=2)
    Label(HomePage,text='Stock',font=PageFont,padx=10,pady=10).grid(row=1,column=0)
    Label(HomePage,text='Cart',font=PageFont,padx=10,pady=10).grid(row=1,column=1)


    global StockListBox
    StockListBox = Listbox(HomePage,font=PageFont)
    StockListBox.grid(column=0,row=2,rowspan=1)

    global CartListBox
    CartListBox = Listbox(HomePage,font=PageFont)
    CartListBox.grid(column=1,row=2)
    
    
    global EmptyCartError
    EmptyCartError = Label(HomePage,font=PageFont,text='At least you need to select one product !',fg='red')


    Button(HomePage,text='Add to Cart',command=AddToCart).grid(column=0,row=4,sticky='ew')

    Button(HomePage,text='Remove from cart',command=RemoveFromCart).grid(column=1,row=4,sticky='ew')


    Button(HomePage,text='Admin page',command=OpenLoginPage).grid(column=0,row=5,sticky='ew')

    Button(HomePage,text='Place order',command=PlaceOrder).grid(column=1,row=5,sticky='ew')



# FOODS = [
#     ['Pizza',12.99],
#     ['Burger',9.99],
#     ['Pasta',11.99],
#     ['Salad',7.99]
# ]


FOODS = [i for i in DBAdmin.find()]


ORDERS = [i[''] for i in DBOrder.find()]


FoodList = []

Cart = []

class Food:
    def __init__(self,Name,Price):
        self.Name = Name
        self.Price = Price

    def AddToStockListBox(self):
        StockListBox.insert(END,'  '+self.Name+'  '+str(self.Price)+'$  ')

    def RemoveFromStockListBox(self,ID):
        StockListBox.delete(ID)

    def AddToCart(self,ID):
        Cart.append(ID)
        CartListBox.insert(END,'  '+self.Name+'  '+str(self.Price)+'$  ')

    def AddToDBOrder(self,ID):
        DBOrder.insert_one({'':ID})

    def RemoveFromCart(self,ID):
        Cart.remove(Cart[ID])
        CartListBox.delete(ID)

    def RemoveFromDBOrder(self,ID):
        DBOrder.delete_one({'':ID})








def GenerateFoods():
    global FoodList
    for i in FOODS:
        FoodList.append(Food(i['Name'],i['Cost']))
    for i in FoodList:
        i.AddToStockListBox()


def GenerateOrders():
    global Cart
    for i in ORDERS:
        FoodList[i].AddToCart(i)







def AddToCart():
    selected_indices = StockListBox.curselection()
    if(selected_indices):
        FoodList[selected_indices[0]].AddToCart(selected_indices[0])
        FoodList[selected_indices[0]].AddToDBOrder(selected_indices[0])
    else:
        print("No item selected")

def RemoveFromCart():
    selected_indices = CartListBox.curselection()
    if selected_indices:
        FoodList[selected_indices[0]].RemoveFromCart(selected_indices[0])
        FoodList[selected_indices[0]].RemoveFromDBOrder(selected_indices[0])
        print(selected_indices[0])
    else:
        print("No item selected")



def OpenLoginPage():
    import Login
    Login.UI()
    Login.LoginPage.mainloop()



def PlaceOrder():
    if len(Cart) != 0:
        # import bill
        # bill.UI()
        # bill.BillPage.mainloop()
        print(Cart)
    else:
        CartListBox.config(highlightbackground='red',highlightcolor='red')
        EmptyCartError.grid(column=0,row=3,columnspan=2)
    








def Controller():
    UI()
    GenerateFoods()
    GenerateOrders()
    HomePage.mainloop()
Controller()


