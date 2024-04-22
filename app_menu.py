import sqlite3
from tkinter import ttk, Canvas, Button, Label, NE, Scrollbar, Frame, messagebox, StringVar, Entry
from PIL import Image, ImageTk
import datetime
from additional_features import set_completion_list, autocomplete, handle_keyrelease

# USER MENU
BACKGROUND_COLOR = "#f7f7f7"
FORM_BG_COLOR = "#FFFFFF"
NAV_COLOR = '#1b1a1a'
NAV_TEXT_COLOR = '#ffffff'

# Helper functions
def makeprint():
    pass

class MyCombobox(Entry):
    def __init__(self, master, width, **kw):
        self.var = kw.pop("textvariable", StringVar())
        Entry.__init__(self, master, width=width, textvariable=self.var, **kw)
        self.lb = Listbox(width=width)
        self.lb.place(x=100, y=60, height=100)
        self.lb.bind("<Double-Button-1>", self.selection)
        self.lb.bind("<Right>", self.selection)
        self.lb.bind("<Left>", self.selection)
        self.lb.bind("<Up>", self.selection)
        self.lb.bind("<Down>", self.selection)
        self.lb.bind("<Return>", self.selection)
        self.lb.bind("<Button-1>", self.selection)
        self.var.trace("w", self.autocomplete)

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)

    def selection(self, event):
        if self.lb.curselection() != ():
            index = self.lb.curselection()[0]
            value = self.lb.get(index)
            self.var.set(value)
            self.lb.place_forget()

    def autocomplete(self, *args):
        if self.var.get() == "":
            self.lb.place_forget()
            return
        s = self.var.get().lower()
        self.lb.delete(0, END)
        for item in self._completion_list:
            if s in item.lower():
                self.lb.insert(END, item)
        self.lb.place(x=100, y=60, height=100)

def clicktranstable(event):
    selection = event.widget.selection()[0]
    selected_item = event.widget.item(selection, 'values')
    cartitemid.set(selected_item[1])
    cartitemprice.set(selected_item[4])
    cartitem.set(selected_item[2])
    cartitemstock.set(selected_item[3])
    return selected_item

def removecart(tree, total):
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
                fi = (tree.item(i))['values']
        total.set(total.get() - fi[4])
        cartitemid.set('')
        cartitem.set('')
        cartitemprice.set('')
        cartitemstock.set('')
        tree.delete(*tree.get_children())
        for i in list_:
            tree.insert('', 'end', values=i)

def transtableadd(tree, transid, total):
    x = tree.get_children()
    if len(x) == 0:
        messagebox.showerror('Error', 'Empty cart!')
        return
    if not messagebox.askyesno('Alert!', 'Do you want to proceed?'):
        return
    a = []
    cur.execute("select max(invoice) from sales")
    invoice = cur.fetchall()
    invoice = invoice[0][0] + 1
    for i in x:
        list_ = tree.item(i)
        a.append(list_['values'])
    for i in a:
        s = (str(i[5])).split('-')
        i[5] = s[2] + "-" + s[1] + "-" + s[0]
        cur.execute("insert into sales values (?,?,?,?,?,?)",
                     (int(i[0]), int(invoice), int(i[1]), int(i[3]), i[5], i[6]))
        cur.execute("select stocks from products where product_id=?", (int(i[1]),))
        list_ = cur.fetchall()
        cur.execute("update products set stocks=? where product_id=?",
                     (list_[0][0] - id_qty[str(i[1])], int(i[1])))
        base.commit()
    messagebox.showinfo('Success', 'Transaction Successful!')
    makeprint()
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

