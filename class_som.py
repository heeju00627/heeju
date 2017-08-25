# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 22:45:37 2017

@author: heeju
"""

from pylab import matplotlib,plot,axis,show,pcolor,colorbar,bone
import numpy as np
from matplotlib import pylab as pl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style

from threading import Thread, Event

from queue import Queue

import tkinter as tk
from tkinter import ttk

import class_data as datas
import class_project as projects

from minisom import MiniSom
from numpy import genfromtxt,array,linalg,zeros,mean,std,apply_along_axis
import numpy


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

## som 결과 window에 대한 class
class Som(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        ####---------------------------------------------   
        ## 프로젝트 리스트
        self.projectList = []
        
        ####---------------------------------------------   
        ## 아이콘, 제목
        #tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "training result")
        
        ####---------------------------------------------   
        ## 컨테이너 관리
        container = tk.Frame(self)
        container.grid(sticky="news")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        ####---------------------------------------------   
        ## 메뉴바
        menubar = tk.Menu(container)
        
        ## File 메뉴
        fileMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=fileMenu)
        
        fileMenu.add_command(label="Exit",
                             command=self.destroy)
        
        ## Help 메뉴
        helpMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="Tutorial",
                             command=lambda: popupMsg("not supported just yet"))
    
        tk.Tk.config(self, menu=menubar)
        
        ####---------------------------------------------   
        ## 상태바
        self.status = tk.StringVar()
        
        statusbar = tk.Label(container, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        statusbar.grid(row=1, sticky="news")
        statusbar.grid_columnconfigure(0, weight=1)
        statusbar.grid_columnconfigure(0, weight=1)
        
        ####---------------------------------------------   
        ## 프레임 관리
        self.frames = {}

        ## 프레임 생성
        ## 여러 페이지 돌아야 할 때
        #for F in (StartPage, ...):
        F = SomPage
        frame = F(container, self)
        self.frames[F] = frame          
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        self.executeSom()
    
    ## 솜 실행하기
    def executeSom(self):
        
        frame = self.frames[SomPage]
        frame.callback_threaded(self.status)
    
####---------------------------------------------    
## 솜 결과 페이지
## 솜 동작 관리
class SomPage(tk.Frame):
    
    ## UI 생성
    def __init__(self, parent, controller):
     
        ## tk.Frame 초기화
        tk.Frame.__init__(self, parent)
        
        style.use("ggplot")

        self.figure = pl.figure(1)
        self.a = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(sticky="news")
        self.canvas._tkcanvas.grid(sticky="news")
        
        ## Initialization
        self.som = MiniSom(10,10,136,sigma=1.0,learning_rate=0.5)
    
    ####---------------------------------------------   
    ## THREAD 생성
    def callback_threaded(self, status):
        
        self.queue = Queue()    # 크기가 1인 버퍼
        
        self.thread = Thread(target=self.training, args=(status,))
        self.thread.daemon = True
        self.thread.start()
        
        self.queue.put(object()) ## 첫번째
        print("Start")
        self.queue.join() ## 네번째
        self.thread.join()
        self.plotting(status)
        
    
    ## size, learning_rate, training_count, target_count)
    def training(self, status):
        
        self.figure.clear()
        self.queue.get() ## 두번째
        
        ## reading the dataset in the csv format  
        self.data = genfromtxt('iris6.csv', delimiter=',',dtype = float)
        self.data = numpy.nan_to_num(self.data)
        ## data normalization
        self.data = apply_along_axis(lambda x: x/linalg.norm(x),1,self.data) 
        
        self.som.random_weights_init(self.data)
        
        print("Training...")
        
        self.som.train_random(self.data,100) # random training
        
        bone()
        ## plotting the distance map as background
        pcolor(self.som.distance_map().T)
        colorbar()
        
        ## loadingthe labels
        target = genfromtxt('iris4_2.csv', delimiter=',', usecols=(0), dtype=int)
        self.t = zeros(len(target),dtype=int)
        
        print("...ready to plot...")
        
        for i in range(len(target)):
            self.t[target == i] = i
        
        self.som.win_map(self.data)
        
        self.queue.task_done() ## 세번째
        
    def plotting(self, status):
        
        self.figure = pl.figure(1)
        self.a = self.figure.add_subplot(111)
        
        print("Plotting...")
        
        ## use differet colors and markers for each label
        ## markers = []
        colors = ['r','g','b','y','w','orange','black','pink','brown','purple']
        
        ## making bm file
        with open('bm.txt', 'w') as f:
             f.write(str(len(self.data))+'\n')
             for cnt,xx in enumerate(self.data):
                 win = self.som.winner(xx) # getting the winner
             # palce a marker on the winning position for the sample xx
                 self.a.plot(win[0]+.5,win[1]+.5,'.', markerfacecolor='None', markeredgecolor=colors[self.t[cnt]], markersize=1, markeredgewidth=1)
                 f.write(str(win[0])+'\t'+str(win[1])+'\t'+str(self.t[cnt])+'\n')
        
        ## making umx file
        with open('umx.txt', 'w') as f:
            for cnt,xx in enumerate(self.data):
             win = self.som.winner(xx) # getting the winner
             # palce a marker on the winning position for the sample xx
             self.a.plot(win[0]+.5,win[1]+.5,'.',markerfacecolor='None',
                   markeredgecolor=colors[self.t[cnt]], markersize=1, markeredgewidth=1)
            um=self.som.distance_map()
            for i in range(10):
                for j in range(10):
                    f.write(str(um[i,j])+'\t')
                f.write('\n')
        
        f.close()
        #self.a.axis([0,self.som.weights.shape[0], 0, self.som.weights.shape[1]])
        
        print("Finished!")
        self.canvas.show()