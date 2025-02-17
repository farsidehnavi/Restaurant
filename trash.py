# import pymongo
# from tkinter import *
# from tkinter.font import Font



# client = pymongo.MongoClient('mongodb://localhost:27017/')
# DB = client['ByPy']
# # DB.create_collection('Restaurant')
# DB = DB.Restaurant



# def UI():

#     global AdminPage
#     AdminPage = Tk(className='admin')

    
#     PageFont = Font(AdminPage,family='Playwrite GB S ExtraLight',size=11)

#     Label(AdminPage,text='Admin !',font=PageFont).grid(column=0,row=0,columnspan=2)

#     StockList = Listbox(AdminPage,font=PageFont)
#     StockList.grid(column=0,row=1,rowspan=4)

#     global NameEntry
#     global PriceEntry

#     Label(AdminPage,text='name',font=PageFont).grid(column=1,row=1)

#     NameEntry = Entry(AdminPage,font=PageFont)
#     NameEntry.grid(column=1,row=2)

#     Label(AdminPage,text='price',font=PageFont).grid(column=1,row=3)
    
#     PriceEntry = Entry(AdminPage,font=PageFont)
#     PriceEntry.grid(column=1,row=4)


#     Button(AdminPage,font=PageFont,text='Remove').grid(column=0,row=5,sticky='ew')

#     Button(AdminPage,font=PageFont,text='Add').grid(column=1,row=5,sticky='ew')


#     Button(AdminPage,text='Back to main',font=PageFont,command=AdminPage.destroy).grid(column=0,row=6,columnspan=2,sticky='ew')


#     AdminPage.mainloop()

# UI()
