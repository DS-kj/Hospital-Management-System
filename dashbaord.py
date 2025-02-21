from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import subprocess
root=Tk()
root.title('Dashboard')
root.iconbitmap('icon.ico')
root.geometry('700x500')
a=Image.open(r'_DASHBOARD.png')
b=a.resize((700,500))
c=ImageTk.PhotoImage(b)
lbl=Label(image=c).place(x=0,y=0)
def Doctor():
    #opens doctor dashboard 
    process=subprocess.Popen(['python','doctorDash.py'])#refernces process to see if window is open
    root.withdraw()#hide main dashboard root
    while True:
        status = process.poll()  # Check if the process has terminated
        if status is not None:#check if window closed as when window running it returns none
            root.deiconify() #show main dashboard
            break
    
def Patience():
    roots=Toplevel()
    roots.title('Patience Page')
    roots.geometry('700x500')
    roots.iconbitmap('icon.ico')


btn=Button(root,text='Doctor',command=Doctor).place(x=120,y=170)
btn1=Button(text='Patience',command=Patience).place(x=120,y=370)
root.mainloop()