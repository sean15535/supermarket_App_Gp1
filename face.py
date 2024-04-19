from tkinter import *
import sqlite3
import tkinter.messagebox
import datetime

# Establish database connection
conn = sqlite3.connect("Database\\store.db")
c = conn.cursor()

# date
date = datetime.datetime.now().date()
time_now = datetime.datetime.now().strftime("%H:%M:%S")  # Format the time as HH:MM:SS

# Temporary lists
product_list = []
product_price = []
product_quantity = []
product_id = []

#function for the time
def update_clock():
    now = datetime.datetime.now()
    time_now = now.strftime("%H:%M:%S")
    date_now = now.strftime("%Y-%m-%d")
    datetime_label.config(text="Today's Date: " + date_now + " | Time: " + time_now)
    root.after(1000, update_clock)  # Update every 1000 milliseconds (1 second)

# Function to search for a product
def find_product():
    get_id = enter_id_entry.get()
    query = "SELECT * FROM inventory WHERE id =?"
    result = c.execute(query, (get_id,))
    for r in result:
        get_id = r[0]
        get_name = r[1]
        get_price = r[4]
        get_stock = r[2]
    product_name_label.configure(text="Product Name: " + str(get_name))
    product_price_label.configure(text="Price: N" + str(get_price))
    # Quantity and Label
    quantity_l = Label(left_frame, text='Enter Quantity', font=("arial 18 bold"), bg='steelblue', fg='black')
    quantity_l.place(x=20, y=370)
    quantity_e = Entry(left_frame, width=25, font=("arial 18 bold"), bg='white')
    quantity_e.place(x=250, y=370)
    quantity_e.focus()

    # Add to cart button
    add_to_cart_btn = Button(left_frame, width=25, text='Add To Cart', height=2, bg='orange', command=lambda: add_to_cart(get_name, get_price))
    add_to_cart_btn.place(x=395, y=420)

    # Generate bill and change button
    change_l = Label(left_frame, text='Given Amount', font=("arial 18 bold"), bg='steelblue', fg='black')
    change_l.place(x=20, y=550)
    change_e = Entry(left_frame, width=25, font=("arial 18 bold"), bg='white')
    change_e.place(x=250, y=550)
    change_btn = Button(left_frame, width=25, text='Calculate Change', height=2, bg='orange', command=change_func)
    change_btn.place(x=395, y=600)

    # Generate bill button
    bill_btn = Button(left_frame, width=80, text='Generate Bill', height=2, bg='brown', command=generate_bill)
    bill_btn.place(x=120, y=700)

# Function to add a product to the cart
def add_to_cart(get_name, get_price):
    quantity_value = int(quantity_e.get())
    product_list.append(get_name)
    product_price.append(get_price * quantity_value)
    product_quantity.append(quantity_value)
    # Display added product in the cart
    for i in range(len(product_list)):
        Label(right_frame, text=str(product_list[i]), font=('arial 18 bold'), bg='white', fg='black').place(x=20, y=100 + 40 * i)
        Label(right_frame, text=str(product_quantity[i]), font=('arial 18 bold'), bg='white', fg='black').place(x=310, y=100 + 40 * i)
        Label(right_frame, text=str(product_price[i]), font=('arial 18 bold'), bg='white', fg='black').place(x=470, y=100 + 40 * i)
    total_label.configure(text="Total: N" + str(sum(product_price)))

# Function to calculate change
def change_func():
    amount_given = float(change_e.get())
    our_total = float(sum(product_price))
    to_give = amount_given - our_total
    c_amount = Label(left_frame, text='Change: N' + str(to_give), font=("arial 18 bold"), bg='steelblue', fg='yellow')
    c_amount.place(x=20, y=650)

# Function to generate bill
def generate_bill():
    initial = "SELECT * FROM inventory WHERE id=?"
    for i in range(len(product_list)):
        result = c.execute(initial, (product_id[i],))
        for r in result:
            old_stock = r[2]
        new_stock = int(old_stock) - product_quantity[i]
        sql = "UPDATE inventory SET stock=? WHERE id=?"
        c.execute(sql, (new_stock, product_id[i]))
        conn.commit()

# Initialize the Tkinter window
root = Tk()
root.title("Bokku Supermarket ")
root.geometry('1280x720')

# Left Frame
left_frame = Frame(root, width=900, height=600, bg='steelblue')
left_frame.pack(side=LEFT)

# Right Frame
right_frame = Frame(root, width=700, height=800, bg='white')
right_frame.pack(side=RIGHT)

# App name and date
heading = Label(left_frame, text="Market Square", font=('arial 40 bold'), bg='steelblue', fg='white')
heading.place(x=15, y=0)

datetime_label = Label(right_frame, text="Today's Date: " + str(date) + " | Time: " + time_now, font=('arial 12 bold'), bg='white', fg='steelblue')
datetime_label.place(x=10, y=0)

# Invoice Table
tproduct = Label(right_frame, text="Products", font=('arial 18 bold'), bg='white', fg='black')
tproduct.place(x=10, y=60)
tquantity = Label(right_frame, text="Quantity", font=('arial 18 bold'), bg='white', fg='black')
tquantity.place(x=310, y=60)
tamount = Label(right_frame, text="Amount", font=('arial 18 bold'), bg='white', fg='black')
tamount.place(x=470, y=60)

# Creating product Id label and box
enter_id_label = Label(left_frame, text="Enter Product ID", font=('arial 18 bold'), fg='black', bg='steelblue')
enter_id_label.place(x=20, y=80)
enter_id_entry = Entry(left_frame, width=25, font=('arial 18 bold'), bg='white')
enter_id_entry.place(x=300, y=80)
enter_id_entry.focus()

# Search Button
search_btn = Button(left_frame, width=25, text='Search', height=2, bg='#008B8B', command=find_product)
search_btn.place(x=445, y=120)

# Items to appear once the search button is clicked
product_name_label = Label(left_frame, text="", font=('arial 25 bold'), bg='steelblue', fg='white')
product_name_label.place(x=20, y=250)
product_price_label = Label(left_frame, text="", font=('arial 25 bold'), bg='steelblue', fg='white')
product_price_label.place(x=20, y=290)

# Quantity Entry
quantity_l = Label(left_frame, text='Enter Quantity', font=("arial 18 bold"), bg='steelblue', fg='black')
quantity_l.place(x=20, y=370)
quantity_e = Entry(left_frame, width=25, font=("arial 18 bold"), bg='white')
quantity_e.place(x=250, y=370)

# Total Label
total_label = Label(right_frame, text='', font=('arial 30 bold'), bg='white', fg='black')
total_label.place(x=10, y=600)

update_clock()  # Start the clock update
root.mainloop()
