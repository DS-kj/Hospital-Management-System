from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import sqlite3
from tkinter import ttk
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
    if user.get()=="Enter Username.":
        messagebox.showinfo('ERRORR',"Enter Username")
    if pwd.get()=="Enter Password.":
        messagebox.showinfo('ERRORR',"Enter Password")
    else:
        username = user.get()
        password = pwd.get()
    
        if username and password:
            # Connect to the SQLite database
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()

            # Create a table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL)''')

            # Insert the user data into the table
            cursor.execute('''INSERT INTO user (user, pwd) 
                              VALUES (?, ?)''', (username, password))

            # Commit the transaction and close the connection
            conn.commit()
            conn.close()

            # Show success message
            messagebox.showinfo("Success", f"User {username} created successfully!")
#frame
frame=Frame(root,bd=5)
#place 75% x and 50% y of display
frame.place(x=200,y=40)
# login
col='#000000'
Login=Label(frame, text="Create",fg=col,font=('Times new roman',30))
name=Label(frame, text="Username",fg=col,font=('Times new roman',15))
user=Entry(frame,font=('Times new roman',15),fg="gray")
user.insert(0,"Enter Username.")#initial placeholder
def add(event):#If event is not done bring back the place holder.
    if user.get()=="":
        user.insert(0,"Enter Username.")
        user.config(fg="gray")
def sub(event):
    if user.get()=="Enter Username.":
        user.delete(0,END)#Clears text
        user.config(fg="black")
user.bind("<FocusIn>",sub)#focusin is a event and sub is function
user.bind("<FocusOut>",add)# "   "  "  "
Password=Label(frame, text="Password",fg=col,font=('Times new roman',15))
pwd=Entry(frame,font=('Times new roman',15),fg="gray")
pwd.insert(0,"Enter Password.")#initial placeholder
def add(event):#If event is not done bring back the place holder.
    if pwd.get()=="":
        pwd.insert(0,"Enter Password.")
        pwd.config(fg="gray")
def sub(event):
    if pwd.get()=="Enter Password.":
        pwd.delete(0,END)#Clears text
        pwd.config(fg="black")
pwd.bind("<FocusIn>",sub)#focusin is a event and sub is function
pwd.bind("<FocusOut>",add)# "   "  "  "
submit=Button(frame,text='Create',command=admi,fg=col,font=('Times new roman',15))
def delete_user():
    delete = selected_user.get()  # Get the selected username from the dropdown

    if delete:
        # Connect to the SQLite database
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()

        # Delete the user with the specified username
        cursor.execute('''DELETE FROM user WHERE user = ?''', (delete,))
        conn.commit()

        # Check if the deletion was successful
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", f"User {delete} deleted successfully!")
        else:
            messagebox.showerror("Error", "User not found.")
        conn.close()
        # Update the dropdown list after deletion
        update_dropdown()
    else:
        messagebox.showerror("Error", "Please select a username to delete.")
def update_dropdown():
    # Connect to the SQLite database
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    # Get all usernames from the user table
    cursor.execute('SELECT user FROM user')
    users = cursor.fetchall()
    conn.close()

    # Create a list of usernames
    username_list = [user[0] for user in users]

    # Update the OptionMenu with the new list of usernames
    selected_user.set('')  # Reset the selected value
    dropdown['menu'].delete(0, 'end')  # Clear the existing dropdown options

    for user in username_list:
        dropdown['menu'].add_command(label=user, command=lambda value=user: selected_user.set(value))


# Create a Tkinter variable to store the selected username
selected_user = StringVar()

# Create a simple dropdown menu and populate it with usernames
dropdown = OptionMenu(frame, selected_user, '')
dropdown.place(x=100,y=332)

# Fetch the usernames and update the dropdown
update_dropdown()

# Button to delete the selected user
delete_button = Button(frame, text='Delete User', command=delete_user, fg=col, font=('Times new roman', 15))
delete_button.grid(row=27, column=1, columnspan=2, pady=20)

# Button to delete the selected user
delete_button = Button(frame, text='Delete User', command=delete_user, fg=col, font=('Times new roman', 15))
delete_button.grid(row=27, column=1, columnspan=2, pady=20)
#display login
Login.grid(row=0,column=0,columnspan=1,pady=20)
name.grid(row=1,column=0,pady=20)
user.grid(row=1,column=1,pady=20,padx=10)
Password.grid(row=2,column=0,pady=20)
pwd.grid(row=2,column=1,pady=20,padx=10)
submit.grid(row=25,column=1,columnspan=2,pady=20)

frame2 = Frame(root)
frame2.place(x=150,y=500)

# Function to fetch and display data
def fetch_data():
    # Connect to SQLite database
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Fetch data from the user table (assuming columns are 'user' and 'pwd')
    cursor.execute("SELECT user, pwd FROM user")
    rows = cursor.fetchall()  # Fetch all rows

    # Clear the table before inserting new data
    for item in tree.get_children():
        tree.delete(item)

    # Insert fetched data with serial number (SN)
    for index, row in enumerate(rows, start=1):
        tree.insert("", "end", values=(index, row[0], row[1]))  # SN, username (user), password (pwd)

    # Close the database connection
    conn.close()

# Create a Treeview widget (table)
columns = ("SN", "Username", "Password")
tree = ttk.Treeview(frame2, columns=columns, show="headings")

# Define column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

# Place the Treeview using grid inside frame2
tree.grid(row=0, column=0, padx=10, pady=10)

# Button to refresh and show data
btn_refresh = Button(frame2, text="Refresh Data", command=fetch_data)
btn_refresh.grid(row=1, column=0, pady=10)

# Fetch and display data when the program starts
fetch_data()


root.mainloop()