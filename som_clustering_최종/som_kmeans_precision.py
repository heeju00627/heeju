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
        data2=[]
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
            #data.append([x[i], y[i], z[i], clas[i]])
            data.append([x[i], y[i], z[i]])
        
         
        #np.random.seed(5)
        #centers = [[1, 1], [-1, -1], [1, -1]]   
        data = np.array(data)
        c = np.array(clas)

        cluster_num=input("cluster num: ")
        cluster_num=int(cluster_num)
        est = KMeans(n_clusters=cluster_num)
        
        fignum = 1   
        fig = plt.figure(fignum, figsize=(10, 7))   
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        
        est.fit(data)
        labels = est.labels_
        print(labels)


        num=cluster_num

        #make precision
        class_new = [[0*num] for row in range(num)]
        match1= []

        for i in range(int(n)):
            match1.append([labels[i],c[i]])
            for j in range(num):
                if(c[i]==j):
                    class_new[j].append(labels[i])
                    
        for i in range(num):
            sum_label_count=0
            cnt=Counter(class_new[i])
            print(i," count: ",cnt)
            for j in range(num):
                sum_label_count+=cnt[j]
            print(i," sum_count: ",sum_label_count)
            print(i," count_max: ",cnt.most_common(1)[0][1])
            print(i," precision: ",cnt.most_common(1)[0][1]/sum_label_count)
            print("\n")


        #make recall
        label_new = [[0*num] for row in range(num)]
        match2= []

        for i in range(int(n)):
            match2.append([labels[i],c[i]])
            for j in range(num):
                if(labels[i]==j):
                    label_new[j].append(c[i])
                    
        for i in range(num):
            sum_class_count=0
            cnt=Counter(label_new[i])
            print(i," count: ",cnt)
            for j in range(num):
                sum_class_count+=cnt[j]
            print(i," sum_count: ",sum_class_count)
            print(i," count_max: ",cnt.most_common(1)[0][1])
            print(i," recall: ",cnt.most_common(1)[0][1]/sum_class_count)
            print("\n")

        
                
        ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=labels.astype(np.float), marker='o')
        ax.view_init(20, 45)
        ax.w_xaxis.set_ticklabels([])
        ax.w_yaxis.set_ticklabels([])
        ax.w_zaxis.set_ticklabels([])
        
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        
        
        """fignum = 2   
        fig = plt.figure(fignum, figsize=(10, 7))            
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.scatter(x, y, z, c=c.astype(np.float), marker='o')
        ax.view_init(20, 45)
        
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')"""
        

        plt.show()
        

A=Plot_Umatrix()

A.plot()
