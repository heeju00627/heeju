# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 15:11:14 2017

@author: heeju
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Plot_Umatrix():
    def __init__(self, parent = None, width = 5, height = 4, dpi = 1000):
        fig = Figure(figsize = (width, height), dpi = dpi)
        self.axes = fig.add_subplot(111)
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
        
    def plot(self):
        num = 10;
        x = []
        y = []
        z = []
        clas = []
        names = []
        data = []
        
        with open('Tetra_esom_2500_50x82e20.bm', 'r') as bm:
            size = bm.readline().split("%")[1]
            k = int(size.split(" ")[0])
            l = int(size.split(" ")[1])
            n = int(bm.readline().split("%")[1])
            
            for i in range(n):
                cord = bm.readline().split("\n")[0]
                cord = cord.split("\t")
                x.append(int(cord[1]))
                y.append(int(cord[2]))
                
        with open('Tetra_esom_2500_50x82e20.umx', 'r') as umx:
            umx.readline()
            matrix = umx.read().split("\n")
            
            for i in range(n):
                z.append(float(matrix[x[i]].split("\t")[y[i]]))
                
        with open('Tetra_esom_2500.cls', 'r') as cls:
            size = int(cls.readline().split(" ")[1])
            for i in range(num):
                names.append(cls.readline().split("\t")[1])
                
            for j in range(size):
                clas.append(int(cls.readline().split("\t")[1]))
        
        for i in range(size):
            data.append([x[i], y[i], z[i], clas[i]])
        
        #X = np.array(x, y, z)
        #kmeans = KMeans(n_clusters=10, random_state=0).fit(X)
        
         
        np.random.seed(5)
        centers = [[1, 1], [-1, -1], [1, -1]]   
        data = np.array(data)
        c = np.array(clas)
        est = KMeans(n_clusters=10)
        
        fignum = 1   
        fig = plt.figure(fignum, figsize=(10, 7))   
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        #ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
        #plt.clf()
        #plt.cla()
        est.fit(data)
        labels = est.labels_
        
        match= []
        class0 = []
        class1 = []
        class2 = []
        class3 = []
        class4 = []
        class5 = []
        class6 = []
        class7 = []
        class8 = []
        class9 = []
        
        for i in range(size):
            match.append([labels[i], c[i]])
            if (c[i] == 0):
                class0.append(labels[i])
            elif (c[i] == 1):
                class1.append(labels[i])
            elif (c[i] == 2):
                class2.append(labels[i])
            elif (c[i] == 3):
                class3.append(labels[i])
            elif (c[i] == 4):
                class4.append(labels[i])
            elif (c[i] == 5):
                class5.append(labels[i])
            elif (c[i] == 6):
                class6.append(labels[i])
            elif (c[i] == 7):
                class7.append(labels[i])
            elif (c[i] == 8):
                class8.append(labels[i])
            elif (c[i] == 9):
                class9.append(labels[i])
            
        cnt0=Counter(class0)
        cnt1=Counter(class1)
        cnt2=Counter(class2)
        cnt3=Counter(class3)
        cnt4=Counter(class4)
        cnt5=Counter(class5)
        cnt6=Counter(class6)
        cnt7=Counter(class7)
        cnt8=Counter(class8)
        cnt9=Counter(class9)
        print(cnt0.most_common(1)[0][1]/clas.count(0))
        print(cnt1.most_common(1)[0][1]/clas.count(1))
        print(cnt2.most_common(1)[0][1]/clas.count(2))
        print(cnt3.most_common(1)[0][1]/clas.count(3))
        print(cnt4.most_common(1)[0][1]/clas.count(4))
        print(cnt5.most_common(1)[0][1]/clas.count(5))
        print(cnt6.most_common(1)[0][1]/clas.count(6))
        print(cnt7.most_common(1)[0][1]/clas.count(7))
        print(cnt8.most_common(1)[0][1]/clas.count(8))
        print(cnt9.most_common(1)[0][1]/clas.count(9))
        
        ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=labels.astype(np.float), marker='o')
        ax.view_init(20, 45)
        ax.w_xaxis.set_ticklabels([])
        ax.w_yaxis.set_ticklabels([])
        ax.w_zaxis.set_ticklabels([])
        
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        
        
        fignum = 2   
        fig = plt.figure(fignum, figsize=(10, 7))            
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.scatter(x, y, z, c=c.astype(np.float), marker='o')
        ax.view_init(20, 45)
        
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        
        plt.show()
        self.draw()