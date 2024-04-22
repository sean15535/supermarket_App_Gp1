import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

def login_window():
    loginw = Tk()
    loginw.title("Login")
    width = 450
    height = 600
    screen_width = loginw.winfo_screenwidth()
    screen_height = loginw.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    loginw.geometry("%dx%d+%d+%d" % (width, height, x, y))
    loginw.resizable(0, 0)
    loginw.protocol('WM_DELETE_WINDOW', login_del)
    loginw.config(bg="#4267b2")

    image = Image.open("images/purple-gradient.png")
    resize_image = image.resize((450, 600))
    img = ImageTk.PhotoImage(resize_image)

    bgimage = Label(
        loginw,
        image=img
    )
    bgimage.place(x=-2, y=-2)

    logintable()
    username = StringVar(value="Username")
    password = StringVar(value="Password")
    obj(loginw, username, password)

    loginw.mainloop()

def login_del():
    if messagebox.askyesno("Quit", " Leave application?"):
        exit(0)

def logintable():
    base = sqlite3.connect("login.db")
    cur = base.cursor()
    cur.execute(
        "CREATE TABLE if not exists users (name varchar (20), phone_no number, gender varchar(10), username varchar (20),password varchar (20) NOT NULL,account_type varchar ( 10 ) NOT NULL,PRIMARY KEY(username));")
    base.commit()
    base.close()

def obj(loginw, username, password):
    loginframe = Canvas(loginw, bg="#f2f2f2", height=400, width=300, highlightthickness=2)
    loginw.bind('<Return>', lambda event: checkuser(event, loginw, username, password))
    loginframe.place(x=85, y=95)
    toplabel = Label(loginframe, fg="black", bg="#f2f2f2", anchor="center", text="Login",
                     font="Montserrat 30 normal")
    toplabel.place(x=95, y=30)
    us = Entry(loginframe, width=20, bg="#ffffff", textvariable=username, border=0, justify='center',
               font="Roboto 14 ")
    us.place(x=35, y=145, height=40)
    pa = Entry(loginframe, width=20, bg="#ffffff", textvariable=password, border=0, justify='center',
               font="Roboto 14 ")
    pa.place(x=35, y=190, height=40)
    us.bind('<Button-1>', lambda event: onclick(event, us, "Username", "Choose your username"))
    pa.bind('<Button-1>', lambda event: onclick(event, pa, "Password", "Create a password"))
    signin = Button(loginframe, width=20, text="Sign in", bg="#9933ff", fg="white",
                    command=lambda: checkuser(0, loginw, username, password),
                    font="Roboto 14")
    signin.place(x=35, y=290)

def checkuser(event, loginw, username, password):
    s = username.get().upper()
    s1 = password.get().upper()
    base = sqlite3.connect("login.db")
    cur = base.cursor()
    cur.execute("select * from users where username=? and password=? ", (s, s1))
    list_ = cur.fetchall()
    base.close()
    if len(list_) > 0:
        success(loginw)
    else:
        fail()

def success(loginw):
    loginw.quit()

def fail():
    messagebox.showerror("Error", "The username or password is incorrect")

def onclick(event, widget, default_text, placeholder_text):
    if widget.get() == default_text or widget.get() == placeholder_text:
        widget.delete(0, "end")

if __name__ == "__main__":
    login_window()
