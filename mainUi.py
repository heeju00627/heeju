# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 23:01:46 2017

@author: heeju
"""

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

style.use("ggplot")
        
exchange = "default"
programName = "hysom"


#** popup message **
def popupMsg(msg):
    
    popup = tk.Tk()
    
    popup.wm_title("!")
    label = tk.Label(popup, text=msg)
    label.grid()
    #label.pack(side="top", fill="x", pady=10)
    
    button1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    button1.grid()
    #button1.pack()
    
    popup.mainloop()

#** cluster display changing **
def changeDisplay(toWhat, pn):
    
    global exchange
    global programName
    
    exchange = toWhat
    programName = pn

class app(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        #tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "hy_som")
        
        container = tk.Frame(self)
        container.grid(sticky="news")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # ** menu bar **
        menubar = tk.Menu(container)
        
        fileMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=fileMenu)
        
        subProjectMenu = tk.Menu(fileMenu, tearoff=0)
        subProjectMenu.add_command(label="Load Project...",
                                   command=lambda: popupMsg("not supported just yet"))
        subProjectMenu.add_command(label="Save Project...",
                                   command=lambda: popupMsg("not supported just yet"))
        subProjectMenu.add_command(label="Close Project...",
                                   command=lambda: popupMsg("not supported just yet"))
        fileMenu.add_cascade(label="Project", menu=subProjectMenu)
        
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit",
                             command=self.destroy)
        
        runMenu = tk.Menu(menubar, tearoff=1)
        menubar.add_cascade(label="Run", menu=runMenu)
        runMenu.add_command(label="Convert(fna->lrn)",
                            command=lambda: popupMsg("not supported just yet"))
        runMenu.add_command(label="Training...",
                            command=lambda: popupMsg("not supported just yet"))
        
        clusterMenu = tk.Menu(menubar,tearoff=1)
        menubar.add_cascade(label="Cluster", menu=clusterMenu)
        clusterMenu.add_command(label="Clustering",
                                command=lambda: popupMsg("not supported just yet"))
        clusterMenu.add_separator()
        clusterMenu.add_command(label="SOM result",
                                command=lambda: changeDisplay("SOM", "som"))
        clusterMenu.add_command(label="K-Means result",
                                command=lambda: changeDisplay("K-Means", "kmeans"))
        clusterMenu.add_command(label="DBSCAN result",
                                command=lambda: changeDisplay("DBSCAN", "dbscan"))
        
        helpMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="Tutorial",
                             command=lambda: popupMsg("not supported just yet"))
    
        tk.Tk.config(self, menu=menubar)
        
        # ** status bar **
        status = tk.Label(text="Preparing...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status.grid(row=1, sticky="news")
        status.grid_columnconfigure(0, weight=1)
        status.grid_columnconfigure(0, weight=1)
        
        # ** page frame **
        self.frames = {}

        #for F in (StartPage):
        F = StartPage
        frame = F(container, self)
        self.frames[F] = frame          
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        self.show_frame(StartPage)

        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
    
    

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
     
        tk.Frame.__init__(self, parent)
        
        for r in range(6):
            self.rowconfigure(r, weight=1)
            
        for c in range(6):
            self.columnconfigure(c, weight=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)
        
        label = tk.Label(self, text="HY-SOM")
        label.grid(row=0, column=0, columnspan=6)
        label.grid_columnconfigure(0, weight=1)
            
        listview = ttk.Treeview(self)
        listview.grid(row=1, rowspan=4, column=1, columnspan=4, sticky="news")
    
        ysb = ttk.Scrollbar(listview, orient="vertical", command = listview.yview)
        xsb = ttk.Scrollbar(listview, orient="horizontal", command = listview.xview)
        listview['yscroll'] = ysb.set
        listview['xscroll'] = xsb.set
        
        listview.rowconfigure(0, weight=1)
        listview.columnconfigure(0, weight=1)
        ysb.grid(row=0, rowspan=4, column=1, sticky="ns")
        xsb.grid(row=4, column=0, columnspan=2, sticky="ew")
                
        #tree["columns"]=("one","two")
        #tree.column("one", width=100 )
        #tree.column("two", width=100)
        #tree.heading("one", text="coulmn A")
        #tree.heading("two", text="column B")
        #tree.insert("" , 0,    text="Line 1", values=("1A","1b"))
        #id2 = tree.insert("", 1, "dir2", text="Dir 2")
        #tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))
        
        #listview.insert(self, "end", "sampleData.txt")
        #fileList = self.openFile()
        #for file in fileList:
        #listbox.insert("end", file) 
        
        listview["columns"] = ("one", "two")
        #listview.column("zero", width=1)
        
        listview.heading("#0", text="project", anchor="w")
        listview.heading("one", text="type", anchor="w")
        listview.heading("two", text="name", anchor="w")
        
        listview.column("#0", width=4)
        listview.column("one", width=1)
        listview.column("two", width=1)
        
        listview.insert("", 0, text="sampleData", values=("1A", "1b"))
        listview.insert("", 3, "dir3", text="Dir 3")
        listview.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))
        
        button1 = ttk.Button(self, text="Add" )
        button1.grid(row=5, column=1, sticky="ew")
        button1.grid_rowconfigure(0, weight=1)
        button1.grid_columnconfigure(0, weight=1)
        
        button2 = ttk.Button(self, text="Convert" )
        button2.grid(row=5, column=2, sticky="ew")
        button2.grid_rowconfigure(0, weight=1)
        button2.grid_columnconfigure(0, weight=1)
        
        button3 = ttk.Button(self, text="Training" )
        button3.grid(row=5, column=3, sticky="ew")
        button3.grid_rowconfigure(0, weight=1)
        button3.grid_columnconfigure(0, weight=1)
        
        button4 = ttk.Button(self, text="Result" )
        button4.grid(row=5, column=4, sticky="ew")
        button4.grid_rowconfigure(0, weight=1)
        button4.grid_columnconfigure(0, weight=1)
        
        
        
app = app()
app.update_idletasks()  # Update "requested size" from geometry manager

width = 600
height = 400
                    
x = (app.winfo_screenwidth() - width) / 2
y = (app.winfo_screenheight() - height) / 4
    
app.geometry("%dx%d+%d+%d" %(width, height, x, y))
app.resizable(0, 0)
        
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

app.mainloop()