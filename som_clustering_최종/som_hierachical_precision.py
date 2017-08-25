

import time as time
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets.samples_generator import make_swiss_roll
from collections import Counter

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

n_samples = 1500
noise = 0.05


w = []
y = []
z = []
clas = []
names = []
data = []
X = []
with open('bm.txt', 'r') as bm:
            
    n=bm.readline()
    #print(n)
    for i in range(int(n)):
        line=bm.readline().split('\t')
        w.append(int(line[0]))
        y.append(int(line[1]))
        clas.append(int(line[2]))
            
        #print("AAA")
        #print(len(x))
with open('umx.txt', 'r') as umx:
    matrix = umx.read().split("\n")
            
    for i in range(int(n)):
        tmp=matrix[w[i]]
        s=tmp.split('\t')
        z.append(float(s[y[i]]))
        #print(len(clas))
        #print(len(x))
        #print(len(y))
        #print(len(z))
for i in range(int(n)):
            #data.append([x[i], y[i], z[i], clas[i]])
    X.append([w[i], y[i], z[i]])


#X=load_input('train.txt')
X = np.array(X)
c = np.array(clas)
#X, _ = make_swiss_roll(n_samples, noise)
print(X)
# Make it thinner
X[:, 1] *= .5

###############################################################################
# Define the structure A of the data. Here a 10 nearest neighbors
from sklearn.neighbors import kneighbors_graph
connectivity = kneighbors_graph(X, n_neighbors=10, include_self=False)

###############################################################################
# Compute clustering
print("Compute structured hierarchical clustering...")
cluster_num=input("cluster num: ")
cluster_num=int(cluster_num)

st = time.time()
ward = AgglomerativeClustering(n_clusters=cluster_num, connectivity=connectivity,
                               linkage='ward').fit(X)
elapsed_time = time.time() - st
label = ward.labels_

print(label)

num=cluster_num
#make precision
class_new = [[0*num] for row in range(num)]
match1= []

for i in range(int(n)):
    match1.append([label[i],c[i]])
    for j in range(num):
        if(c[i]==j):
            class_new[j].append(label[i])
                
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
    match2.append([label[i],c[i]])
    for j in range(num):
        if(label[i]==j):
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


# Plot result
fig = plt.figure()
ax = p3.Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
ax.view_init(30, -30)
for l in np.unique(label):
    ax.plot3D(X[label == l, 0], X[label == l, 1], X[label == l, 2],
              'o', color=plt.cm.jet(float(l) / np.max(label + 1)))
#ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels.astype(np.float))

#plt.title('With connectivity constraints (time %.2fs)' % elapsed_time)

plt.show()