def addtotrans(tree, additem, qty, total):
    if len(additem.get()) == 0 or additem.get() not in inventory:
        messagebox.showerror("Error", "Product Not Found!")
        return
    else:
        if not qty.get().isdigit():
            messagebox.showerror('Error', 'Invalid quantity!')
            return
        if int(qty.get()) <= 0:
            messagebox.showerror('Error', 'Invalid quantity!')
            return
        cur.execute("select product_id,product_desc from products where product_desc = ? ",
                    (additem.get(),))
        row = cur.fetchall()
        row = [list(row[0])]
        row[0].insert(0, transid)
        row[0].append(int(qty.get()))
        row[0].append((int(qty.get()) * desc_price[additem.get()]))
        x = str(datetime.datetime.now().strftime("%d-%m-%y"))
        row[0].append(x)
        x = datetime.datetime.now()
        x = str(x.hour) + ' : ' + str(x.minute) + ' : ' + str(x.second)
        row[0].append(x)
        row = [tuple(row[0])]
        cartitemid.set(row[0][1])
        cartitemprice.set(desc_price[additem.get()])
        cartitem.set(row[0][2])
        cur.execute("select stocks from products where product_id=?", (row[0][1],))
        li = cur.fetchall()
        if (li[0][0] - id_qty[row[0][1]]) - int(qty.get()) < 0:
            if li[0][0] != 0:
                messagebox.showerror('Error', 'Product with this quantity not available!')
            else:
                messagebox.showerror('Error', 'Product out of stock!')
            return
        id_qty[row[0][1]] += int(qty.get())
        cartitemstock.set(li[0][0] - id_qty[row[0][1]])
        for data in row:
            tree.insert('', 'end', values=data)
        total.set(total.get() + (int(qty.get()) * desc_price[additem.get()]))
        qty.set('1')
        additem.set('')

def getproducts(tree):
    cur.execute("select * from products")
    productlist = cur.fetchall()
    for i in productlist:
        tree.insert('', 'end', values=i)

def builditemtable(entryframe, entryframe1, tableframe, tableframeinfo, tableframe1, label1):
    entryframe.place_forget()
    entryframe1.place_forget()
    tableframe.place(tableframeinfo)
    tableframe1.place_forget()
    active(label1)
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

