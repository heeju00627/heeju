from minisom import MiniSom
from numpy import genfromtxt,array,linalg,zeros,mean,std,apply_along_axis
import numpy
"""
    This script shows how to use MiniSom on the Iris dataset.
    In partucular it shows how to train MiniSom and how to visualize the result.
    ATTENTION: pylab is required for the visualization.        
"""


# reading the iris dataset in the csv format    
# (downloaded from http://aima.cs.berkeley.edu/data/iris.csv)
#rn = len(open('iris4.csv').readlines())

data = genfromtxt('iris6.csv', delimiter=',',dtype = float)
data = numpy.nan_to_num(data)
print (data)
data = apply_along_axis(lambda x: x/linalg.norm(x),1,data) # data normalization

### Initialization and training ###
som = MiniSom(40,40,136,sigma=1.0,learning_rate=0.5)
som.random_weights_init(data)
print("Training...")
som.train_random(data,10000) # random training
print("\n...ready!")

### Plotting the response for each pattern in the iris dataset ###
from pylab import plot,axis,show,pcolor,colorbar,bone

bone()
pcolor(som.distance_map().T) # plotting the distance map as background
colorbar()

target = genfromtxt('iris4_2.csv',delimiter=',',usecols=(0),dtype=int) # loadingthe labels
t = zeros(len(target),dtype=int)
print (target)

t[target == 0] = 0
t[target == 1] = 1
t[target == 2] = 2
t[target == 3] = 3
t[target == 4] = 4
# use differet colors and markers for each label
#markers = []
colors = ['r','g','b','y','w']

with open('bm.txt', 'w') as f:    #making bm file
    for cnt,xx in enumerate(data):
         win = som.winner(xx) # getting the winner
     # palce a marker on the winning position for the sample xx
         plot(win[0]+.5,win[1]+.5,'.',markerfacecolor='None',markeredgecolor=colors[t[cnt]],markersize=1,markeredgewidth=1)
         f.write(str(win[0])+'\t'+str(win[1])+'\n')


with open('umx.txt', 'w') as f:    #making umx file
    for cnt,xx in enumerate(data):
     win = som.winner(xx) # getting the winner
     # palce a marker on the winning position for the sample xx
     plot(win[0]+.5,win[1]+.5,'.',markerfacecolor='None',
           markeredgecolor=colors[t[cnt]],markersize=1,markeredgewidth=1)
    um=som.distance_map()
    for i in range(40):
        for j in range(40):
            f.write(str(um[i,j])+'\t')
        f.write('\n')


f.close()
axis([0,som.weights.shape[0],0,som.weights.shape[1]])
show() # show the figure


