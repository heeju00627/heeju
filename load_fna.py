# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 07:18:57 2017

@author: heeju
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QMessageBox, QLabel, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'load'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.initUi()
        
    def initUi(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        fileName = self.openFileNameDialog()
        #fileName = self.saveFileNameDialog()
        self.show()
        
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Fna Files (*.fna)", options = options)
        if fileName:
            return fileName
        
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QfileDialog.getSaveFileName()", "", "All Files (*);;lrn Files (*.lrn)", options = options)
        if fileName:
            return fileName

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())