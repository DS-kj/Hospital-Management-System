from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import sqlite3
import subprocess
class default_login():
    wd=0#width
    ht=0#height
    img=''
    def __init__(self,a,b,path):
        self.wd=a
        self.ht=b
        self.img=f'{path}'
        # '''create main window root'''
    def create(self):
        root = Tk()
        #(window width x window height + display x cordinate + y cordinate (400 puts it in center) )
        root.geometry(f'{self.wd}x{self.ht}+400+0')
        #window can't be changed in size (neither width, nor height)
        root.resizable(0,0)
        root.iconbitmap("icon.ico")
        # '''putting background images'''

    a=Image.open('log1.png')
    #resize
    b=a.resize((w_le))
    #need to use this to turn img into tkinter usable format
    c=ImageTk.PhotoImage(b)
    #create label and pack it as background
    l=Label(image=c) 
    l.grid()