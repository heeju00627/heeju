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
   
        
    def plot(self):
        num = 10;
        x = []
        y = []
        z = []
        clas = []
        names = []
        data = []
        #print("BBB")
        n=0
        with open('bm.txt', 'r') as bm:
            
            n=bm.readline()
            for i in range(int(n)):
                line=bm.readline().split('\t')
                x.append(int(line[0]))
                y.append(int(line[1]))
                clas.append(int(line[2]))
            
        #print("AAA")
        #print(len(x))
        with open('umx.txt', 'r') as umx:
            matrix = umx.read().split("\n")
            
            for i in range(int(n)):
                tmp=matrix[x[i]]
                s=tmp.split('\t')
                z.append(float(s[y[i]]))
        #print(len(clas))
        #print(len(x))
        #print(len(y))
        #print(len(z))
        for i in range(int(n)):
            data.append([x[i], y[i], z[i], clas[i]])
        
         
        np.random.seed(5)
        centers = [[1, 1], [-1, -1], [1, -1]]   
        data = np.array(data)
        c = np.array(clas)
        est = KMeans(n_clusters=10)
        
        fignum = 1   
        fig = plt.figure(fignum, figsize=(10, 7))   
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        
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

        #print(len(labels))
        #print(len(c))
        #print(size)
        for i in range(int(n)):
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
            
        cnt0=Counter(class0)
        cnt1=Counter(class1)
        cnt2=Counter(class2)
        cnt3=Counter(class3)
        cnt4=Counter(class4)
        cnt5=Counter(class5)
       
        print(cnt0.most_common(1)[0][1]/clas.count(0))
        print(cnt1.most_common(1)[0][1]/clas.count(1))
        print(cnt2.most_common(1)[0][1]/clas.count(2))
        print(cnt3.most_common(1)[0][1]/clas.count(3))
        print(cnt4.most_common(1)[0][1]/clas.count(4))
        
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
        

A=Plot_Umatrix()

A.plot()
