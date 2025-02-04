# '''this is a login page'''

from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import sqlite3
# '''create main window root'''

root = Tk()
#(window width x window height + display x cordinate + y cordinate (400 puts it in center) )
root.geometry('700x800+400+0')
#window can't be changed in size (neither width, nor height)
root.resizable(0,0)
root.iconbitmap("icon.ico")
# '''putting background images'''

a=Image.open(r'log1.png')
#resize
b=a.resize((700,800))
#need to use this to turn img into tkinter usable format
c=ImageTk.PhotoImage(b)
#create label and pack it as background
l=Label(image=c) 
l.grid()

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
Login=Label(frame, text="LOGIN",fg=col,font=('Times new roman',30))
name=Label(frame, text="Username",fg=col,font=('Times new roman',15))
user=Entry(frame,font=('Times new roman',15),fg="gray")
user.insert(0,"Enter your Username.")#initial placeholder
def add(event):#If event is not done bring back the place holder.
    if user.get()=="":
        user.insert(0,"Enter your Username.")
        user.config(fg="gray")
def sub(event):
    if user.get()=="Enter your Username.":
        user.delete(0,END)#Clears text
        user.config(fg="black")
user.bind("<FocusIn>",sub)
user.bind("<FocusOut>",add)
Password=Label(frame, text="Passsword",fg=col,font=('Times new roman',15))
pwd=Entry(frame,font=('Times new roman',15),fg="gray")
pwd.insert(0,"Enter your Password.")# initial placeholder
def addp(event):#If event is not done bring back the place holder.
    if pwd.get()=="":
        pwd.insert(0,"Enter your Password.")
        pwd.config(fg="gray")
def subp(event):#If some event is done remove the place holder
    if pwd.get()=="Enter your Password.":
        pwd.delete(0,END)#Clears text
        pwd.config(fg="black")
pwd.bind("<FocusIn>",subp)
pwd.bind("<FocusOut>",addp)
# submit=Button(frame,text='LOGIN',command=check,fg=col,font=('Times new roman',15))
#display login
Login.grid(row=0,column=0,columnspan=2,pady=20)
name.grid(row=1,column=0,pady=20)
user.grid(row=1,column=1,pady=20,padx=10)
Password.grid(row=2,column=0,pady=20)
pwd.grid(row=2,column=1,pady=20,padx=10)

# submit.grid(row=25,column=1,columnspan=2,pady=20)




#run the window on screen using mainloop method
root.mainloop()