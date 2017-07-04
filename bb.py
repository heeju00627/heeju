# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 05:34:09 2017

@author: heeju
"""

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Goals For The Week")

def saveall():
    data=[] #clear list of data
    myfile = open('myfile.txt','w')
    for x in range(0,5):
        #read entire contents of each text widget
        data.append(text[x].get(1.0,tk.END))
        #write it to file with symbol '^' to separate each day
        myfile.write(data[x] + "^")
    myfile.close()

def openit():
    myfile=open('myfile.txt','r')
    #read all data in, split it by '^'
    alldata = myfile.read()
    data = alldata.split("^")
    x=0
    for line in data:
        #get rid of last 'enter'
        line = line[0:len(line) - 1]
        #clear each text box and replace with data
        text[x].delete(1.0,tk.END)
        text[x].insert(1.0, line)
        x+=1

#make your widgets
planner=ttk.Notebook(pad=10)
#list of 5 frames, text widgets, scrolls, and data for each text
frames=[]
text=[]
scroll=[]
data=[]
days=["Monday","Tuesday","Wednesday","Thursday","Friday"]

#frame for lower part of app
btnframe = ttk.Frame(pad=10, relief="groove")
btnsave=tk.Button(btnframe, text="Save Changes",command=saveall)
btnopen=tk.Button(btnframe, text="Open Planner", command=openit)
#pack buttons beside each other in frame with 10 spaces between
btnopen.pack(side="left", padx=10)
btnsave.pack(side="left", padx=10)

#frames, text widgets and scrolls for 5 days
for x in range(0,5):
      frames.append(ttk.Frame(planner))
      text.append(tk.Text(frames[x],width=60, height=10))
      scroll.append(tk.Scrollbar(frames[x]))
      text[x].pack(side="left")
      scroll[x].pack(side="left", fill="y")
      scroll[x].configure(command=text[x].yview)
      text[x].configure(yscrollcommand = scroll[x].set)
      planner.add(frames[x], text=days[x])

#add planner to app
planner.pack()
#add button frame to app right below it
btnframe.pack(pady=10)

root.mainloop()