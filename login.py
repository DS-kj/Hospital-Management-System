from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import subprocess

# '''create main window root'''

root = Tk()
root.geometry('700x800+400+0')  # Window dimensions and position
root.resizable(0, 0)  # Window can't be resized
root.iconbitmap("icon.ico")  # Make sure the icon file is available

# Setting up background image
a = Image.open('log1.png')
b = a.resize((700, 800))  # Resize image to fit the window
c = ImageTk.PhotoImage(b)  # Convert to Tkinter compatible format
l = Label(image=c)
l.grid()  # Display background

# Database initialization: create table if it doesn't exist and insert admin user if needed
def initialize_database():
    try:
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()

        # Create the 'user' table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                            user TEXT NOT NULL,
                            pwd TEXT NOT NULL)''')

        # Check if there's already an admin user in the table
        cursor.execute('SELECT * FROM user WHERE user="admin"')
        result = cursor.fetchone()
        
        if result is None:
            # If no admin user, insert the default admin user
            cursor.execute('''INSERT INTO user (user, pwd) VALUES (?, ?)''', ('admin', 'admin123'))
            conn.commit()

        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while initializing the database: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Call the function to initialize the database when the program starts
initialize_database()

# Define the functions for the login page
def add(event):  # If event is not done, bring back the placeholder.
    if user.get() == "":
        user.insert(0, "Enter your Username.")
        user.config(fg="gray")

def sub(event):
    if user.get() == "Enter your Username.":
        user.delete(0, END)  # Clears text
        user.config(fg="black")

def reset():
    root.quit()
    subprocess.Popen(["python", "reset.py"])

def addp(event):  # If event is not done, bring back the placeholder.
    if pwd.get() == "":
        pwd.insert(0, "Enter your Password.")
        pwd.config(fg="gray")

def subp(event):  # If some event is done, remove the placeholder.
    if pwd.get() == "Enter your Password.":
        pwd.delete(0, END)  # Clears text
        pwd.config(fg="black")

def afterlogin():
    subprocess.Popen(["python", "after_login.py"])

# '''create a login frame'''

def check():
    try:
        # Check for admin login first
        if user.get() == "admin" and pwd.get() == "admin123":
            messagebox.showinfo("Admin Login", "Welcome, Admin!")
            # Run admin.py if login is correct
            subprocess.Popen(["python", "admin.py"])
            root.destroy()  # Close the login window
        else:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()

            # Check if the entered username and password match
            cursor.execute('SELECT * FROM user WHERE user=? AND pwd=?', (user.get(), pwd.get()))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo('Success!', f'WELCOME {user.get()}, you have logged in successfully')
                subprocess.Popen(["python", "dashboard.py"])  # Connects the 'python' code named dashboard.py to this page
                root.destroy()  # Destroy the login window
            else:
                messagebox.showerror('OOPS!!', 'Invalid username or password!!!')

            conn.commit()
            conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while interacting with the database: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Frame for login UI
frame = Frame(root, bd=5)
frame.place(x=350, y=200)  # Position the frame

# Labels, Entry fields, and Button
col = '#000000'
Login = Label(frame, text="Sign in", fg=col, font=('Times new roman', 30))
name = Label(frame, text="Username", fg=col, font=('Times new roman', 15))
user = Entry(frame, font=('Times new roman', 15), fg="gray")
user.insert(0, "Enter your Username.")  # initial placeholder
user.bind("<FocusIn>", sub)  # focusin is an event and sub is the function
user.bind("<FocusOut>", add)  # focusout is an event and add is the function

Password = Label(frame, text="Password", fg=col, font=('Times new roman', 15))
pwd = Entry(frame, show='*', font=('Times new roman', 15), fg="gray")
pwd.insert(0, "Enter your Password.")  # initial placeholder
pwd.bind("<FocusIn>", subp)
pwd.bind("<FocusOut>", addp)

submit = Button(frame, text='Login', command=check, fg=col, font=('Times new roman', 15))

btn = Button(frame, text='Reset', command=reset, fg=col, font=('Times new roman', 15), width=8, height=7)

# Display the login interface
Login.grid(row=0, column=0, columnspan=1, pady=20)
btn.grid(row=0, column=0, columnspan=1)
name.grid(row=1, column=0, pady=20)
user.grid(row=1, column=1, pady=20, padx=10)
Password.grid(row=2, column=0, pady=20)
pwd.grid(row=2, column=1, pady=20, padx=10)
submit.grid(row=25, column=1, columnspan=2, pady=20)
btn.grid(row=25, column=0)
btn.config(fg='blue', width=5, height=1)

# Run the window using the mainloop method
root.mainloop()
