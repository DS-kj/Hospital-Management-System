# '''this is a login page'''

from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import sqlite3
import subprocess
# '''create main window root'''

root = Tk()
#(window width x window height + display x cordinate + y cordinate (400 puts it in center) )
root.geometry('700x800+400+0')
#window can't be changed in size (neither width, nor height)
root.resizable(0,0)
root.iconbitmap("icon.ico")
# '''putting background images'''

a=Image.open('log1.png')
#resize
b=a.resize((700,800))
#need to use this to turn img into tkinter usable format
c=ImageTk.PhotoImage(b)
#create label and pack it as background
l=Label(image=c) 
l.grid()

def add(event):#If event is not done bring back the place holder.
    if user.get()=="":
        user.insert(0,"Enter your Username.")
        user.config(fg="gray")
def sub(event):
    if user.get()=="Enter your Username.":
        user.delete(0,END)#Clears text
        user.config(fg="black")
def addd(event):#If event is not done bring back the place holder.
    if user.get()=="":
        user.insert(0,"Enter your old Password.")
        user.config(fg="gray")
def subb(event):
    if user.get()=="Enter your old Password.":
        user.delete(0,END)#Clears text
        user.config(fg="black")
def reset():
    root.quit()
    subprocess.Popen(["python","reset.py"])
def addp(event):#If event is not done bring back the place holder.
    if pwd.get()=="":
        pwd.insert(0,"Enter your new Password.")
        pwd.config(fg="gray")
def subp(event):#If some event is done remove the place holder
    if pwd.get()=="Enter your new Password.":
        pwd.delete(0,END)#Clears text
        pwd.config(fg="black")
def addpp(event):#If event is not done bring back the place holder.
    if pwd.get()=="":
        pwd.insert(0,"Enter your new Password.")
        pwd.config(fg="gray")
def subpp(event):#If some event is done remove the place holder
    if pwd.get()=="Enter your new Password.":
        pwd.delete(0,END)#Clears text
        pwd.config(fg="black")
def afterlogin():
    subprocess.Popen(["python","after_login.py"])
def login():
    if user.get()=='xyz' and pwd.get()=='xyz':
        root.quit()
        afterlogin()
# '''create a login frame'''

#authentication
# def check():
#     # #database
    # conn=sqlite3.connect('python.db')
    # c=conn.cursor()
    # c.execute(
    #     """CREATE TABLE IF NOT EXISTS auth(user text,pwd text)"""
    # )
    # c.execute('SELECT user FROM auth;')
    # nam=c.fetchone()
    # print(nam) #needs work not complete
#frame
frame=Frame(root,bd=5)
#place 75% x and 50% y of display
frame.place(x=350,y=200)
# login
col='#000000'
Login=Label(frame, text="RESET",fg=col,font=('Times new roman',30))
oldn=Label(frame, text="Old password",fg=col,font=('Times new roman',15))
old=Entry(frame,font=('Times new roman',15),fg="gray")
old.insert(0,"Enter your old Password")#initial placeholder
name=Label(frame, text="Username",fg=col,font=('Times new roman',15))
user=Entry(frame,font=('Times new roman',15),fg="gray")
user.insert(0,"Enter your new Username.")#initial placeholder
user.bind("<FocusIn>",sub)#focusin is a event and sub is function
user.bind("<FocusOut>",add)# "   "  "  "
Password=Label(frame, text="Passsword",fg=col,font=('Times new roman',15))
pwd=Entry(frame,font=('Times new roman',15),fg="gray")
pwd.insert(0,"Enter your new Password.")# initial placeholder
pwd.bind("<FocusIn>",subp)
pwd.bind("<FocusOut>",addp)
def change():
    pass
submit=Button(frame,text='CONFIRM',command=change,fg=col,font=('Times new roman',15))
#display login
Login.grid(row=0,column=0,columnspan=1,pady=20)
oldn.grid(row=1,column=0,columnspan=1,pady=20)
old.grid(row=1,column=1,columnspan=1,pady=20)
name.grid(row=2,column=0,pady=20)
user.grid(row=2,column=1,pady=20,padx=5)
Password.grid(row=3,column=0,pady=20)
pwd.grid(row=3,column=1,pady=20,padx=5)
submit.grid(row=25,column=1,columnspan=2,pady=20)




#run the window on screen using mainloop method
root.mainloop()