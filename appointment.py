from tkinter import *
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

# Create main window
root = Tk()
root.geometry("700x500")
root.title("Doctor Appointment System")

# Load and resize the background image
image_path = "appoint.png"  # Replace with your actual image path
bg = Image.open(image_path)
bg = bg.resize((700, 500))
bg_image = ImageTk.PhotoImage(bg)

# Create a Label to hold the image
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Set background


# Create the Date Picker
date_picker = DateEntry(root, width=12, background="blue", foreground="white", borderwidth=2)
date_picker.place(x=320, y=148)  # Positioning it to the right of the "date -" label


# Create the Time Picker 
time_slots = [f"{h if h <= 12 else h - 12}:00 {'AM' if h < 12 else 'PM'}" for h in range(9, 18)]  # 9 AM - 5 PM
time_picker = ttk.Combobox(root, width=12, values=time_slots)
time_picker.place(x=320, y=217)  # Position for time picker
time_picker.set("9:00 AM")  # Default time

conn = sqlite3.connect('appointments.db')
cursor = conn.cursor()

# Create the appointments table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY, date TEXT, time TEXT)''')
conn.commit()


# Function to store appointment in database
def store_appointment():
    selected_date = date_picker.get()
    selected_time = time_picker.get()

    if selected_date and selected_time:
        cursor.execute("INSERT INTO appointments (date, time) VALUES (?, ?)", (selected_date, selected_time))
        conn.commit()
        messagebox.showinfo("Success", f"Appointment stored:\nDate: {selected_date}\nTime: {selected_time}")
    else:
        messagebox.showwarning("Input Error", "Please select both Date and Time!")

# Search button to store data
search_button = Button(root, text="Search", command=store_appointment, font=("Arial", 10), bg="lightblue")
search_button.place(x=355, y=277)  # Position below time picker
root.mainloop()
