from tkinter import *
import sqlite3
import tkinter.messagebox
import datetime

# Establish database connection
conn = sqlite3.connect("Database\\store.db")
c = conn.cursor()

# Date
date = datetime.datetime.now().date()
time_now = datetime.datetime.now().strftime("%H:%M:%S")  # Format the time as HH:MM:SS

# Temporary lists
product_list = []
product_price = []
product_quantity = []
product_id = []

# Function for the time
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
    quantity_l = Label(left_frame, text='Enter Quantity', font=("arial 14 bold"), bg='#6A24FF', fg='black')
    quantity_l.place(x=20, y=300)
    quantity_e = Entry(left_frame, width=20, font=("arial 14 bold"), bg='white', bd='7')
    quantity_e.place(x=180, y=300)
    quantity_e.focus()

    # Add to cart button
    add_to_cart_btn = Button(left_frame, width=10, text='Add To Cart', height=2, bg='lime', command=lambda: add_to_cart(get_name, get_price))
    add_to_cart_btn.place(x=420, y=300)

    # Generate bill and change button
    change_l = Label(left_frame, text='Given Amount', font=("arial 14 bold"), bg='#6A24FF', fg='black')
    change_l.place(x=20, y=370)
    change_e = Entry(left_frame, width=20, font=("arial 14 bold"), bg='white', bd='7')
    change_e.place(x=180, y=370)
    change_btn = Button(left_frame, width=15, text='Calculate Change', height=2, bg='orange', command=change_func)
    change_btn.place(x=400, y=415)

    # Generate bill button
    bill_btn = Button(left_frame, width=40, text='Generate Bill', height=2, bg='brown', command=generate_bill)
    bill_btn.place(x=120, y=500)

# Function to add a product to the cart
def add_to_cart(get_name, get_price):
    quantity_value = int(quantity_e.get())
    product_list.append(get_name)
    product_price.append(get_price * quantity_value)
    product_quantity.append(quantity_value)
    
    # Display added product in the cart
    for i in range(len(product_list)):
        Label(right_frame, text=str(product_list[i]), font=('arial 14 bold'), bg='white', fg='black').place(x=10, y=100 + 30 * i)
        Label(right_frame, text=str(product_quantity[i]), font=('arial 14 bold'), bg='white', fg='black').place(x=200, y=100 + 30 * i)
        Label(right_frame, text=str(product_price[i]), font=('arial 14 bold'), bg='white', fg='black').place(x=350, y=100 + 30 * i)
    total_label.configure(text="Total: N" + str(sum(product_price)))

# Function to calculate change
def change_func():
    amount_given = float(change_e.get())
    our_total = float(sum(product_price))
    to_give = amount_given - our_total
    c_amount = Label(left_frame, text='Change: N' + str(to_give), font=("arial 14 bold"), bg='#6A24FF', fg='yellow')
    c_amount.place(x=20, y=470)

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

# Create the main frame
main_frame = Frame(root, bg='white')
main_frame.pack(fill=Y, expand=True)  # Adjusted packing

# Create the title label with custom border color
title_label = Label(main_frame, text="Supermarket POS", bd=12, bg='#6A24FF', fg='white', font=('times new roman', 25, 'bold'), relief=GROOVE, justify=CENTER, highlightcolor="white")
title_label.pack(fill=X)

# Left Frame
left_frame = Frame(main_frame, width=600, height=700, bg='#6A24FF')
left_frame.pack(side=LEFT)

# Right Frame
right_frame = Frame(main_frame, width=700, height=800, bg='white')
right_frame.pack(side=RIGHT)

datetime_label = Label(right_frame, text="Today's Date: " + str(date) + " | Time: " + time_now, font=('arial 12 bold'), bg='white', fg='#6A24FF')
datetime_label.place(x=10, y=0)

# line partition
tproduct = Label(right_frame, text="_____________________________________________________________", font=('arial 14 bold'), bg='white', fg='black')
tproduct.place(x=10, y=30)

# Invoice Table
tproduct = Label(right_frame, text="Products", font=('arial 14 bold'), bg='white', fg='black')
tproduct.place(x=10, y=60)
tquantity = Label(right_frame, text="Quantity", font=('arial 14 bold'), bg='white', fg='black')
tquantity.place(x=300, y=60)
tamount = Label(right_frame, text="Amount", font=('arial 14 bold'), bg='white', fg='black')
tamount.place(x=550, y=60)

# line partition
tproduct = Label(right_frame, text="_____________________________________________________________", font=('arial 14 bold'), bg='white', fg='black')
tproduct.place(x=10, y=85)

# Creating product Id label and box
enter_id_label = Label(left_frame, text="Enter Product ID", font=('arial 14 bold'), fg='black', bg='#6A24FF')
enter_id_label.place(x=20, y=20)
enter_id_entry = Entry(left_frame, width=20, font=('arial 14 bold'), bg='white', bd=7)
enter_id_entry.place(x=180, y=20)
enter_id_entry.focus()

# Search Button
search_btn = Button(left_frame, width=10, text='Search', height=2, bg='lime', command=find_product)
search_btn.place(x=420, y=20)

# Items to appear once the search button is clicked
product_name_label = Label(left_frame, text="", font=('arial 14 bold'), bg='#6A24FF', fg='white')
product_name_label.place(x=20, y=200)
product_price_label = Label(left_frame, text="", font=('arial 14 bold'), bg='#6A24FF', fg='white')
product_price_label.place(x=20, y=230)


# Total Label
total_label = Label(right_frame, text='', font=('arial 20 bold'), bg='white', fg='black')
total_label.place(x=10, y=550)

update_clock()  # Start the clock update
root.mainloop()
