# -*- coding: utf-8 -*-
"""
Created on Fri May 19 05:44:01 2017

@author: heeju
"""

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
#matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

style.use("ggplot")
        
f = Figure()
a = f.add_subplot(111)
#a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])


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


#** load file **
def loadFile():
    
    fileList = []
    return fileList


#** save file **
def saveFile():
    
    pass


#** cluster display changing **
def changeDisplay(toWhat, pn):
    
    global exchange
    global programName
    
    exchange = toWhat
    programName = pn


#** live graph updating **
def animate(i):
    
    pullData = open("sampleData.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))       
    a.clear()
    a.plot(xList, yList)


def tutorial():
    pass


class Table(tk.Frame): 
       
    def __init__(self, parent, rows=12, columns=2):
        pullData = open("sampleData.txt", "r").read()
        data.append(pullData)
        dataList = pullData.split('\n')
        xList = []
        yList = []
        for eachLine in dataList:
            if len(eachLine) > 1:
                x, y = eachLine.split(',')
                xList.append(int(x))
                yList.append(int(y))
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent)
        self._widgets = []
        i = 0
        for row in xList:
            current_row = []
            label = tk.Label(self, text="%s" %(row), 
                                 borderwidth=0, width=10)
            label.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            label = tk.Label(self, text="%s" %(yList[i]), 
                                 borderwidth=0, width=10)
            label.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            self._widgets.append(current_row)
            i = i + 1

        for column in yList:
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure()


class app(tk.Tk):
    global data
    global fileList
    data = []
    fileList = []
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        #tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "hy_som")
        
        container = tk.Frame(self)
        container.grid(sticky="news")
        #container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # ** menu bar **
        menubar = tk.Menu(container)
        
        fileMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open...",
                             command=lambda: popupMsg("not supported just yet"))
        fileMenu.add_command(label="Save...",
                             command=lambda: popupMsg("not supported just yet"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Close...",
                             command=lambda: popupMsg("not supported just yet"))  # 일부 file 닫기(목록에서 제거)
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
                             command=tutorial)
    
        tk.Tk.config(self, menu=menubar)
        
        # ** status bar **
        status = tk.Label(text="Preparing...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        #status.pack(side="bottom", fill="x")
        status.grid(row=1, sticky="news")
        status.grid_columnconfigure(0, weight=1)
        status.grid_columnconfigure(0, weight=1)
        
        # ** page frame **
        self.frames = {}

        for F in (StartPage, MainPage):
            frame = F(container, self)
            self.frames[F] = frame          
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
        
        self.show_frame(StartPage)

        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
    
    def show_tab(self, cont, tab):
        
        frame = self.frames[cont]
        frame.tkraise()
        frame.notebook.select(tab)
        

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
     
        tk.Frame.__init__(self, parent)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        
        for c in range(1):
            self.columnconfigure(c, weight=1)
        
        label = tk.Label(self, text="Start Page")
        label.grid(row=0)
        label.grid_rowconfigure(0, weight=1)
        label.grid_columnconfigure(0, weight=1)
        #label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Text Page",
                            command=lambda: controller.show_tab(MainPage, 1))
        button1.grid(row=1)
        button1.grid_rowconfigure(0, weight=1)
        button1.grid_columnconfigure(0, weight=1)
        #button1.pack()
        
        button2 = ttk.Button(self, text="Data Page",
                            command=lambda: controller.show_tab(MainPage, 2))
        button2.grid(row=2)
        button2.grid_rowconfigure(0, weight=1)
        button2.grid_columnconfigure(0, weight=1)
        #button2.pack()
        button3 = ttk.Button(self, text="Map Page",
                            command=lambda: controller.show_tab(MainPage, 3))
        button3.grid(row=3)
        button3.grid_rowconfigure(0, weight=1)
        button3.grid_columnconfigure(0, weight=1)
        #button3.pack()
        

class MainPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        for r in range(6):
            self.rowconfigure(r, weight=1)    
        for c in range(5):
            self.columnconfigure(c, weight=1)
            
        # ** top frame **
        top_frame = tk.Frame(self, bg="red")
        top_frame.grid(row=0, column=0, columnspan=8, sticky="news")
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(0, weight=1)
        
        #top_frame.pack(side="top")
        label1 = tk.Label(top_frame, text="Top Page")
        label1.grid(row=0, column=0)
        #label1.pack(side="left", pady=10, padx=10)        
        
        button1 = ttk.Button(top_frame, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=1)
        #button1.pack(side="right")
        
        # ** list frame **
        list_frame = tk.Frame(self, borderwidth=20, bg="blue")
        list_frame.grid(row=1, column=0, rowspan=3, sticky="wens")
        
        for r in range(4):
            if (r < 2):
                list_frame.rowconfigure(r, weight=1)
            if (r >= 2):
                list_frame.rowconfigure(r, weight=6)
        for c in range(2):
            list_frame.columnconfigure(c, weight=1)
        #list_frame.pack()
        
        label2 = tk.Label(list_frame, text="List")
        label2.grid(row=0, column=0, columnspan=2, sticky="new")
        #labe2.pack(side="top")
            
        button2 = ttk.Button(list_frame, text="Add",
                             command=lambda: popupMsg("not supported just yet"))
                            #command=lambda: controller.openFile())
        button2.grid(row=1, column=0)
        #button2.pack()
        
        button3 = ttk.Button(list_frame, text="Close",
                             command=lambda: popupMsg("not supported just yet"))
                            #command=lambda: controller.closeFile())
        button3.grid(row=1, column=1)
        #button3.pack()
        
        #self.dataCols = ('fullpath', 'type', 'size')
        #listview = ttk.Treeview(columns=self.dataCols, displaycolumns='size')
        listview = ttk.Treeview(list_frame)
        listview.grid(row=2, column=0, rowspan=6, columnspan=2, sticky="news")
        #listbox.pack(fill="y")
    
        ysb = ttk.Scrollbar(listview, orient="vertical", command=listview.yview)
        xsb = ttk.Scrollbar(listview, orient="horizontal", command=listview.xview)
        listview['yscroll'] = ysb.set
        listview['xscroll'] = xsb.set
        
        listview.rowconfigure(0, weight=1)
        listview.columnconfigure(0, weight=1)
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")
                
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
        
        
        # ** property frame **
        property_frame = tk.Frame(self, borderwidth=20, bg="green")
        property_frame.grid(row=4, column=0, rowspan=2, sticky="wens")
        property_frame.grid_rowconfigure(0, weight=1)
        property_frame.grid_columnconfigure(0, weight=1)
        #property_frame.pack()
        
        label3 = tk.Label(property_frame, text="Property")
        label3.grid()
        #labe3.pack(side="top")
        
        # ** implement tab **
        notebook= ttk.Notebook(self)
        
        # ** tab frame **
        self.frames = {}

        for F in (TabOne, TabTwo, TabThree):
            frame = F(notebook, self)
            self.frames[F] = frame          
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            notebook.add(self.frames[F], text=frame._name)
        
        notebook.grid(row=1, column=1, rowspan=5, columnspan=10, sticky="nesw")
        notebook.grid_rowconfigure(1, weight=1)
        notebook.grid_columnconfigure(1, weight=1)
        #notebook.pack(fill="both", expand=True)

    
class TabOne(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=8)
        
        label = tk.Label(self, text="Text Tab")
        label.grid(row=0)
        #label.pack(pady=10, padx=10)
        
        text = tk.Text(self)
        text.grid(row=1, sticky="news")
        #text.pack(fill="both", expand=True)
        data.append("hello")
        text.insert('end', data)
        
    
class TabTwo(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=8)
        
        label = tk.Label(self, text="Data Tab")
        label.grid(row=0)
        #label.pack(pady=10, padx=10)
        
        t = Table(self, 11, 2)
        t.grid(row=1, sticky="news")
        #t.pack(side="top")
        t.set(0, 0, "Hello, world")
        
        
class TabThree(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=8)
        
        label = tk.Label(self, text="Map Tab")
        label.grid(row=0)
        #label.pack(pady=10, padx=10)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().grid(row=1, sticky="news")
        #canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        
        #toolbar = NavigationToolbar2TkAgg(canvas, self)
        #toolbar.update()
        canvas._tkcanvas.grid(sticky="news")
        #canvas._tkcanvas.pack(side="bottom", fill="both", expand=True)

        
app = app()
app.update_idletasks()  # Update "requested size" from geometry manager

width = 1280
height = 720
                    
x = (app.winfo_screenwidth() - width) / 2
y = (app.winfo_screenheight() - height) / 4
    
app.geometry("%dx%d+%d+%d" %(width, height, x, y))
app.resizable(0, 0)
        
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

ani = animation.FuncAnimation(f, animate)
app.mainloop()