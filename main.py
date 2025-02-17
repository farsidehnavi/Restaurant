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
    
    Button(HomePage,text='Developer Button',command=DevButton).grid(column=0,row=6,sticky='ew')
    
    Button(HomePage,text='Developer Button2',command=DevButton2).grid(column=1,row=6,sticky='ew')



FOODS = [i for i in DBAdmin.find()]
ORDERS = [i[''] for i in DBOrder.find()]
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

    def AddToDBOrder(self):
        DBOrder.insert_one({'':self})

    def RemoveFromCart(self,ID):
        global Cart
        for i in range(len(Cart)):
            if Cart[i] == self:
                del Cart[i]
                break
        CartListBox.delete(ID)

    def RemoveFromDBOrder(self):
        DBOrder.delete_one({'':self})








def GenerateFoods():
    global Stock
    for i in FOODS:
        Stock.append(Food(i['Name'],i['Cost']))
    for i in Stock:
        i.AddToStockListBox()


def GenerateOrders():
    global Cart
    for i in ORDERS:
        Stock[i].AddToCart(i)







def AddToCart():
    selected_indices = StockListBox.curselection()
    if selected_indices:
        Stock[selected_indices[0]].AddToCart()
        # Stock[selected_indices[0]].AddToDBOrder(selected_indices[0])
    else:
        print("No item selected")

def RemoveFromCart():
    selected_indices = CartListBox.curselection()
    if selected_indices:
        Cart[selected_indices[0]].RemoveFromCart(selected_indices[0])
        # Stock[selected_indices[0]].RemoveFromDBOrder(selected_indices[0])
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
    


def DevButton():
    
    Cart[5].RemoveFromCart(5)
    

def DevButton2():
    
    print(Cart)





def Controller():
    UI()
    GenerateFoods()
    GenerateOrders()
    HomePage.mainloop()
Controller()












