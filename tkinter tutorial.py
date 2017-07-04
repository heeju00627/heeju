# -*- coding: utf-8 -*-
"""
Created on Fri May 12 10:43:14 2017

@author: heeju
"""

import tkinter as tk
import tkinter.messagebox

root = tk.Tk()

##LABEL
#theLabel = tk.Label(root, text="hi")
#theLabel.pack()
#
##FRAME
#topFrame = tk.Frame(root)
#topFrame.pack()
#bottomFrame = tk.Frame(root)
#bottomFrame.pack(side=tk.BOTTOM)
#
##BUTTON
#button1 = tk.Button(topFrame, text="Button 1", fg="red")
#button2 = tk.Button(topFrame, text="Button 2", fg="blue")
#button3 = tk.Button(topFrame, text="Button 3", fg="green")
#button4 = tk.Button(bottomFrame, text="Button 4", fg="purple")
#button1.pack(side=tk.LEFT)
#button2.pack(side=tk.LEFT)
#button3.pack(side=tk.LEFT)
#button4.pack(side=tk.BOTTOM)
#
##LAYOUT
#one = tk.Label(root, text="One", bg="red", fg="white")
#one.pack()
#two = tk.Label(root, text="Two", bg="green", fg="black")
#two.pack(fill=tk.X)
#three = tk.Label(root, text="Three", bg="blue", fg="white")
#three.pack(side=tk.LEFT, fill=tk.Y)
#
##GRID
#label_1 = tk.Label(root, text="Name")
#label_2 = tk.Label(root, text="Password")
#entry_1 = tk.Entry(root)
#entry_2 = tk.Entry(root)
#label_1.grid(row=0, sticky=tk.E)
#label_2.grid(row=1, sticky=tk.E)
#entry_1.grid(row=0, column=1)
#entry_2.grid(row=1, column=1)
#c = tk.Checkbutton(root, text="Keep me logged in")
#c.grid(columnspan=2)
#
##FUNCTION
#def printHello(event):
#    print("hello!")
#button_1 = tk.Button(root, text="Say hello")
##<Button-1> : left mouse button
#button_1.bind("<Button-1>", printHello)
#button_1.pack()
#
##MOUSE CLICK
#def leftClick(event):
#    print("Left")
#def middleClick(event):
#    print("Middle")
#def rightClick(event):
#    print("Right")
#frame = tk.Frame(root, width=300, height=250)
#frame.bind("<Button-1>", leftClick)
#frame.bind("<Button-2>", middleClick)
#frame.bind("<Button-3>", rightClick)
#frame.pack()
#
##CLASS
#class KimiButtons:
#    def __init__(self, master):
#        frame = tk.Frame(master)
#        frame.pack()
#        self.printButton = tk.Button(frame, text="Print Message", command=self.printMessage)
#        self.printButton.pack(side=tk.LEFT)
#        self.quitButton = tk.Button(frame, text="Quit", command=frame.quit)
#        self.quitButton.pack(side=tk.LEFT)
#    def printMessage(self):
#        print("Wow!")
#b = KimiButtons(root)
#
##MESSAGE BOX
#tk.messagebox.showinfo('hello', 'my name is...')
#answer=tk.messagebox.askquestion('question 1', 'do you like?')
#if answer == 'yes':
#    print("-------")
#
##CANVAS
#canvas = tk.Canvas(root, width=200, height=100)
#canvas.pack()
#blackLine = canvas.create_line(0, 0, 200, 50)
#redLine = canvas.create_line(0, 100, 200, 50, fill="red")
#greenBox = canvas.create_rectangle(25, 25, 130, 60, fill="green")
#canvas.delete(redLine)
#canvas.delete(tk.ALL)
#
##IMAGE
#photo = tk.PhotoImage(file="hello.png")
#label = tk.Label(root, image=photo)
#label.pack()


# **** Main Menu ****
menu = tk.Menu(root)
root.config(menu=menu)

fileMenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
# Menu.add_command(label, command)
fileMenu.add_command(label="Open...")
fileMenu.add_command(label="Save...")
fileMenu.add_separator()
fileMenu.add_command(label="Close...")  # 일부 file 닫기(목록에서 제거)
fileMenu.add_command(label="Quit")

runMenu = tk.Menu(menu)
menu.add_cascade(label="Run", menu=runMenu)
runMenu.add_command(label="Convert(fna->lrn)")
runMenu.add_command(label="Training...")

clusterMenu = tk.Menu(menu)
menu.add_cascade(label="Clustering", menu=clusterMenu)
clusterMenu.add_command(label="Result")


# **** Toolbar ****
#toolbar = tk.Frame(root)
#
#insertButt = tk.Button(toolbar, text="Insert Image")
#insertButt.pack(side=tk.LEFT, padx=2, pady=2)
#printButt = tk.Button(toolbar, text="Print")
#printButt.pack(side=tk.LEFT, padx=2, pady=2)
#
#toolbar.pack(side=tk.TOP, fill=tk.X)



# **** Status Bar ****
status = tk.Label(root, text="Preparing...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.pack(side=tk.BOTTOM, fill=tk.X)


root.mainloop()