from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from PIL import Image,ImageTk
import subprocess
# Create the main window
root = Tk()
root.title("Patient's dashboard")
root.geometry("1400x500")
root.resizable(0,0)
root.iconbitmap('icon.ico')

# adding image
a=Image.open('dashy (2).jpg')
#resize
b=a.resize((1400,500))
#need to use this to turn img into tkinter usable format
c=ImageTk.PhotoImage(b)
#create label and pack it as background
l=Label(image=c) 
l.place(relheight=1,relwidth=1)
# Connect to SQLite Database
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL)''')

# Function to add new record to the database
def add_record():
    id=entry_id.get()
    name = entry_name.get()
    phone = entry_phone.get()
    try:
        if (id and name and phone)!='':
            cursor.execute("INSERT INTO patients (id,name, phone) VALUES (?,?, ?)", 
                        (id,name, phone))
            conn.commit()
            messagebox.showinfo("Success", "Patients record added successfully!")
            clear_entries()
            display_records()
        else:
            messagebox.showwarning("Input Error", "Please fill all details!")
    except:
        messagebox.showwarning("Invalid!!","Error has occured")
# Function to update a record in the database
def update_record():
    try:
        record_id = int(entry_id.get())
        name = entry_name.get()
        phone = entry_phone.get()

        if name and phone:
            cursor.execute("UPDATE patients SET name = ?, phone = ? WHERE id = ?",
                           (name, phone, record_id))
            conn.commit()
            messagebox.showinfo("Success", "Patients record updated successfully!")
            clear_entries()
            display_records()
        else:
            messagebox.showwarning("Input Error", "Please fill all details!")
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid ID to update!")

# Function to delete a selected record from the database
def delete_record():
    # Get the selected item from the Treeview
    selected_item = treeview.selection()
    if selected_item:
        record_id = treeview.item(selected_item)["values"][0]  # Get the ID of the selected record
        cursor.execute("DELETE FROM patients WHERE id = ?", (record_id,))
        conn.commit()
        messagebox.showinfo("Success", "Patients record deleted successfully!")
        display_records()
        
    else:
        messagebox.showwarning("Selection Error", "Please select a record to delete!")
# Function for opening appointment
def Appoint():
    #opens doctor dashboard 
    process=subprocess.Popen(['python','appoint.py'])# refernces process to see if window is open
    root.destroy()# hide main dashboard root
    while True:
        status = process.poll()  # Check if the process has terminated
        if status is not None:# check if window closed as when window running it returns none
            subprocess.Popen(['python','patient.py'])# main dashboard
            break
# Function to clear the entry fields
def clear_entries():
    entry_id.delete(0, END)
    entry_name.delete(0, END)
    entry_phone.delete(0, END)

# Function to display all patients records in the Treeview
def display_records():
    # Clear the Treeview before displaying records
    for row in treeview.get_children():
        treeview.delete(row)

    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()

    # Display the records in the Treeview and the end
    for row in rows:
        treeview.insert("", END, values=row)

# Function to handle row selection
def on_select_record(event):
    selected_item = treeview.selection()
    if selected_item:
        record = treeview.item(selected_item)["values"]
        # Populate the entry fields with the selected record
        entry_id.delete(0, END)
        entry_name.delete(0, END)
        entry_phone.delete(0, END)

        entry_id.insert(0, record[0])
        entry_name.insert(0, record[1])
        entry_phone.insert(0, record[2])

#create frame1
frame1=Frame(root)
# Create the form widgets
label_id = Label(frame1, text="Patients ID (for update/and add):")
label_name = Label(frame1, text="Patients Name:")
label_phone = Label(frame1, text="Phone Number:")

entry_id = Entry(frame1)
entry_name = Entry(frame1)
entry_phone = Entry(frame1)

# Create buttons for adding, updating, and deleting records and appointment page
button_add = Button(root, text="Add Record", command=add_record)
button_update = Button(root, text="Update Record", command=update_record)
button_delete = Button(root, text="Delete Record", command=delete_record)
button_appointment=Button(root,text='Manage appointments',command=Appoint)
# Treeview to display records
treeview = ttk.Treeview(root, columns=("ID", "Name", "Phone"), show="headings", height=20)
treeview.heading("ID", text="Patients ID")
treeview.heading("Name", text="Name")
treeview.heading("Phone", text="Phone")

# Add a binding to handle row selection (use <<TreeviewSelect>>)
treeview.bind("<<ButtonRelease-1>>", on_select_record)

#frame placement
frame1.grid()
# Layout management using grid
label_id.grid(row=0, column=1, sticky="e", padx=10, pady=10)
entry_id.grid(row=0, column=2, padx=10, pady=10)

label_name.grid(row=1, column=1, sticky="e", padx=10, pady=10)
entry_name.grid(row=1, column=2, padx=10, pady=10)

label_phone.grid(row=3, column=1, sticky="e", padx=10, pady=10)
entry_phone.grid(row=3, column=2, padx=10, pady=10)

button_add.grid(row=0, column=4, padx=10, pady=10, sticky="w")
button_update.grid(row=2, column=4, padx=10, pady=10, sticky="w")
button_delete.grid(row=4, column=4, padx=10, pady=10, sticky="w")
button_appointment.grid(row=1,column=0,padx=10,pady=10,sticky="w")

treeview.grid(row=0, column=3, rowspan=5, padx=10, pady=10)

# Display records when the app starts
display_records()

# Start the Tkinter event loop
root.mainloop()

# Close the database connection when exiting
conn.close()