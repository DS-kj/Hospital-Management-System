from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import subprocess
from tkinter import ttk
import sqlite3
from datetime import datetime
root=Tk()
root.title('Dashboard')
root.iconbitmap('icon.ico')
root.geometry('1500x750+0+0')#zero added for centering the window when it opens at first
root.resizable(0,0)
a=Image.open(r'_DASHBOARD.png')
b=a.resize((1550,800))
c=ImageTk.PhotoImage(b)
lbl=Label(image=c).place(relheight=1,relwidth=1)

def Doctor():
    #opens doctor dashboard 
    process=subprocess.Popen(['python','doctorDash.py'])#refernces process to see if window is open
    root.destroy()#hide main dashboard root
    while True:
        status = process.poll()  # Check if the process has terminated
        if status is not None:# check if window closed as when window running it returns none
            subprocess.Popen(['python','dashboard.py'])# show main dashboard
            break

def Patient():
    #opens doctor dashboard 
    process=subprocess.Popen(['python','patient.py'])#refernces process to see if window is open
    root.destroy()#hide main dashboard root
    while True:
        status = process.poll()  # Check if the process has terminated
        if status is not None:# check if window closed as when window running it returns none
            subprocess.Popen(['python','dashboard.py']) # show main dashboard
            break


def fetch_appointments():
    # Connect to SQLite database
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Get today's date in the format 'YYYY-MM-DD'
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    # Query to fetch appointments that are today, including doctor name, and time, sorted by appointment time
    cursor.execute("""
    SELECT a.id, p.name AS patient_name, d.name AS doctor_name, a.appointment_time 
    FROM appointments a
    JOIN doctors d ON a.doctor_id = d.id
    JOIN patients p ON a.patient_id = p.id
    WHERE DATE(a.appointment_date) = ?
    ORDER BY a.appointment_time ASC
    """, (today_date,))  # Pass today_date to filter by today's appointments
    appointments = cursor.fetchall()

    conn.close()
    
    return appointments

# Fetch today's appointments from the database
appointments = fetch_appointments()

# Create a frame for the appointment list
frame = Frame(root,bg="#29b5e3")
frame.place(x=550,y=0)

# Add a label on top of the frame
label = Label(frame, text="Today's Appointments", font=("Times New Roman", 16),bg="#29b5e3")
label.pack(pady=10)

# Set up a treeview widget to display the appointments in a table format
tree = ttk.Treeview(frame, columns=("Id", "Patient Name", "Doctor Name", "Time"), show="headings",height=30)

# Define the column headings
tree.heading("Id", text="Appointment ID")
tree.heading("Patient Name", text="Patient Name")
tree.heading("Doctor Name", text="Doctor Name")
tree.heading("Time", text="Time")

# Insert the appointments into the treeview
for appointment in appointments:
    appointment_id, patient_name, doctor_name, appointment_time = appointment
    tree.insert("", END, values=(appointment_id, patient_name, doctor_name, appointment_time))

# Pack the treeview widget to fill the frame
tree.pack(padx=10, pady=10, expand=True)


#Main buttons
btn=Button(root,text='Doctor',command=Doctor).place(x=270,y=220)
btn1=Button(root,text='Patient',command=Patient).place(x=270,y=550)


#run window called root in loop
root.mainloop()