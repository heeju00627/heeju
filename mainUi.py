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

from threading import Thread
from queue import Queue

import tkinter as tk
from tkinter import ttk

import class_data as datas
import class_project as projects
import class_som as somsom

from minisom import MiniSom
from numpy import genfromtxt,array,linalg,zeros,mean,std,apply_along_axis
import numpy

import os
import re


####---------------------------------------------    
## 팝업 메시지
def popupMsg(msg):
    
    popup = tk.Tk()
    
    popup.wm_title("!")
    label = tk.Label(popup, text=msg)
    label.grid()
    
    button1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    button1.grid()
    
    popup.mainloop()


####---------------------------------------------    
## new project dialog
class newProjectDialog(tk.Toplevel):
    
    def __init__(self, controller):
        
        self.win = tk.Toplevel()
        
        ## grid 관리
        for r in range(3):
            self.win.rowconfigure(r, weight=1)
            
        for c in range(4):
            self.win.columnconfigure(c, weight=1)
        
        self.label1 = tk.Label(self.win, text="프로젝트 이름")
        self.label1.grid(row=0, column=0)
        self.label1.grid_rowconfigure(0, weight=1)
        self.label1.grid_columnconfigure(0, weight=1)
        
        self.entry1 = tk.Entry(self.win)
        self.entry1.grid(row=0, column=1, columnspan=3, sticky="ew")
        self.entry1.grid_rowconfigure(0, weight=1)
        self.entry1.grid_columnconfigure(0, weight=1)
        
        self.label2 = tk.Label(self.win, text="프로젝트 경로")
        self.label2.grid(row=1, column=0)
        self.label2.grid_rowconfigure(0, weight=1)
        self.label2.grid_columnconfigure(0, weight=1)
        
        self.entryText = tk.StringVar()
        self.entry2 = tk.Entry(self.win, textvariable=self.entryText )
        self.entry2.grid(row=1, column=1, columnspan=2, sticky="ew")
        self.entry2.grid_rowconfigure(0, weight=1)
        self.entry2.grid_columnconfigure(0, weight=1)
        
        self.button1 = ttk.Button(self.win, text="Open", command=lambda: self.loadFolder())
        self.button1.grid(row=1, column=3)
        self.button1.grid_rowconfigure(0, weight=1)
        self.button1.grid_columnconfigure(0, weight=1)
        
        self.button2 = ttk.Button(self.win, text="Okay", command=lambda: self.onSubmit(controller, self.entry1.get(), self.entry2.get()))
        self.button2.grid(row=2, column=0, columnspan=2)
        self.button2.grid_rowconfigure(0, weight=1)
        self.button2.grid_columnconfigure(0, weight=1)
        
        self.button3 = ttk.Button(self.win, text="Cancel", command=self.win.destroy)
        self.button3.grid(row=2, column=2, columnspan=2)
        self.button3.grid_rowconfigure(0, weight=1)
        self.button3.grid_columnconfigure(0, weight=1)
        
        self.win.mainloop()
        
        
    ####---------------------------------------------    
    def loadFolder(self):
        
        foldername = tk.filedialog.askdirectory()
        
        if foldername:
            self.entryText.set(foldername)
        
    def onSubmit(self, controller, name, path):
        
        if (not name):
            popupMsg("프로젝트 이름을 입력하세요")
        
        if (re.search(r'[^A-Za-z0-9_\-\\]', name)):
            popupMsg("올바른 프로젝트 이름을 입력하세요")
        
        if (not os.path.isdir(path)):
            popupMsg("올바른 경로를 입력하세요")
        
        if (name and os.path.isdir(path)):
            newProject = projects.Project(name, path)
            controller.projectList[name] = newProject
            controller.projectName.append(name)
            
            menu = controller.projectlistmenu.children["menu"]
            if (controller.projectName[0] == 'no exist'):
                menu.delete(0, "end")
                controller.projectName.remove('no exist')
            menu.add_command(label=name, command=lambda v=name: controller.selectProject(name))
            controller.selectProject(name)
            self.win.destroy()



####---------------------------------------------    
## add file dialog
class addFileDialog(tk.Toplevel):
    
    def __init__(self, controller):
        
        filenames = tk.filedialog.askopenfilenames(filetypes=[('Supported Files(.fna, .fasta)', ('*.fna', '*.fasta')), ('All','*')])
    
        if filenames:
            controller.projectList[controller.choiceVar.get()].addFiles(filenames)
            controller.selectProject(controller.choiceVar.get())





