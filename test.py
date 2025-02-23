import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

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

def display_appointments():
    # Fetch today's appointments from the database
    appointments = fetch_appointments()

    # Create a Tkinter window
    window = tk.Tk()
    window.title("Hospital Appointments")

    # Create a frame for the appointment list
    frame = tk.Frame(window)
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Add a label on top of the frame
    label = tk.Label(frame, text="Today's Appointments", font=("Arial", 16))
    label.pack(pady=10)

    # Set up a treeview widget to display the appointments in a table format
    tree = ttk.Treeview(frame, columns=("Id", "Patient Name", "Doctor Name", "Time"), show="headings")
    
    # Define the column headings
    tree.heading("Id", text="Appointment ID")
    tree.heading("Patient Name", text="Patient Name")
    tree.heading("Doctor Name", text="Doctor Name")
    tree.heading("Time", text="Time")

    # Insert the appointments into the treeview
    for appointment in appointments:
        appointment_id, patient_name, doctor_name, appointment_time = appointment
        tree.insert("", tk.END, values=(appointment_id, patient_name, doctor_name, appointment_time))

    # Pack the treeview widget to fill the frame
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Run the Tkinter main loop
    window.mainloop()

# Call the function to display appointments
display_appointments()
