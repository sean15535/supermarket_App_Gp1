import sqlite3
from tkinter import ttk, StringVar, Entry
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
from additional_features import MyCombobox  # Importing required functions

BACKGROUND_COLOR = "#f7f7f7"
FORM_BG_COLOR = "#FFFFFF"
BG = "#ffffff"
FG = "#000000"
NAV_COLOR = 'white'
NAV_TEXT_COLOR = '#000000'


def user_mainmenu(main_window, NAV_COLOR, NAV_TEXT_COLOR, builditemtable, make_invoice):
    mainframe = Canvas(main_window, bg=NAV_COLOR, highlightthickness=1)
    mainframe.grid(column=0, row=1, columnspan=1, rowspan=15)
    
    image1 = Image.open("images/items.png")
    resize_image4 = image1.resize((50, 50))
    mi1 = ImageTk.PhotoImage(resize_image4)
    accounts = Button(mainframe, image=mi1, border=0, bg=NAV_COLOR, command=builditemtable)
    accounts.grid(column=0, row=1, padx=16, pady=(20, 0))
    label1 = Label(mainframe, text="Items", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
    label1.grid(column=0, row=2, pady=(5, 10))

    image2 = Image.open("images/invoice.png")
    resize_image2 = image2.resize((50, 50))
    mi2 = ImageTk.PhotoImage(resize_image2)
    sales = Button(mainframe, image=mi2, border=0, bg=NAV_COLOR, command=make_invoice)
    sales.grid(column=0, row=3, pady=(10, 0))
    label2 = Label(mainframe, text="Invoice", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
    label2.grid(column=0, row=4, pady=(5, 10))

    image3 = Image.open("images/change user.png")
    resize_image3 = image3.resize((50, 50))
    mi3 = ImageTk.PhotoImage(resize_image3)
    changeuser = Button(mainframe, image=mi3, border=0, bg=NAV_COLOR)
    changeuser.grid(column=0, row=5, pady=(10, 0))
    label3 = Label(mainframe, text="Sign Out", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
    label3.grid(column=0, row=6, pady=(5, 15))

    image4 = Image.open("images/quit.png")
    resize_image4 = image4.resize((50, 50))
    mi4 = ImageTk.PhotoImage(resize_image4)
    logout = Button(mainframe, image=mi4, border=0, bg=NAV_COLOR)
    logout.grid(column=0, row=7, pady=(10, 0))
    label4 = Label(mainframe, text="Quit", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
    label4.grid(column=0, row=8, pady=(5, 218))

    tableframe1 = Frame(main_window, width=150, height=600, bg="#ffffff")
    tableframe1.place(x=1230, y=180, anchor=NE)
    tableframe = Frame(main_window, width=350, height=700, bg="#ffffff")
    tableframe.place(x=1070, y=230, anchor=NE)
    entryframe = Frame(main_window, width=800, height=350, bg="#ffffff")
    entryframe.place(x=810, y=410)
    entryframe1 = Frame(main_window, width=500, height=350, bg="#ffffff")
    entryframe1.place(x=230, y=410)
    make_invoice()

def active(label1, label2, label3, label4, active_label):
    label1.config(fg='#ffffff')
    label2.config(fg='#ffffff')
    label3.config(fg='#ffffff')
    label4.config(fg='#ffffff')
    active_label.config(fg='#00ffff')

def builditemtable(entryframe, entryframe1, tableframe, tableframeinfo, tableframe1, active_label, label1):
    entryframe.place_forget()
    entryframe1.place_forget()
    tableframe.place(tableframeinfo)
    tableframe1.place_forget()
    active(active_label, label1)
    scrollbarx = Scrollbar(tableframe, orient=HORIZONTAL)
    scrollbary = Scrollbar(tableframe, orient=VERTICAL)
    tree = ttk.Treeview(tableframe, columns=("Product ID", "Product Name", "Description", "Category",
                                             'Price', 'Stocks'), selectmode="extended", height=18,
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=150)
    tree.column('#4', stretch=NO, minwidth=0, width=100)
    tree.column('#5', stretch=NO, minwidth=0, width=100)
    tree.column('#6', stretch=NO, minwidth=0, width=100)
    tree.heading('Product ID', text="Product ID", anchor=W)
    tree.heading('Product Name', text="Product Name", anchor=W)
    tree.heading('Description', text="Description", anchor=W)
    tree.heading('Category', text="Category", anchor=W)
    tree.heading('Price', text="Price", anchor=W)
    tree.heading('Stocks', text="Stocks", anchor=W)
    tree.grid(row=1, column=0, sticky="W")
    scrollbary.config(command=tree.yview)
    scrollbarx.grid(row=2, column=0, sticky="we")
    scrollbarx.config(command=tree.xview)
    scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
    getproducts(tree)


def getproducts(cur, tree):
    cur.execute("select * from products")
    productlist = cur.fetchall()
    for i in productlist:
        tree.insert('', 'end', values=i)


def make_invoice(tableframe, entryframe, entryframeinfo, entryframe1, entryframe1info, tableframe1, tableframe1info, active, label2, tree, clicktranstable, user_input):
    # Hide the tableframe and display the entry frames
    tableframe.place_forget()
    entryframe.place(entryframeinfo)
    entryframe1.place(entryframe1info)
    tableframe1.place(tableframe1info)
    
    # Activate the label2
    active(label2)
    
    # Set up scrollbars
    scrollbarx = Scrollbar(tableframe1, orient=HORIZONTAL)
    scrollbary = Scrollbar(tableframe1, orient=VERTICAL)
    
    # Create the Treeview widget
    tree = ttk.Treeview(tableframe1, columns=("Transaction ID", "Product ID", "Product Name",
                                              'Quantity', 'Price', 'Date', 'Time'),
                        selectmode="browse", height=6,
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    
    # Configure columns and headings
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=140)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=170)
    tree.column('#4', stretch=NO, minwidth=0, width=130)
    tree.column('#5', stretch=NO, minwidth=0, width=130)
    tree.column('#6', stretch=NO, minwidth=0, width=130)
    tree.column('#7', stretch=NO, minwidth=0, width=130)
    tree.heading('Transaction ID', text="Transaction ID", anchor=W)
    tree.heading('Product ID', text="Product ID", anchor=W)
    tree.heading('Product Name', text="Product Name", anchor=W)
    tree.heading('Quantity', text="Quantity", anchor=W)
    tree.heading('Price', text="Price", anchor=W)
    tree.heading('Date', text="Date", anchor=W)
    tree.heading('Time', text="Time", anchor=W)
    
    # Place the treeview widget
    tree.grid(row=1, column=0, sticky="W")
    
    # Configure scrollbars
    scrollbary.config(command=tree.yview)
    scrollbarx.grid(row=2, column=0, sticky="we")
    scrollbarx.config(command=tree.xview)
    scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
    
    # Bind the treeview widget to a function
    tree.bind("<<TreeviewSelect>>", clicktranstable)
    
    # Call user_input function
    user_input()


def user_input(cur, transid, qty, additem, total, entryframe, tableframe1, entryframe1, invoice, cartitemstock):
    cur.execute('select max(trans_id) from sales')
    li = cur.fetchall()
    if li[0][0] is not None:
        transid = li[0][0] + 1
    else:
        transid = 100

    qty = StringVar(value=1)
    additem = StringVar()
    total = IntVar(value=0)

    Button(entryframe, text="Proceed", command=transtableadd, bd=10, width=8, height=7, bg="#FFFFFF",
           font="roboto 10").place(x=0, y=30)
    Button(entryframe, text="Add to cart", command=addtotrans, bd=10, width=10, height=3, bg="#FFFFFF",
           font="roboto 10").place(x=100, y=80)
    Button(entryframe, text="Remove", command=removecart, bd=10, width=10, height=3, bg="#FFFFFF",
           font="roboto 10").place(x=210, y=80)

    entercart = MyCombobox(entryframe, width=20, textvariable=additem, font="roboto 12")
    entercart.place(x=100, y=30, height=30)

    cartqty = Entry(entryframe, textvariable=qty, width=9, bg="#ffffff", font="roboto 12")
    cartqty.place(x=320, y=30, height=30)

    carttotal = Entry(entryframe, textvariable=total, width=20, state='readonly', bg="#ffffff",
                      font="roboto 12")
    carttotal.place(x=130, y=185, height=60)

    Label(entryframe, text="Quantity", font="roboto 12 bold", bg="#ffffff").place(x=318, y=0)
    Label(entryframe, text="Search", font="roboto 12 bold", bg="#ffffff").place(x=100, y=0)
    Label(entryframe, text="Amount Due", font="roboto 14 bold", bg="#ffffff").place(x=0, y=205)

    cur.execute("select max(invoice) from sales")
    invoice = cur.fetchall()
    invoice = invoice[0][0] + 1
    Label(tableframe1, text="Invoice No. " + str(invoice), font="roboto 14 bold", bg="#ffffff").grid(
        row=0, column=0)

    cur.execute("select product_desc,product_price from products")
    li = cur.fetchall()

    inventory = []
    desc_price = dict()

    for i in range(len(li)):
        if inventory.count(li[i][0]) == 0:
            inventory.append(li[i][0])
        desc_price[li[i][0]] = li[i][1]

    entercart.set_completion_list(inventory)

    li = ['Product Id', 'Product Name', 'Price', 'Left Stock']
    va = 0

    for i in range(4):
        Label(entryframe1, text=li[i], font="roboto 14 bold", bg="#FFFFFF").place(x=0, y=va)
        va += 65

    cartitemid = StringVar()
    cartitem = StringVar()
    cartitemprice = StringVar()
    cartitemstock = StringVar()

    Entry(entryframe1, textvariable=cartitemid, font="roboto 14", bg="#FFFFFF", width=25,
          state='readonly').place(x=162, y=0, height=40)
    Entry(entryframe1, textvariable=cartitem, font="roboto 14", bg="#FFFFFF", width=25,
          state='readonly').place(x=162, y=65, height=40)
    Entry(entryframe1, textvariable=cartitemprice, font="roboto 14", bg="#FFFFFF", width=25,
          state='readonly').place(x=162, y=65 * 2, height=40)
    Entry(entryframe1, textvariable=cartitemstock, font="roboto 14", bg="#FFFFFF", width=25,
          state='readonly').place(x=162, y=65 * 3, height=40)

    id_qty = dict()

    cur.execute("select product_id from products")
    list_ = cur.fetchall()

    for i in range(len(list_)):
        id_qty[list_[i][0]] = 0


def add_to_transaction(additem, inventory, qty, desc_price, transid, cartitemid, cartitemprice, cartitem, id_qty, tree, total, cartitemstock):
    if len(additem) == 0 or additem not in inventory:
        messagebox.showerror("Error", "Product Not Found!")
        return
    else:
        if not qty.isdigit():
            messagebox.showerror('Error', 'Invalid quantity!')
            return
        if int(qty) <= 0:
            messagebox.showerror('Error', 'Invalid quantity!')
            return
        
        # Fetch product details from the database
        cur.execute("SELECT product_id, product_desc FROM products WHERE product_desc = ?", (additem,))
        row = cur.fetchall()
        row = [list(row[0])]
        row[0].insert(0, transid)
        transid += 1
        row[0].append(int(qty))
        row[0].append(int(qty) * desc_price[additem])
        x = str(datetime.datetime.now().strftime("%d-%m-%y"))
        row[0].append(x)
        x = datetime.datetime.now()
        x = str(x.hour) + ' : ' + str(x.minute) + ' : ' + str(x.second)
        row[0].append(x)
        row = [tuple(row[0])]
        cartitemid.set(row[0][1])
        cartitemprice.set(desc_price[additem])
        cartitem.set(row[0][2])
        
        # Check available stock
        cur.execute("SELECT stocks FROM products WHERE product_id=?", (row[0][1],))
        li = cur.fetchall()
        if (li[0][0] - id_qty[row[0][1]]) - int(qty) < 0:
            if li[0][0] != 0:
                messagebox.showerror('Error', 'Product with this quantity not available!')
            else:
                messagebox.showerror('Error', 'Product out of stock!')
            return
        
        # Update stock and add item to transaction
        id_qty[row[0][1]] += int(qty)
        cartitemstock.set(li[0][0] - id_qty[row[0][1]])
        for data in row:
            tree.insert('', 'end', values=data)
        total.set(total.get() + (int(qty) * desc_price[additem]))
        qty.set('1')
        additem.set('')



def transtableadd(cur, tree, invoice, id_qty, base, cartitemstock, cartitem, cartitemid, cartitemprice, total, additem, qty):
    x = tree.get_children()
    if len(x) == 0:
        messagebox.showerror('Error', 'Empty cart!')
        return
    if not messagebox.askyesno('Alert!', 'Do you want to proceed?'):
        return
    a = []
    cur.execute("select max(invoice) from sales")
    invoice_number = cur.fetchall()
    invoice_number = invoice_number[0][0] + 1
    
    for i in x:
        list_ = tree.item(i)
        a.append(list_['values'])
        
    for i in a:
        s = (str(i[5])).split('-')
        i[5] = s[2] + "-" + s[1] + "-" + s[0]
        cur.execute("insert into sales values (?,?,?,?,?,?)",
                     (int(i[0]), int(invoice_number), int(i[1]), int(i[3]), i[5], i[6]))
        cur.execute("select stocks from products where product_id=?", (int(i[1]),))
        list_ = cur.fetchall()
        cur.execute("update products set stocks=? where product_id=?",
                     (list_[0][0] - id_qty[str(i[1])], int(i[1])))
        base.commit()
        
    messagebox.showinfo('Success', 'Transaction Successful!')
    tree.delete(*tree.get_children())
    cartitemstock.set('')
    cartitem.set('')
    cartitemid.set('')
    cartitemprice.set('')
    total.set(0)
    additem.set('')
    qty.set('1')
    cur.execute("select product_id from products")
    list_ = cur.fetchall()
    for i in range(0, len(list_)):
        id_qty[list_[i][0]] = 0
    make_invoice()

 
def removecart(tree, cartitemstock, cartitem, cartitemid, cartitemprice, additem, qty, id_qty, total):
    remove = tree.selection()
    if len(remove) == 0:
        messagebox.showerror('Error', 'No cart selected')
        return
    if messagebox.askyesno('Alert!', 'Remove cart?'):
        x = tree.get_children()
        remove = remove[0]
        list_ = []
        fi = []
        for i in x:
            if i != remove:
                list_.append(tuple((tree.item(i))['values']))
            else:
                fi = ((tree.item(i))['values'])
        tree.delete(*tree.get_children())
        for i in list_:
            tree.insert('', 'end', values=i)
        cartitemstock.set('')
        cartitem.set('')
        cartitemid.set('')
        cartitemprice.set('')
        additem.set('')
        qty.set('1')
        id_qty[str(fi[1])] -= fi[3]
        total.set(total.get() - fi[4])

def clicktranstable(tree, cur, cartitemid, cartitem, cur_execute, id_qty, cartitemprice, cartitemstock):
    # Get the currently selected row
    cur_item = tree.item(cur)
    li = cur_item['values']
    
    # Check if a row is selected
    if len(li) == 7:
        # Update the values in the entry fields
        cartitemid.set(li[1])
        cartitem.set(li[2])
        
        # Query the database for product price and stock
        cur_execute("SELECT product_price, stocks FROM products WHERE product_id=?", (li[1],))
        result = cur.fetchall()
        
        # Update the price and stock fields in the GUI
        if result:
            cartitemprice.set(result[0][0])
            cartitemstock.set(result[0][1] - id_qty[cartitemid.get()])


if __name__ == "__main__":
    from tkinter import Tk
    import sqlite3

    # Create Tkinter window
    root = Tk()
    root.title("Supermarket App")

    # Connect to SQLite database
    cur = sqlite3.connect("login.db")
    base = cur.cursor()

 # Call user_mainmenu function with the correct parameters
    user_mainmenu(root, NAV_COLOR, NAV_TEXT_COLOR, builditemtable, make_invoice)

    # Start Tkinter event loop
    root.mainloop()