####---------------------------------------------    
## app 전체 틀
class app(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        ## tk.Tk 초기화
        tk.Tk.__init__(self, *args, **kwargs)
        
        ####---------------------------------------------   
        ## 프로젝트 리스트
        self.projectList = {}
        self.projectName = ['no exist']
        
        ####---------------------------------------------   
        ## 아이콘, 제목
        #tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "hy_som")
        
        ####---------------------------------------------   
        ## 컨테이너 관리
        container = tk.Frame(self)
        container.grid(sticky="news")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        for r in range(7):
            self.rowconfigure(r, weight=2)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
            
        for c in range(6):
            self.columnconfigure(c, weight=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)
        
        
        ####---------------------------------------------   
        ## 메뉴바
        menubar = tk.Menu(container)
        
        ## File 메뉴
        fileMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New Project...",
                                   command=lambda: self.newProject())
        fileMenu.add_command(label="Load Project...",
                                   command=lambda: popupMsg("not supported just yet"))
        fileMenu.add_command(label="Save Project...",
                                   command=lambda: popupMsg("not supported just yet"))
        fileMenu.add_command(label="Close Project...",
                                   command=lambda: popupMsg("not supported just yet"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Add File...",
                                 command=lambda: self.addFile())
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit",
                             command=self.destroy)
        
        ## Run 메뉴
        runMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=runMenu)
        runMenu.add_command(label="Convert(fna->lrn)",
                            command=lambda: popupMsg("not supported just yet"))
        runMenu.add_command(label="Training...",
                            command=lambda: popupMsg("not supported just yet"))
        
        ## Cluster 메뉴
        clusterMenu = tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Cluster", menu=clusterMenu)
        clusterMenu.add_command(label="Clustering",
                                command=lambda: popupMsg("not supported just yet"))
        clusterMenu.add_separator()
        clusterMenu.add_command(label="SOM result",
                                command=lambda: popupMsg("not supported just yet"))
        clusterMenu.add_command(label="K-Means result",
                                command=lambda: popupMsg("not supported just yet"))
        clusterMenu.add_command(label="DBSCAN result",
                                command=lambda: popupMsg("not supported just yet"))
        
        ## Help 메뉴
        helpMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="Tutorial",
                             command=lambda: popupMsg("not supported just yet"))
    
        tk.Tk.config(self, menu=menubar)
        
        
        
        ####---------------------------------------------   
        ## 제목
        label = tk.Label(self, text="HY-SOM")
        label.grid(row=0, column=0, columnspan=6)
        label.grid_rowconfigure(0, weight=1)
        label.grid_columnconfigure(0, weight=1)
        
        
        ####---------------------------------------------   
        ## 프로젝트 리스트 관리 버튼(생성, 불러오기, 저장, 닫기)
        button1 = ttk.Button(self, text="New Project..",
                             command=lambda: self.newProject())
        button1.grid(row=1, column=1, sticky="ew")
        button1.grid_rowconfigure(0, weight=1)
        button1.grid_columnconfigure(0, weight=1)
        
        button2 = ttk.Button(self, text="Load Project..",
                             command=lambda: popupMsg("not supported just yet"))
        button2.grid(row=1, column=2, sticky="ew")
        button2.grid_rowconfigure(0, weight=1)
        button2.grid_columnconfigure(0, weight=1)
        
        button3 = ttk.Button(self, text="Save Project..",
                             command=lambda: popupMsg("not supported just yet"))
        button3.grid(row=1, column=3, sticky="ew")
        button3.grid_rowconfigure(0, weight=1)
        button3.grid_columnconfigure(0, weight=1)
        
        button4 = ttk.Button(self, text="Close Project..",
                             command=lambda: popupMsg("not supported just yet"))
        button4.grid(row=1, column=4, sticky="ew")
        button4.grid_rowconfigure(0, weight=1)
        button4.grid_columnconfigure(0, weight=1)
        
        ####---------------------------------------------   
        ## 프로젝트 리스트
        self.choiceVar = tk.StringVar()
        self.choiceVar.set(self.projectName[0])
        
        ## 프로젝트 리스트 선택 메뉴
        self.projectlistmenu = tk.OptionMenu(self, self.choiceVar, *self.projectName)
        self.projectlistmenu.grid(row=2, column=1, columnspan=4, sticky="ew")
        self.projectlistmenu.grid_rowconfigure(0, weight=1)
        self.projectlistmenu.grid_columnconfigure(0, weight=1)
        
        ####---------------------------------------------   
        ## 파일 리스트 뷰
        self.filelistview = ttk.Treeview(self)
        self.filelistview .grid(row=3, rowspan=3, column=1, columnspan=4, sticky="news")
    
        ## 파일 리스트 뷰 스크롤바
        ysb = ttk.Scrollbar(self.filelistview, orient="vertical", command = self.filelistview.yview)
        xsb = ttk.Scrollbar(self.filelistview, orient="horizontal", command = self.filelistview.xview)
        self.filelistview['yscroll'] = ysb.set
        self.filelistview['xscroll'] = xsb.set
        
        self.filelistview.rowconfigure(0, weight=1)
        self.filelistview.columnconfigure(0, weight=1)
        ysb.grid(row=0, rowspan=3, column=1, sticky="ns")
        xsb.grid(row=2, column=0, columnspan=2, sticky="ew")
                
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
        
        ## 파일 리스트 뷰 옵션
        self.filelistview["columns"] = ("one", "two", "three")
        
        ## 파일 리스트 뷰 타이틀
        self.filelistview.heading("#0", text="name", anchor="w")
        self.filelistview.heading("one", text="ext", anchor="w")
        self.filelistview.heading("two", text="size", anchor="w")
        self.filelistview.heading("three", text="attached", anchor="w")
        
        ## 파일 리스트 뷰 사이즈
        self.filelistview.column("#0", width=200)
        self.filelistview.column("one", width=1)
        self.filelistview.column("two", width=1)
        self.filelistview.column("three", width=1)
        
        #filelistview.insert("", 0, text="sampleData", values=("1A", "1b"))
        #filelistview.insert("", 3, "dir3", text="Dir 3")
        #filelistview.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))
        
        ####---------------------------------------------   
        ## 파일 리스트 관리 버튼(추가, 변환, 트레이닝, 클러스터링)
        button5 = ttk.Button(self, text="Add File",
                             command=lambda: self.addFile())
        button5.grid(row=6, column=1, sticky="ew")
        button5.grid_rowconfigure(0, weight=1)
        button5.grid_columnconfigure(0, weight=1)
        
        button6 = ttk.Button(self, text="Convert",
                             command=lambda: popupMsg("not supported just yet"))
        button6.grid(row=6, column=2, sticky="ew")
        button6.grid_rowconfigure(0, weight=1)
        button6.grid_columnconfigure(0, weight=1)
        
        button7 = ttk.Button(self, text="Training",
                             command=lambda: self.callback_threaded())
        button7.grid(row=6, column=3, sticky="ew")
        button7.grid_rowconfigure(0, weight=1)
        button7.grid_columnconfigure(0, weight=1)
        
        button8 = ttk.Button(self, text="Result",
                             command=lambda: popupMsg("not supported just yet"))
        button8.grid(row=6, column=4, sticky="ew")
        button8.grid_rowconfigure(0, weight=1)
        button8.grid_columnconfigure(0, weight=1)
        
        self.training_count = 0
        self.result_count = 0
        
        
        ####---------------------------------------------   
        ## 상태바
        self.status = tk.StringVar()
        self.status.set('Preparing...')
        
        self.statusbar = tk.Label(textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.grid(row=7, column=0, columnspan=6, sticky="news")
        self.statusbar.grid_columnconfigure(0, weight=1)
        
        
        ####---------------------------------------------   
        ## 프레임 관리
        #self.frames = {}

        ## 프레임 생성
        ## 여러 페이지 돌아야 할 때
        #for F in (StartPage):
        #F = StartPage
        #frame = F(container, self)
        #self.frames[F] = frame          
        #frame.grid(row=0, column=0, sticky="nsew")
        #frame.grid_rowconfigure(0, weight=1)
        #frame.grid_columnconfigure(0, weight=1)
        
        #self.show_frame(StartPage)


    ####---------------------------------------------   
    ## 프레임 보여주기
    #def show_frame(self, cont):
        
    #    frame = self.frames[cont]
    #    frame.tkraise()
        
        
    ####---------------------------------------------   
    ## 프로젝트 선택
    def selectProject(self, name):
        self.choiceVar.set(name)
        project = self.projectList[name]
        
        self.filelistview.delete(*self.filelistview.get_children())
        for f in project.data.fileList:
            self.filelistview.insert("" , 0, text=os.path.basename(f), values=(os.path.splitext(f)[1][1:], "%d KB" % (os.path.getsize(f) / 1024) , "no"))
        
        self.status.set(project.path + '/' + project.name)
        
        
    ####---------------------------------------------   
    ## 프로젝트 생성
    def newProject(self):
        newProjectDialog(self)
        
    
    ####---------------------------------------------
    ## 파일 추가
    def addFile(self):
        if (self.projectName[0] == 'no exist'):
            popupMsg("열려 있는 프로젝트가 없습니다")
        else:
            addFileDialog(self)
        
        
    ####---------------------------------------------   
    ## THREAD 생성
    def callback_threaded(self):
        
        self.thread = Thread(target=self.somButton)
        self.thread.daemon = True
        self.thread.start()
        
        
    def somButton(self):
        
        ap2p = somsom.Som()
        ap2p.update_idletasks()  # Update "requested size" from geometry manager
        
        width = 600
        height = 400
                            
        x = (ap2p.winfo_screenwidth() - width) / 2
        y = (ap2p.winfo_screenheight() - height) / 4
            
        ap2p.geometry("%dx%d+%d+%d" %(width, height, x/2, y/2))
        ap2p.resizable(0, 0)
                
        ap2p.grid_rowconfigure(0, weight=1)
        ap2p.grid_columnconfigure(0, weight=1)
        
        ap2p.mainloop()
        
    def updateProjects(self):
        
        self.choiceVar.set(self.controller.projectName[0])
            
            
if __name__ == '__main__':
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