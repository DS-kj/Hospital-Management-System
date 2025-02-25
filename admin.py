from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import subprocess

# '''create main window root'''

root = Tk()
root.geometry('900x800+400+0')
root.resizable(0,0)
root.iconbitmap("icon.ico")

# '''putting background images'''

a=Image.open('appointment.jpg')
b=a.resize((1100,800))
c=ImageTk.PhotoImage(b)
l=Label(image=c) 
l.grid()

#authentication
def admi():
    if user.get()=="Enter Username." and pwd.get()=="Enter Password.":
        messagebox.showwarning('ERROR',"Enter Username and Password")
    elif user.get()=="Enter Username."or user.get()=="" and pwd.get()==pwd.get():
        messagebox.showwarning('ERRORR',"Enter Username")
    elif user.get()==user.get() and pwd.get()=='Enter Password.' or pwd.get()=="":
        messagebox.showwarning('ERRORR',"Enter Password")
    else:
        username = user.get()
        password = pwd.get()
        if username and password:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL)''')
            cursor.execute('''INSERT INTO user (username, password) 
                              VALUES (?, ?)''', (username, password))
            fetch_data()
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"User {username} created successfully!")

frame=Frame(root)
frame.place(x=20,y=140)
col='#000000'
Login=Label(frame, text="Create",fg=col,font=('Times new roman',30))
name=Label(frame, text="Username",fg=col,font=('Times new roman',15))
user=Entry(frame,font=('Times new roman',15),fg="gray")
user.insert(0,"Enter Username.")

def add(event):
    if user.get()=="":
        user.insert(0,"Enter Username.")
        user.config(fg="gray")

def sub(event):
    if user.get()=="Enter Username.":
        user.delete(0,END)
        user.config(fg="black")

user.bind("<FocusIn>",sub)
user.bind("<FocusOut>",add)
Password=Label(frame, text="Password",fg=col,font=('Times new roman',15))
pwd=Entry(frame,font=('Times new roman',15),fg="gray")
pwd.insert(0,"Enter Password.")

def add(event):
    if pwd.get()=="":
        pwd.insert(0,"Enter Password.")
        pwd.config(fg="gray")

def sub(event):
    if pwd.get()=="Enter Password.":
        pwd.delete(0,END)
        pwd.config(fg="black")

pwd.bind("<FocusIn>",sub)
pwd.bind("<FocusOut>",add)
submit=Button(frame,text='Create',command=admi,fg=col,font=('Times new roman',15))

Login.grid(row=0,column=0,columnspan=1,pady=20)
name.grid(row=1,column=0,pady=20)
user.grid(row=1,column=1,pady=20,padx=10)
Password.grid(row=2,column=0,pady=20)
pwd.grid(row=2,column=1,pady=20,padx=10)
submit.grid(row=25,column=1,columnspan=2,pady=20)

frame2 = Frame(root,bg='#beeffe')
frame2.place(x=420,y=117)
lab_f2=Label(frame2,text="User",fg=col,bg='#beeffe',font=('Times new roman',30))
lab_f2.grid(row=0,column=0,columnspan=1,pady=20,padx=0)

def fetch_data():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user FROM user")
    rows = cursor.fetchall()
    for item in tree.get_children():
        tree.delete(item)
    for index, row in enumerate(rows, start=1):
        tree.insert("", "end", values=(index, row[0]))
    conn.close()

columns = ("SN", "Username")
tree = ttk.Treeview(frame2, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.grid(row=1, column=0, padx=10, pady=10)

btn_refresh = Button(frame2, text="Refresh Data", command=fetch_data)
btn_refresh.grid(row=2, column=0, pady=10)

fetch_data()

def delete_user():
    selected=tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a user to delete.")
        return
    user= tree.item(selected, 'values')[1]
    conn= sqlite3.connect('hospital.db')
    cursor= conn.cursor()
    cursor.execute("DELETE FROM user WHERE user=?", (user,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"User {user} deleted successfully!")
    fetch_data()

btn_delete = Button(frame2, text="Delete User", command=delete_user, bg="red", fg="white")
btn_delete.grid(row=2, column=0, pady=10, padx=5,sticky='e')

root.mainloop()