def make_invoice(tableframe, entryframe, entryframeinfo, entryframe1, entryframe1info, tableframe1, tableframe1info, label2):
    tableframe.place_forget()
    entryframe.place(entryframeinfo)
    entryframe1.place(entryframe1info)
    tableframe1.place(tableframe1info)
    active(label2)
    scrollbarx = Scrollbar(tableframe1, orient=HORIZONTAL)
    scrollbary = Scrollbar(tableframe1, orient=VERTICAL)
    tree = ttk.Treeview(tableframe1, columns=("Transaction ID", "Product ID", "Product Name",
                                               'Quantity', 'Price', 'Date', 'Time'), selectmode="browse",
                        height=6,
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
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
    tree.grid(row=1, column=0, sticky="W")
    scrollbary.config(command=tree.yview)
    scrollbarx.grid(row=2, column=0, sticky="we")
    scrollbarx.config(command=tree.xview)
    scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
    tree.bind("<<TreeviewSelect>>", clicktranstable)
    user_input(tree)

def active(label1=None, label2=None, label3=None, label4=None, label=None):
    if label1:
        label1.config(fg='#ffffff')
    if label2:
        label2.config(fg="#ffffff")
    if label3:
        label3.config(fg="#ffffff")
    if label4:
        label4.config(fg="#ffffff")
    if label:
        label.config(fg='#00ffff')

def user_input(tree):
    cur.execute('select max(trans_id) from sales')
    li = cur.fetchall()
    if li[0][0] is not None:
        transid = li[0][0] + 1
    else:
        transid = 100
    qty = StringVar(value=1)
    additem = StringVar()
    total = IntVar(value=0)
    Button(entryframe, text="Proceed", command=lambda: transtableadd(tree, transid, total), bd=10, width=8, height=7,
           bg="#FFFFFF",
           font="roboto 10").place(x=0, y=30)
    Button(entryframe, text="Add to cart", command=lambda: addtotrans(tree, additem, qty, total), bd=10, width=10,
           height=3, bg="#FFFFFF",
           font="roboto 10").place(x=100, y=80)
    Button(entryframe, text="Remove", command=lambda: removecart(tree, total), bd=10, width=10, height=3, bg="#FFFFFF",
           font="roboto 10").place(x=210, y=80)
    entercart = MyCombobox(entryframe, width=20, textvariable=additem, font="roboto 12")
    entercart.place(x=100, y=30, height=30)
    cartqty = Entry(entryframe, textvariable=qty, width=9, bg="#ffffff", font="roboto 12")
    cartqty.place(x=320, y=30, height=30)
    carttotal = Entry(entryframe, textvariable=total, width=20, state='readonly', bg="#ffffff",
                      font="roboto 12")
    carttotal.place(x=130, y=185, height=60)
    Label(entryframe, text="Quantity", font="roboto 12 bold", bg="#ffffff").place(x=318, y=0)
    Label(entryframe, text="Search", font="roboto 12 bold", bg="#ffffff").place(x=0, y=0)
    Label(entryframe, text="Total", font="roboto 12 bold", bg="#ffffff").place(x=0, y=185)
    Label(entryframe, text="Rs.", font="roboto 12 bold", bg="#ffffff").place(x=100, y=185)
    Label(entryframe, text="No.", font="roboto 12 bold", bg="#ffffff").place(x=300, y=185)
    tree.grid(row=1, column=0, sticky="W")

def makeprint():
    pass

# Main function
if __name__ == '__main__':
    base = sqlite3.connect('inventory.db')
    cur = base.cursor()
    root = Tk()
    root.title('Inventory System')
    root.geometry('850x500')
    root.configure(bg=BACKGROUND_COLOR)
    root.resizable(False, False)

    id_qty = {}
    desc_price = {}
    cur.execute("select product_id, stocks, product_desc, price from products")
    inventory = cur.fetchall()
    for i in inventory:
        id_qty[i[0]] = 0
        desc_price[i[2]] = i[3]

    base = sqlite3.connect('sales.db')
    cur = base.cursor()
    cur.execute('''create table if not exists sales (
                trans_id int primary key,
                invoice int,
                product_id int,
                quantity int,
                date text,
                time text)
                ''')

    entryframe = Frame(root, bg=BACKGROUND_COLOR)
    entryframeinfo = {'x': 200, 'y': 20, 'width': 640, 'height': 200}
    entryframe.place(entryframeinfo)

    entryframe1 = Frame(root, bg=BACKGROUND_COLOR)
    entryframe1info = {'x': 200, 'y': 240, 'width': 640, 'height': 220}

    tableframe = Frame(root, bg=BACKGROUND_COLOR)
    tableframeinfo = {'x': 200, 'y': 20, 'width': 640, 'height': 450}

    tableframe1 = Frame(root, bg=BACKGROUND_COLOR)
    tableframe1info = {'x': 200, 'y': 20, 'width': 640, 'height': 450}

    label1 = Label(root, text="Inventory", font="roboto 20 bold", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
    label1.place(x=0, y=100, width=200, height=50)

    label2 = Label(root, text="Transaction", font="roboto 20 bold", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
    label2.place(x=0, y=200, width=200, height=50)

    builditemtable(entryframe, entryframe1, tableframe, tableframeinfo, tableframe1, label1)

    menubutton = Button(root, text="Make Invoice", bg=NAV_COLOR, fg=NAV_TEXT_COLOR, font="roboto 10 bold",
                        command=lambda: make_invoice(tableframe, entryframe, entryframeinfo, entryframe1,
                                                     entryframe1info, tableframe1, tableframe1info, label2))
    menubutton.place(x=0, y=300, width=200, height=50)
    menubutton.bind("<Enter>", lambda e: menubutton.config(bg=NAV_TEXT_COLOR, fg=NAV_COLOR))
    menubutton.bind("<Leave>", lambda e: menubutton.config(bg=NAV_COLOR, fg=NAV_TEXT_COLOR))

    Button(root, text="Make Print", bg=NAV_COLOR, fg=NAV_TEXT_COLOR, font="roboto 10 bold", command=makeprint).place(
        x=0, y=400, width=200, height=50)

    root.mainloop()
