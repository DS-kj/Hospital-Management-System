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
#authentication
def admi():
    username = user.get()
    password = pwd.get()
    
    if username and password:
        # Connect to the SQLite database
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()

        # Create a table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL)''')

        # Insert the user data into the table
        cursor.execute('''INSERT INTO users (username, password) 
                          VALUES (?, ?)''', (username, password))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        # Show success message
        messagebox.showinfo("Success", f"User {username} created successfully!")
#frame
frame=Frame(root,bd=5)
#place 75% x and 50% y of display
frame.place(x=350,y=200)
# login
col='#000000'
Login=Label(frame, text="Create",fg=col,font=('Times new roman',30))
name=Label(frame, text="Username",fg=col,font=('Times new roman',15))
user=Entry(frame,font=('Times new roman',15),fg="Black")
Password=Label(frame, text="Passsword",fg=col,font=('Times new roman',15))
pwd=Entry(frame,font=('Times new roman',15),fg="Black")
submit=Button(frame,text='Create',command=admi,fg=col,font=('Times new roman',15))

#display login
Login.grid(row=0,column=0,columnspan=1,pady=20)
name.grid(row=1,column=0,pady=20)
user.grid(row=1,column=1,pady=20,padx=10)
Password.grid(row=2,column=0,pady=20)
pwd.grid(row=2,column=1,pady=20,padx=10)
submit.grid(row=25,column=1,columnspan=2,pady=20)


#run the window on screen using mainloop method
root.mainloop()