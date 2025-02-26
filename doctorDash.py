from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk

# Create the main window
root = Tk()
root.title("Doctor's dashboard")
root.geometry("1400x500")
root.iconbitmap('icon.ico')
root.resizable(0, 0)

# adding image
a = Image.open('dashy (2).jpg')
# resize
b = a.resize((1400, 500))
# need to use this to turn img into tkinter usable format
c = ImageTk.PhotoImage(b)
# create label and pack it as background
l = Label(image=c)
l.place(relheight=1, relwidth=1)

# Connect to SQLite Database
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    specialty TEXT NOT NULL,
                    phone TEXT NOT NULL)''')

# Function to add new record to the database
def add_record():
    id = entry_id.get()
    name = entry_name.get()
    specialty = selected_specialty.get()  # Get selected specialty from dropdown
    phone = entry_phone.get()
    try:
        if (id and name and specialty and phone) != '':
            cursor.execute("INSERT INTO doctors (id,name, specialty, phone) VALUES (?,?, ?, ?)", 
                           (id, name, specialty, phone))
            conn.commit()
            messagebox.showinfo("Success", "Doctor record added successfully!")
            clear_entries()
            display_records()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields!")
    except:
        messagebox.showwarning("Invalid!!", "Error has occurred")

# Function to update a record in the database
def update_record():
    try:
        record_id = int(entry_id.get())
        name = entry_name.get()
        specialty = selected_specialty.get()  # Get selected specialty from dropdown
        phone = entry_phone.get()

        if name and specialty and phone:
            cursor.execute("UPDATE doctors SET name = ?, specialty = ?, phone = ? WHERE id = ?",
                           (name, specialty, phone, record_id))
            conn.commit()
            messagebox.showinfo("Success", "Doctor record updated successfully!")
            clear_entries()
            display_records()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields!")
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid ID to update!")

# Function to delete a selected record from the database
def delete_record():
    # Get the selected item from the Treeview
    selected_item = treeview.selection()
    if selected_item:
        record_id = treeview.item(selected_item)["values"][0]  # Get the ID of the selected record
        cursor.execute("DELETE FROM doctors WHERE id = ?", (record_id,))
        conn.commit()
        messagebox.showinfo("Success", "Doctor record deleted successfully!")
        display_records()
        
    else:
        messagebox.showwarning("Selection Error", "Please select a record to delete!")

# Function to clear the entry fields
def clear_entries():
    entry_id.delete(0, END)
    entry_name.delete(0, END)
    selected_specialty.set('')  # Clear dropdown selection
    entry_phone.delete(0, END)

# Function to display all doctor records in the Treeview
def display_records():
    # Clear the Treeview before displaying records
    for row in treeview.get_children():
        treeview.delete(row)

    cursor.execute("SELECT * FROM doctors")
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
        selected_specialty.set('')  # Clear dropdown selection
        entry_phone.delete(0, END)

        entry_id.insert(0, record[0])
        entry_name.insert(0, record[1])
        selected_specialty.set(record[2])  # Set dropdown value
        entry_phone.insert(0, record[3])

# Create frame1
frame1 = Frame(root)

# Create the form widgets
label_id = Label(frame1, text="Doctor ID (for update/add):")
label_name = Label(frame1, text="Doctor Name:")
label_specialty = Label(frame1, text="Specialty:")
label_phone = Label(frame1, text="Phone Number:")

entry_id = Entry(frame1)
entry_name = Entry(frame1)
entry_phone = Entry(frame1)

# Create dropdown for specialty with the four options
selected_specialty = StringVar()
selected_specialty.set('')  # Default empty value
dropdown_specialty = OptionMenu(frame1, selected_specialty, "General", "Cardio", "ENT", "Neuro")

# Create buttons for adding, updating, and deleting records
button_add = Button(root, text="Add Record", command=add_record)
button_update = Button(root, text="Update Record", command=update_record)
button_delete = Button(root, text="Delete Record", command=delete_record)

# Treeview to display records
treeview = ttk.Treeview(root, columns=("ID", "Name", "Specialty", "Phone"), show="headings", height=20)
treeview.heading("ID", text="Doctor ID")
treeview.heading("Name", text="Name")
treeview.heading("Specialty", text="Specialty")
treeview.heading("Phone", text="Phone")

# Add a binding to handle row selection (use button release1 means mouse click)
treeview.bind("<<ButtonRelease-1>>", on_select_record)

# Frame placement
frame1.grid()

# Layout management using ans sticky e means stick towards east side
label_id.grid(row=0, column=1, sticky="e", padx=10, pady=10)
entry_id.grid(row=0, column=2, padx=10, pady=10)

label_name.grid(row=1, column=1, sticky="e", padx=10, pady=10)
entry_name.grid(row=1, column=2, padx=10, pady=10)

label_specialty.grid(row=2, column=1, sticky="e", padx=10, pady=10)
dropdown_specialty.grid(row=2, column=2, padx=10, pady=10)

label_phone.grid(row=3, column=1, sticky="e", padx=10, pady=10)
entry_phone.grid(row=3, column=2, padx=10, pady=10)

button_add.grid(row=0, column=4, padx=10, pady=10, sticky="w")
button_update.grid(row=1, column=4, padx=10, pady=10, sticky="w")
button_delete.grid(row=4, column=4, padx=10, pady=10, sticky="w")

treeview.grid(row=0, column=3, rowspan=5, padx=10, pady=10)

# Display records when the app starts
display_records()

# Start the Tkinter event loop
root.mainloop()

# Close the database connection when exiting
conn.close()
