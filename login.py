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
def reset():
    root.quit()
    subprocess.Popen(["python","reset.py"])
def addp(event):#If event is not done bring back the place holder.
    if pwd.get()=="":
        pwd.insert(0,"Enter your Password.")
        pwd.config(fg="gray")
def subp(event):#If some event is done remove the place holder
    if pwd.get()=="Enter your Password.":
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

# '''create a login frame'''

#authentication
def check():
    conn = sqlite3.connect('hospital.db')

    # Create a cursor object to interact with the database
    c = conn.cursor()

    # # # Create a table named 'user' with fields 'user' and 'pwd'
    # c.execute('''
    # CREATE TABLE IF NOT EXISTS user (
    #     user TEXT NOT NULL,
    #     pwd TEXT NOT NULL
    # );
    # ''')

    # # Insert a record into the 'user' table
    # c.execute('''
    # INSERT INTO user (user, pwd) VALUES (?, ?);
    # ''', ('receptionist', 'ilovehospital'))

    #get user name and check if it is valid
    c.execute('SELECT *, oid FROM user')
    result=c.fetchall()
    for i in result:
        manche=i[0]
        chabi=i[1]
    if manche==user.get() and chabi==pwd.get():
        messagebox.showinfo('Sucess!!!!',f'WELCOME {user.get()},you have logged in sucessfully')
        subprocess.Popen(["python","dashbaord.py"])

        root.destroy()
    else:
        messagebox.showerror('OOPS!!','Invalid username or password!!!')
    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
#frame
frame=Frame(root,bd=5)
#place 75% x and 50% y of display
frame.place(x=350,y=200)
# login
col='#000000'
Login=Label(frame, text="Sign in",fg=col,font=('Times new roman',30))
name=Label(frame, text="Username",fg=col,font=('Times new roman',15))
user=Entry(frame,font=('Times new roman',15),fg="gray")
user.insert(0,"Enter your Username.")#initial placeholder
user.bind("<FocusIn>",sub)#focusin is a event and sub is function
user.bind("<FocusOut>",add)# "   "  "  "
Password=Label(frame, text="Passsword",fg=col,font=('Times new roman',15))
pwd=Entry(frame,show='*',font=('Times new roman',15),fg="gray")
pwd.insert(0,"Enter your Password.")# initial placeholder
pwd.bind("<FocusIn>",subp)
pwd.bind("<FocusOut>",addp)

submit=Button(frame,text='Login',command=check,fg=col,font=('Times new roman',15))

btn=Button(frame,text='Reset',command=reset,fg=col,font=('Times new roman',15),width=8,height=7)
#display login
Login.grid(row=0,column=0,columnspan=1,pady=20)
btn.grid(row=0,column=0,columnspan=1)
name.grid(row=1,column=0,pady=20)
user.grid(row=1,column=1,pady=20,padx=10)
Password.grid(row=2,column=0,pady=20)
pwd.grid(row=2,column=1,pady=20,padx=10)
submit.grid(row=25,column=1,columnspan=2,pady=20)
btn.grid(row=25,column=0)
btn.config(fg='blue',width=5,height=1)



#run the window on screen using mainloop method
root.mainloop()