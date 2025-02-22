import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image,ImageTk
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

# Connect to SQLite Database
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Create the necessary tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    specialty TEXT NOT NULL,
                    phone TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    doctor_id INTEGER NOT NULL,
                    patient_id INTEGER NOT NULL,
                    appointment_date TEXT NOT NULL,
                    appointment_time TEXT NOT NULL,
                    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
                    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE)''')

# Function to add an appointment
def add_appointment():
    doctor_id = selected_doctor.get()
    patient_id = selected_patient.get()
    appointment_date = entry_date.get_date()  # Get the date from the DateEntry widget
    appointment_time = entry_time.get()  # Get the time from the Entry widget
    try:
        if doctor_id and patient_id and appointment_date and appointment_time:
            cursor.execute("INSERT INTO appointments (doctor_id, patient_id, appointment_date, appointment_time) VALUES (?, ?, ?, ?)",
                        (doctor_id, patient_id, appointment_date, appointment_time))
            conn.commit()
            messagebox.showinfo("Success", "Appointment added successfully!")
            clear_entries()
            display_appointments()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields!")
    except:
        messagebox.showerror("db error")
# Function to delete a selected appointment
def delete_appointment():
    try:
        selected_item = treeview.selection()
        if selected_item:
            appointment_id = treeview.item(selected_item)["values"][0]
            cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
            conn.commit()
            messagebox.showinfo("Success", "Appointment deleted successfully!")
            display_appointments()
        else:
            messagebox.showwarning("Selection Error", "Please select an appointment to delete!")
    except:
        messagebox.showerror("db error")
# Function to clear the entry fields
def clear_entries():
    selected_doctor.set('')
    selected_patient.set('')
    entry_date.delete(0, END)
    entry_time.delete(0, END)

# Function to display all appointments in the Treeview
def display_appointments():
    try:
        # Clear the Treeview before displaying records
        for row in treeview.get_children():
            treeview.delete(row)

        cursor.execute("SELECT a.id, d.name, p.name, a.appointment_date, a.appointment_time FROM appointments a "
                    "JOIN doctors d ON a.doctor_id = d.id "
                    "JOIN patients p ON a.patient_id = p.id")
        rows = cursor.fetchall()

        # Display the records in the Treeview
        for row in rows:
            treeview.insert("", END, values=row)
    except:
        messagebox.showerror("db error")
# Function to populate doctor dropdown based on specialty
def get_doctors():
    try:
        specialty = selected_specialty.get()
        cursor.execute("SELECT id, name FROM doctors WHERE specialty = ?", (specialty,))
        doctors = cursor.fetchall()

        # Clear existing doctor options
        doctor_menu['menu'].delete(0, 'end')

        # Add new doctor options based on selected specialty
        for doctor in doctors:
            doctor_menu['menu'].add_command(label=f"{doctor[0]} - {doctor[1]}", command=lambda value=doctor[0]: selected_doctor.set(value))
    except:
        messagebox.showerror("db error")

# Function to populate patient dropdown with name and ID
def get_patients():
    try:
        cursor.execute("SELECT id, name FROM patients")
        patients = cursor.fetchall()

        # Clear existing patient options
        patient_menu['menu'].delete(0, 'end')

        # Add new patient options with name and ID displayed
        for patient in patients:
            patient_menu['menu'].add_command(label=f"{patient[1]} (ID: {patient[0]})", command=lambda value=patient[0]: selected_patient.set(value))
    except:
        messagebox.showerror("db error")    
# Frame setup
root = Tk()
root.title("Appointment System")
root.geometry("1400x600")
root.iconbitmap('icon.ico')
root.resizable(0,0)

#adding background image
# adding image
img = Image.open(r'appointment.jpg')
# need to use this to turn img into tkinter usable format
final_img= ImageTk.PhotoImage(img)
# create label and pack it as background
l = Label(image=final_img)
l.place(relheight=1, relwidth=1)

# Create frames for layout
left_col='#befbfe'
right_col='#beeffe'
frame_left = Frame(root,bg=left_col)
frame_left.pack(side=LEFT, padx=10, pady=10)

frame_right = Frame(root,bg=right_col)
frame_right.pack(side=RIGHT, padx=10, pady=10,)

# Creating widgets for the left frame (form inputs)
label_specialty = Label(frame_left, text="Select Specialty:",bg=left_col)
label_specialty.pack(pady=10)

specialty_options = ["General", "Cardio", "ENT", "Neuro"]
selected_specialty = StringVar()
selected_specialty.set(specialty_options[0])  # default value
specialty_menu = OptionMenu(frame_left, selected_specialty, *specialty_options)
specialty_menu.pack(pady=10)

# Button to load doctors based on specialty
button_load_doctors = Button(frame_left, text="Load Doctors", command=get_doctors)
button_load_doctors.pack(pady=10)

label_doctor = Label(frame_left, text="Select Doctor:",bg=left_col)
label_doctor.pack(pady=10)

selected_doctor = StringVar()
doctor_menu = OptionMenu(frame_left, selected_doctor, "")
doctor_menu.pack(pady=10)

label_patient = Label(frame_left, text="Select Patient:",bg=left_col)
label_patient.pack(pady=10)

selected_patient = StringVar()
patient_menu = OptionMenu(frame_left, selected_patient, "")
patient_menu.pack(pady=10)

# Use DateEntry widget for the date
label_date = Label(frame_left, text="Appointment Date:",bg=left_col)
label_date.pack(pady=10)

entry_date = DateEntry(frame_left, date_pattern='yyyy-mm-dd')  # Date format
entry_date.pack(pady=10)

label_time = Label(frame_left, text="Appointment Time (HH:MM):",bg=left_col)
label_time.pack(pady=10)

# Create the Time Picker 
time_slots = [f"{h if h <= 12 else h - 12}:00 {'AM' if h < 12 else 'PM'}" for h in range(9, 18)]  # 9 AM - 5 PM
entry_time = ttk.Combobox(frame_left, width=12, values=time_slots)
entry_time.pack(pady=10)  # Position for time picker
entry_time.set("9:00 AM")  # Default time
# Add appointment button
button_add_appointment = Button(frame_left, text="Add Appointment", command=add_appointment)
button_add_appointment.pack(pady=10)

# Button to delete appointment
button_delete_appointment = Button(frame_left, text="Delete Appointment", command=delete_appointment)
button_delete_appointment.pack(pady=10)

# Widget for right frame
label_head=Label(frame_right, text="Appointments",font=('Times new roman',30),bg=right_col)
label_head.pack(pady=10)

# Treeview to display appointments in the right frame
treeview = ttk.Treeview(frame_right, columns=("ID", "Doctor", "Patient", "Date", "Time"), show="headings",height=30)
treeview.heading("ID", text="Appointment ID")
treeview.heading("Doctor", text="Doctor")
treeview.heading("Patient", text="Patient")
treeview.heading("Date", text="Date")
treeview.heading("Time", text="Time")
treeview.pack(pady=20)

# Load patients and doctors
get_patients()
get_doctors()

# Display appointments on startup
display_appointments()

# Start Tkinter main loop
root.mainloop()

# Close the database connection when exiting
conn.close()
