from tkinter import*
from tkinter import messagebox
from PIL import Image,ImageTk
root=Tk()
root.title('Dashboard')
root.iconbitmap('icon.ico')
root.geometry('700x500')
a=Image.open(r'C:\Users\batas\OneDrive\Desktop\Code-Freaks\_DASHBOARD.png')
b=a.resize((700,500))
def Doctor():
    roots=Toplevel()
    roots.title('Doctor page')
    roots.geometry('700x500')
    roots.iconbitmap('icon.ico')

def Patience():
    roots=Toplevel()
    roots.title('Patience Page')
    roots.geometry('700x500')
    roots.iconbitmap('icon.ico')

c=ImageTk.PhotoImage(b)
lbl=Label(image=c).place(x=0,y=0)
btn=Button(root,text='Doctor',command=Doctor).place(x=120,y=170)
btn1=Button(text='Patience',command=Patience).place(x=120,y=370)
root.mainloop()